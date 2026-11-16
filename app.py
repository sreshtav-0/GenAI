"""One page that sends the same prompt to ChatGPT, Gemini, and Groq."""

from __future__ import annotations

import base64
import time

import streamlit as st

from comparison import (
    JUDGE_SYSTEM_PROMPT,
    build_judge_prompt,
    history_expired,
    parse_judge_payload,
    string_list,
    surface_overlap,
)
from llm_handler import (
    MODEL_OPTIONS,
    PROVIDERS,
    TECHNIQUES,
    CallResult,
    build_system_prompt,
    call_provider,
    encode_image_bytes,
    mime_from_upload,
    provider_label,
    vision_block_reason,
)

DEFAULTS = {
    "groq_api_key": "",
    "openai_api_key": "",
    "gemini_api_key": "",
    "groq_model": "llama-3.3-70b-versatile",
    "openai_model": "gpt-4o-mini",
    "gemini_model": "gemini-2.5-flash",
    "temperature": 0.7,
    "max_tokens": 1024,
    "technique": "Chain-of-thought",
    "extra_instructions": "",
    "history_ttl_minutes": 10,
    "keep_only_latest": True,
    "judge_provider": "groq",
}

JUDGE_TEMPERATURE = 0.2
JUDGE_MAX_TOKENS = 1024


def init_state() -> None:
    for key, value in DEFAULTS.items():
        st.session_state.setdefault(key, value)
    st.session_state.setdefault("runs", [])
    st.session_state.setdefault("last_activity", None)
    st.session_state.setdefault("deletion_notice", None)
    st.session_state.setdefault("upload_key", 0)


def wipe_saved_text() -> None:
    """Clear the transcript and the form fields before those widgets are drawn.

    Popping the keys is not enough: the browser sends the previous text again
    on the next run and Streamlit restores it.
    """
    st.session_state.runs = []
    st.session_state.last_activity = None
    st.session_state.prompt_text = ""
    st.session_state.reference_answer = ""
    st.session_state.upload_key = int(st.session_state.get("upload_key", 0)) + 1


def on_delete() -> None:
    wipe_saved_text()
    st.session_state.deletion_notice = "Chat history was deleted."


def expire_transcript(now: float) -> None:
    if history_expired(
        st.session_state.last_activity,
        now,
        int(st.session_state.history_ttl_minutes),
    ):
        wipe_saved_text()
        st.session_state.deletion_notice = (
            "Chat history was deleted automatically after the idle limit."
        )


def sidebar() -> None:
    st.sidebar.header("Models")
    st.sidebar.caption(
        "Keys stay in this browser session only. They are not saved to disk "
        "and are not shown again on the page."
    )
    st.sidebar.text_input("ChatGPT API key", type="password", key="openai_api_key")
    st.sidebar.selectbox("ChatGPT model", MODEL_OPTIONS["openai"], key="openai_model")
    st.sidebar.text_input("Gemini API key", type="password", key="gemini_api_key")
    st.sidebar.selectbox("Gemini model", MODEL_OPTIONS["gemini"], key="gemini_model")
    st.sidebar.text_input("Groq API key", type="password", key="groq_api_key")
    st.sidebar.selectbox("Groq model", MODEL_OPTIONS["groq"], key="groq_model")

    st.sidebar.header("Shared prompt settings")
    st.sidebar.selectbox("Prompt technique", list(TECHNIQUES), key="technique")
    st.sidebar.text_area(
        "Extra instructions",
        key="extra_instructions",
        height=100,
        help="Added to the system prompt for every model, so the comparison stays fair.",
    )
    st.sidebar.slider("Temperature", 0.0, 2.0, step=0.1, key="temperature")
    st.sidebar.number_input(
        "Max tokens",
        min_value=256,
        max_value=8192,
        step=256,
        key="max_tokens",
    )
    st.sidebar.selectbox(
        "Comparison judge",
        PROVIDERS,
        format_func=provider_label,
        key="judge_provider",
        help="This model reads the three answers and writes the structured comparison. It uses a low temperature.",
    )

    st.sidebar.header("Privacy")
    st.sidebar.number_input(
        "Delete history after idle minutes",
        min_value=1,
        max_value=120,
        step=1,
        key="history_ttl_minutes",
    )
    st.sidebar.checkbox(
        "Delete the previous comparison when a new one starts",
        key="keep_only_latest",
    )
    st.sidebar.button("Delete history now", width="stretch", on_click=on_delete)


