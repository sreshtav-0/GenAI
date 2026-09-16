from __future__ import annotations

import os
import json
from typing import Any

from langchain.tools import tool
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langgraph.types import Command

from deepagents import FilesystemPermission, create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from deepagents.backends.utils import create_file_data

from rich.console import Console
from dotenv import load_dotenv

load_dotenv()

console = Console()

# ----- MODEL AND SYSTEM PROMPT -----
MODEL = os.getenv("DEEP_AGENT_MODEL", "openai:gpt-5.5")
SYSTEM_PROMPT = """\
You are a Research & Notes Assistant for a developer.

Conventions:
- A user-scoped memory file lives at /memories/preferences.md. Read it at the
start of every conversation. Update it (via edit_file) when the user tells
you a new lasting preference - keep it concise and de-duplicated.
- Skills live under /skills/. Match each user request against the skill
descriptions and follow any skill whose description fits.
- /workspace/ is your scratch area; read and write notes there freely.

Style: direct answer first, minimum necessary context, cite sources, and ask
before any destructive action.
"""

@tool

def web_fetch(url:str)->str:
    """
    Fetch the text contents of a URL. Read-only side-effects; safe to call freely.
    """
    return f"[stub: page contents of {url}]"

@tool
def send_notification(channel:str, message:str)->str:
    """    
    Send a notification to a channel (Slack/email/etc.)
    This has external side effects, so it is gated behind HITL with the `edit` option 
    enabled (humans can fix the recipient/wording before sending).
    """
    return f"Notification sent to '{channel}':{message}"

@tool
def delete_workspace_file(path:str)->str:
    """
    Permanently delete a file under /workspace. Destrucive: gated by HITL.
    """
    return f"Deleted {path}"

ARXIV_SKILL = """\
---
name: arxiv-search
description: Use this skill when the user asks about research papers, preprints, or the state-of-the-art on an ML/AI topic. It searches arXiv via web_fetch and digests the top results.
---

# arxiv-search

## When to use
- "find papers on X"
- "what's the latest research on Y"
- "summarise recent arxiv papers about Z"

## Steps
1. Build a query URL: `https://arxiv.org/search/?searchtype=all&query=<encoded-query>`.
2. Call `web_fetch(url)` to retrieve the listing.
3. Parse out the top 3-5 results (title, authors, abstract).
4. For any paper the user wants deeper context on, fetch its abstract page.
5. Return a concise digest: title, link, 2-line summary, why-it-matters.

## Output format
Always finish with a **References** section listing arXiv IDs and URLs.
"""

CODE_REVIEW_SKILL = """\
---
name: code-review
description: Use this skill when the user asks you to review, audit, or critique code (Python, TypeScript, etc.). Produces a structured review covering correctness, style, performance, security, and tests.
---

# code-review

## When to use
- "review this snippet"
- "audit my function"
- "what would you change about this code"

## Steps
1. Read the snippet (inline in the message, or via `read_file` if path given).
2. Walk through it once for **correctness** (bugs, edge cases, off-by-ones).
3. Walk through it again for **style** (naming, structure, idioms).
4. Note any **performance** issues (allocations, complexity, hot loops).
5. Note any **security** concerns (injection, secrets, deserialization).
6. Suggest **tests** the author should add.

## Output format
### Correctness
- ...
### Style
- ...
### Performance
- ...
### Security
- ...
### Tests to add
- ...
"""

# Initial preferences seeded for the demo user.
SEED_PREFERENCES = """\
## User preferences
- Prefers Python and TypeScript code examples
- Working on AI agents, RAG, and React Native projects
- Likes concise explanations with one short worked example
"""

# ----- BACKEND, STORE SEEDING, AND AGENT CONSTTRUCTION ----- 
# Namespaces for the store. Skills are shared across all users;
# Memories are isolated per-user.
SKILLS_NAMESPACE = ("shared", "skills")
def seed_store(user_id:str) -> InMemoryStore:
    """
    Pre-populate the Store with skills (agent-scoped) and prefs (user-scoped)
    """
    store = InMemoryStore()
    store.put(
        SKILLS_NAMESPACE,
        "/skills/arxiv-search/SKILL.md",
        create_file_data(ARXIV_SKILL)
    )
    store.put(
        SKILLS_NAMESPACE,
        "/skills/code-review/SKILL.md",
        create_file_data(CODE_REVIEW_SKILL)
    )
    store.put(
        (user_id,),
        "/memories/preferences.md",
        create_file_data(SEED_PREFERENCES)
    )
    return store

