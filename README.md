# Multi-Modal Streamlit Chatbot

Local Streamlit page that sends one prompt to ChatGPT, Google Gemini, Groq, and Claude and puts their answers side by side.

Claude is included through Anthropic's Messages API, not Claude Code. It gets the same treatment as the other three: the same prompt, the same prompt technique, the same token limit, the same optional image, its own answer column, and a place in the comparison-judge list. It does not get Claude Code tools or any extra ability the page does not also give ChatGPT, Gemini, and Groq.

The sidebar offers the current public chat models. ChatGPT is GPT-6 and GPT-6.1 (`gpt-6.1-sol`, `gpt-6-astra`, `gpt-6.1-terra`, `gpt-6-luna`). Gemini is the Gemini 3 lineup (`gemini-3.8-flash`, `gemini-3.6-flash`, `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite`, `gemini-3.1-pro-preview`, `gemini-3-flash-preview`). Groq is `openai/gpt-oss-120b`, `openai/gpt-oss-20b`, and the vision model `qwen/qwen3.8-27b`. Claude is `claude-sonnet-5-5`, `claude-opus-5-5`, `claude-haiku-5-5`, and `claude-fable-5-2`.

The same system prompt and token limit go to all four APIs, so the differences you see come from the models rather than from different instructions. Temperature is shared where the API accepts it: Gemini and Groq receive it as set, Claude is capped at 1.0, and the current ChatGPT models omit it because they reject that parameter. A comparison section then lists similarities, differences, reasoning quality, and accuracy. This setup was used to run 100+ cross-model prompt evaluations, using prompt-engineering techniques and a privacy-first layout: the app runs on your machine, and chat history is deleted automatically.

## What the page does

- Sends one prompt to ChatGPT, Gemini, Groq, and Claude together. Claude is called through Anthropic's Messages API, not Claude Code.
- Applies one prompt technique to every model: zero-shot, chain-of-thought, structured reasoning, a role prompt, or a few-shot pattern. Extra instructions you type are added for all four.
- Shows the four answers in columns, with the model name and how long the call took.
- Scores shared wording locally, then asks a judge model you choose to write a structured comparison:
  - similarities
  - differences
  - reasoning quality of each answer
  - accuracy against an optional reference answer
- Attaches one optional image to that same prompt. PNG, JPEG, and WebP are sent with their real media types. A text-only model is reported as unable to read the image instead of being swapped for a different model.
- Skips a provider that has no API key and still compares the models that answered.

The judge is another call to one of the four providers. It is a reading of the answers, not an external source of truth. If you leave the reference answer empty, the accuracy note says that facts were not checked against a known answer.

## Models

- ChatGPT: `gpt-6-astra`, `gpt-6.1-sol`, `gpt-6.1-terra`, `gpt-6-luna`. All four accept images. They do not accept temperature, so that sidebar setting is omitted for ChatGPT.
- Gemini: `gemini-3.8-flash`, `gemini-3.6-flash`, `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite`, `gemini-3.1-pro-preview`, `gemini-3-flash-preview`. All accept images.
- Groq: `openai/gpt-oss-120b`, `openai/gpt-oss-20b`, and `qwen/qwen3.8-27b`. Only Qwen 3.8 27B accepts images.
- Claude: `claude-sonnet-5-5`, `claude-opus-5-5`, `claude-haiku-5-5`, `claude-fable-5-2`. All accept images. Temperature above 1.0 is sent as 1.0.

## Privacy

The app is meant to run locally.

- API keys are typed into password fields and kept in the Streamlit session in memory.
- Keys and transcripts are not written to disk and are not printed back on the page.
- Starting a new comparison deletes the previous one. You can turn that off in the sidebar; the page then keeps at most the last 20 comparisons, still only in memory.
- History is deleted automatically after 10 idle minutes. The sidebar can set that limit from 1 to 120 minutes.
- **Delete history now** clears the transcript and the prompt fields immediately.
- Closing the session drops the keys as well.
- Prompt text and any image are sent only to the providers whose keys you filled in. The judge also receives the prompt and the model answers.

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL Streamlit prints, then add keys in the sidebar:

- Groq: https://console.groq.com
- OpenAI: https://platform.openai.com
- Gemini: https://aistudio.google.com/api-keys
- Claude: https://platform.claude.com/settings/keys

For an image comparison, pick a vision-capable model. On Groq that is `qwen/qwen3.8-27b`. The listed ChatGPT, Gemini, and Claude models accept images.

## Layout

- `app.py` is the comparison page.
- `llm_handler.py` builds the shared prompt and calls each API.
- `comparison.py` computes wording overlap, builds the judge request, and decides when history expires.
- `tests/test_core.py` covers image encoding, vision-model checks, Claude's shared prompt and temperature cap, overlap, and history expiry.