def read_image(uploaded) -> tuple[str, str] | None:
    if uploaded is None:
        return None
    mime = mime_from_upload(uploaded.name, getattr(uploaded, "type", None))
    return mime, encode_image_bytes(uploaded.getvalue())


def run_comparison(prompt: str, reference: str, image: tuple[str, str] | None) -> None:
    system_prompt = build_system_prompt(
        st.session_state.technique,
        st.session_state.extra_instructions,
    )
    temperature = float(st.session_state.temperature)
    max_tokens = int(st.session_state.max_tokens)
    jobs = []
    for provider in PROVIDERS:
        jobs.append(
            (
                provider,
                st.session_state[f"{provider}_api_key"],
                st.session_state[f"{provider}_model"],
            )
        )

    # One provider at a time. Streamlit's script runner can stall if these calls
    # are moved onto worker threads.
    results: dict[str, CallResult] = {}
    for provider, api_key, model in jobs:
        try:
            results[provider] = call_provider(
                provider,
                api_key,
                model,
                system_prompt,
                prompt,
                temperature,
                max_tokens,
                image,
            )
        except Exception as exc:
            results[provider] = CallResult(
                provider=provider,
                model=model,
                error=f"{provider_label(provider)} request failed: {exc}",
            )

    answers = {
        provider_label(provider): results[provider].text
        for provider in PROVIDERS
        if results[provider].text.strip()
    }
    judge = judge_answers(prompt, reference, answers)
    run = {
        "prompt": prompt,
        "reference": reference,
        "system_prompt": system_prompt,
        "image": image,
        "results": {provider: results[provider] for provider in PROVIDERS},
        "overlap": surface_overlap(answers),
        "judge": judge,
        "created_at": time.time(),
    }
    if st.session_state.keep_only_latest:
        st.session_state.runs = [run]
    else:
        st.session_state.runs.append(run)
        st.session_state.runs = st.session_state.runs[-20:]
    st.session_state.last_activity = run["created_at"]


def judge_answers(prompt: str, reference: str, answers: dict[str, str]) -> dict:
    if len(answers) < 2:
        return {
            "payload": None,
            "raw": "",
            "error": "A structured comparison needs answers from at least two models.",
            "judge_label": "",
        }
    judge_provider = st.session_state.judge_provider
    judge_key = st.session_state[f"{judge_provider}_api_key"]
    judge_model = st.session_state[f"{judge_provider}_model"]
    if not str(judge_key).strip():
        return {
            "payload": None,
            "raw": "",
            "error": f"Add a {provider_label(judge_provider)} API key to write the structured comparison.",
            "judge_label": provider_label(judge_provider),
        }
    result = call_provider(
        provider=judge_provider,
        api_key=judge_key,
        model=judge_model,
        system_prompt=JUDGE_SYSTEM_PROMPT,
        user_text=build_judge_prompt(prompt, answers, reference),
        temperature=JUDGE_TEMPERATURE,
        max_tokens=JUDGE_MAX_TOKENS,
        image=None,
    )
    payload = parse_judge_payload(result.text) if result.text else None
    error = result.error
    if result.text and payload is None:
        error = "The judge replied, but the reply was not valid JSON. The raw reply is shown below."
    return {
        "payload": payload,
        "raw": result.text,
        "error": error,
        "judge_label": f"{provider_label(judge_provider)} ({result.model})",
    }


