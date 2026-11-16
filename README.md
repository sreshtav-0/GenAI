# Multi-Modal Streamlit Chatbot

Local Streamlit page that sends one prompt to ChatGPT, Google Gemini, and Groq and puts their answers side by side.

The same system prompt, temperature, and token limit go to all three APIs, so the differences you see come from the models rather than from different instructions. A comparison section then lists similarities, differences, reasoning quality, and accuracy. This setup was used to run 100+ cross-model prompt evaluations, using prompt-engineering techniques and a privacy-first layout: the app runs on your machine, and chat history is deleted automatically.

## What the page does

- Sends one prompt to ChatGPT, Gemini, and Groq together.
- Applies one prompt technique to every model: zero-shot, chain-of-thought, structured reasoning, a role prompt, or a few-shot pattern. Extra instructions you type are added for all three.
- Shows the three answers in columns, with the model name and how long the call took.
- Scores shared wording locally, then asks a judge model you choose to write a structured comparison:
  - similarities
  - differences
  - reasoning quality of each answer
  - accuracy against an optional reference answer
- Attaches one optional image to that same prompt. PNG, JPEG, and WebP are sent with their real media types. A text-only model is reported as unable to read the image instead of being swapped for a different model.
- Skips a provider that has no API key and still compares the models that answered.

The judge is another call to one of the three providers. It is a reading of the answers, not an external source of truth. If you leave the reference answer empty, the accuracy note says that facts were not checked against a known answer.

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

For an image comparison, pick a vision-capable model. On Groq that is Llama 4 Scout or Llama 4 Maverick. The listed ChatGPT and Gemini models accept images.

## Layout

- `app.py` is the comparison page.
- `llm_handler.py` builds the shared prompt and calls each API.
- `comparison.py` computes wording overlap, builds the judge request, and decides when history expires.
- `tests/test_core.py` covers image encoding, vision-model checks, overlap, and history expiry.