def build_agent(user_id:str="demo-user"):
    store = seed_store(user_id)
    checkpointer = InMemorySaver() # REQUIRED for HITL

    # -- Backend -----------------------------------
    # /workspace/ and any other unrouted path -> StateBackend (thread-scoped)
    # /memories/  -> StoreBackend, namespaced by user_id (persists across threads)
    # /skills/    -> StoreBackend, shared namespace (persists; same for all users)

    backend = CompositeBackend(
        default=StateBackend(),
        routes = {
            "/memories/": StoreBackend(
                namespace=lambda rt: (user_id,),
            ),
            "/skills/": StoreBackend(
                namespace=lambda rt: SKILLS_NAMESPACE,
            )
        }
    )
    # -- Permissions -----------------------------------
    # With a CompositeBackend, every permission path must fall under a known
    # route, so we deliberately scope each rule. First-match-wins, so put the
    # more specific rules first.
    permissions = [
        # Skills are read-only - the agent cannot modify its own playbook
        FilesystemPermission(
            operations=["write"],
            paths=["/skills/**"],
            mode="deny"
        ),
        # Memories are read + write so that agent can update preferences
        FilesystemPermission(
            operations=["read", "write"],
            paths=["/memories/**"],
            mode="allow"
        )
    ]
    # -- Human-in-the-loop -----------------------------------
    # Disable interrupts for safe, read-only ops. Gate writes and external
    # side-effects. `edit` is allowed where humans might want to fix args
    # (e.g. wrong recipient on a notification).
    interrupt_on:dict[str, Any] = {
        # Built-in filesystem tools
        "ls": False,
        "read_file": False,
        "glob": False,
        "grep": False,
        "write_file": {"allowed_decisions": ["approve", "reject"]},
        "edit_file": {"allowed_decisions": ["approve", "edit", "reject"]},
        # Custom tools
        "web_fetch": False,
        "send_notification": {"allowed_decisions": ["approve", "edit", "reject"]},
        "delete_workspace_file": {"allowed_decisions": ["approve", "reject"]},
    } 

    agent = create_deep_agent(
        model = MODEL,
        system_prompt = SYSTEM_PROMPT,
        tools = [web_fetch, send_notification, delete_workspace_file],
        backend=backend,
        store=store,
        memory=["memories/preferences.md"],
        skills=["/skills/"],
        permissions=permissions,
        interrupt_on = interrupt_on,
        checkpointer = checkpointer
    )

    return agent

def prompt_for_decision(action:dict, allowed: list[str])->dict:
    """
    Ask the human how to handle a pending tool call.
    
    Returns one of:
    {"type: "approve}
    {"type: "reject}
    {"type": "edit", "edited_action": {"name: <tool>, "args": {...}}}
    """
    console.print("[bold #63458A]\n---Approval required---[/bold #63458A]")
    console.print(f"[bold #3B1F2B]Tool: {action['name']}[/bold #3B1F2B]")
    console.print(f"[bold #FF8811]Args: {json.dumps(action['args'], indent=2)}[/bold #FF8811]")
    console.print(f"[bold green]Allowed: {allowed}[/bold green]")
    while True:
        choice = console.input(f"Decision [{'/'.join(allowed)}]: ").strip().lower()
        if choice == "approve" and "approve" in allowed:
            return {"type": "approve"}
        if choice == "reject" and "reject" in allowed:
            return {"type": "reject"}
        if choice == "edit" and "edit" in allowed:
            raw = input("Paste replacement args on JSON: ").strip()
            try:
                new_args = json.loads(raw)
            except json.JSONDecodeError as exc:
                console.print(f"[bold red]Invalid JSON: {exc}[/bold red]")
                continue
            return {
                "type": "edit",
                "edited_action": {"name": action["name"], "args": new_args}
            }
        console.print("[bold #FF1654]Invalid choice, try again[/bold #FF1654]")

def run_turn(agent, message:str, config:dict)->str:
    """
    Run a single user turn, resolving any interrupts before returning
    """
    result = agent.invoke(
        {"messages": [{"role": "user", "content":message}]},
        config=config,
        version="v2"
    )
    # An agent step may produce multiple batch interrupts. Decision must
    # be returned in the same order of 'action_requests'
    while getattr(result, "interrupts", None):
        interrupt_value = result.interrupts[0].value
        action_requests = interrupt_value["action_requests"]
        review_map = {
            cfg["action_name"]: cfg for cfg in interrupt_value["review_configs"]
        }
 
        decisions = [
            prompt_for_decision(act, review_map[act["name"]]["allowed_decisions"])
            for act in action_requests
        ]
 
        result = agent.invoke(
            Command(resume={"decisions": decisions}),
            config=config,
            version="v2",
        )
 
    return result.value["messages"][-1].content

def main() -> None:
    user_id = os.getenv("USER_ID", "sreshtav")
    agent = build_agent(user_id=user_id)
 
    # Same thread_id across turns -> single conversation. Long-term memory
    # under /memories/ survives across threads because of the Store.
    thread_id = str(uuid7())
    config = {"configurable": {"thread_id": thread_id}}
 
    print(f"Deep Agent ready  (user={user_id}, thread={thread_id[:8]}...)")
    print("Type 'exit' to quit.\n")
 
    while True:
        try:
            user_msg = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user_msg or user_msg.lower() in {"exit", "quit"}:
            break
        try:
            reply = run_turn(agent, user_msg, config)
        except Exception as exc:  # noqa: BLE001
            print(f"\n[error] {exc}\n")
            continue
        print(f"\nagent> {reply}\n")
 
 
if __name__ == "__main__":
    main()