def render_run(run: dict) -> None:
    st.subheader("Outputs")
    columns = st.columns(3)
    for column, provider in zip(columns, PROVIDERS):
        result: CallResult = run["results"][provider]
        with column:
            st.markdown(f"### {provider_label(provider)}")
            st.caption(f"{result.model} · {result.seconds:.1f}s")
            if result.error:
                st.error(result.error)
            if result.text:
                st.markdown(result.text)

    image = run.get("image")
    if image is not None:
        mime, encoded = image
        st.image(base64.b64decode(encoded), caption=f"Image sent with the prompt ({mime})")

    st.subheader("Comparison")
    overlap = run["overlap"]
    if overlap:
        st.markdown("**Shared wording**")
        st.caption("Word overlap between answers. This is not a measure of meaning or correctness.")
        st.dataframe(
            [{"Pair": row["pair"], "Overlap": f"{float(row['overlap']):.0%}"} for row in overlap],
            hide_index=True,
            width="stretch",
        )

    judge = run["judge"]
    if judge["judge_label"]:
        st.caption(f"Judge: {judge['judge_label']} at temperature {JUDGE_TEMPERATURE}.")
    if judge["error"]:
        st.warning(judge["error"])
    payload = judge["payload"]
    if payload:
        render_bullets("Similarities", string_list(payload.get("similarities")))
        render_bullets("Differences", string_list(payload.get("differences")))
        quality = payload.get("reasoning_quality")
        st.markdown("**Reasoning quality**")
        if isinstance(quality, dict):
            for name, note in quality.items():
                st.markdown(f"- **{name}:** {note}")
        elif quality:
            st.markdown(str(quality))
        accuracy = payload.get("accuracy")
        if accuracy:
            st.markdown("**Accuracy**")
            st.markdown(str(accuracy))
        caveats = payload.get("caveats")
        if caveats:
            st.markdown("**Caveats**")
            st.markdown(str(caveats))
    elif judge["raw"]:
        st.markdown(judge["raw"])

    with st.expander("Prompt sent to every model"):
        st.markdown("**System prompt**")
        st.code(run["system_prompt"])
        st.markdown("**User prompt**")
        st.code(run["prompt"])
        if run["reference"].strip():
            st.markdown("**Reference answer used for the accuracy note**")
            st.code(run["reference"])


def render_bullets(title: str, items: list[str]) -> None:
    st.markdown(f"**{title}**")
    if not items:
        st.caption("None listed.")
        return
    for item in items:
        st.markdown(f"- {item}")


def main() -> None:
    st.set_page_config(
        page_title="Side-by-side model comparison",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    init_state()
    expire_transcript(time.time())
    sidebar()

    st.title("Side-by-side model comparison")
    st.write(
        "One prompt is sent to ChatGPT, Gemini, and Groq with the same instructions, "
        "temperature, and token limit. Their answers stay on this page so you can "
        "compare reasoning and, when you supply a reference answer, accuracy."
    )
    st.caption(
        "Chat history lives in this session's memory. It is deleted when you start "
        "a new comparison, when the idle limit is reached, or when you press "
        "Delete history now. Closing the session drops the keys as well."
    )
    if st.session_state.deletion_notice:
        st.info(st.session_state.deletion_notice)
        st.session_state.deletion_notice = None

    missing = [
        provider_label(provider)
        for provider in PROVIDERS
        if not str(st.session_state[f"{provider}_api_key"]).strip()
    ]
    if missing:
        st.info("Add API keys to include " + ", ".join(missing) + ".")

    with st.form("comparison_form", clear_on_submit=False):
        prompt = st.text_area("Prompt", height=140, key="prompt_text")
        reference = st.text_area(
            "Reference answer (optional)",
            height=80,
            key="reference_answer",
            help="Used only by the comparison judge when it discusses accuracy.",
        )
        uploaded = st.file_uploader(
            "Image (optional)",
            type=["png", "jpg", "jpeg", "webp"],
            key=f"upload_{st.session_state.upload_key}",
        )
        submitted = st.form_submit_button("Compare models", type="primary", width="stretch")

    if submitted:
        if not prompt.strip():
            st.warning("Enter a prompt first.")
        elif len(missing) == len(PROVIDERS):
            st.warning("Add at least one API key in the sidebar.")
        else:
            try:
                image = read_image(uploaded)
            except ValueError as exc:
                st.error(str(exc))
            else:
                blocked = [
                    provider_label(provider)
                    for provider in PROVIDERS
                    if vision_block_reason(
                        provider,
                        st.session_state[f"{provider}_model"],
                        image is not None,
                    )
                ]
                if blocked:
                    st.warning(
                        "These models cannot read the attached image: "
                        + ", ".join(blocked)
                        + ". Choose a vision-capable model in the sidebar, or remove the image."
                    )
                with st.spinner("Asking the models and writing the comparison..."):
                    run_comparison(prompt.strip(), reference or "", image)

    for run in reversed(st.session_state.runs):
        render_run(run)
        st.divider()


if __name__ == "__main__":
    main()
