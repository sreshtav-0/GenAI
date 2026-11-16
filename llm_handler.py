"""Calls to ChatGPT, Gemini, Groq, and Claude, plus the shared prompt techniques."""

from __future__ import annotations

import base64
import time
from dataclasses import dataclass

PROVIDERS = ("openai", "gemini", "groq", "anthropic")

PROVIDER_LABELS = {
    "openai": "ChatGPT",
    "gemini": "Gemini",
    "groq": "Groq",
    "anthropic": "Claude",
}

MODEL_OPTIONS = {
    "openai": [
        "gpt-6.1-sol",
        "gpt-6-astra",
        "gpt-6.1-terra",
        "gpt-6-luna",
    ],
    "gemini": [
        "gemini-3.8-flash",
        "gemini-3.6-flash",
        "gemini-3.5-flash-lite",
        "gemini-3.1-flash-lite",
        "gemini-3.1-pro-preview",
        "gemini-3-flash-preview",
    ],
    "groq": [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b",
        "qwen/qwen3.8-27b",
    ],
    "anthropic": [
        "claude-sonnet-5-5",
        "claude-opus-5-5",
        "claude-haiku-5-5",
        "claude-fable-5-2",
    ],
}

# Models that accept an image plus text. Text-only models are not swapped in silently.
VISION_MODELS = {
    "openai": set(MODEL_OPTIONS["openai"]),
    "gemini": set(MODEL_OPTIONS["gemini"]),
    "groq": {
        "qwen/qwen3.8-27b",
    },
    "anthropic": set(MODEL_OPTIONS["anthropic"]),
}

ALLOWED_MIME_TYPES = {
    "image/png",
    "image/jpeg",
    "image/webp",
}

EXTENSION_MIME_TYPES = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "webp": "image/webp",
}

TECHNIQUES = {
    "Zero-shot": (
        "Answer the user's request directly. Do not add a preamble about being an AI."
    ),
    "Chain-of-thought": (
        "Think through the problem step by step before the final answer. "
        "Label the steps, then end with a line that starts with 'Final answer:'."
    ),
    "Structured reasoning": (
        "Use these sections: Assumptions, Reasoning, Answer, Uncertainties. "
        "Keep each section concrete."
    ),
    "Role prompt": (
        "You are a careful analyst. Separate what is stated, what you infer, "
        "and what you conclude."
    ),
    "Few-shot pattern": (
        "Follow the pattern in this example, then answer the user.\n"
        "Example question: Is 17 a prime number?\n"
        "Reasoning: 17 is not divisible by any integer from 2 through 16.\n"
        "Final answer: Yes, 17 is prime."
    ),
}


@dataclass
class CallResult:
    provider: str
    model: str
    text: str = ""
    error: str = ""
    seconds: float = 0.0


def provider_label(provider: str) -> str:
    return PROVIDER_LABELS.get(provider, provider)


def normalize_model_id(model: str) -> str:
    """Gemini settings used to store an extra 'models/' prefix the API does not want."""
    prefix = "models/"
    if model.startswith(prefix):
        return model[len(prefix) :]
    return model


def mime_from_upload(filename: str, content_type: str | None) -> str:
    if content_type in ALLOWED_MIME_TYPES:
        return content_type
    extension = filename.rsplit(".", 1)[-1].lower() if filename else ""
    mime = EXTENSION_MIME_TYPES.get(extension)
    if mime is None:
        raise ValueError("Upload a PNG, JPEG, or WebP image.")
    return mime


def encode_image_bytes(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def image_data_url(mime: str, encoded: str) -> str:
    if mime not in ALLOWED_MIME_TYPES:
        raise ValueError(f"Unsupported image type: {mime}")
    if not encoded or encoded != encoded.strip():
        raise ValueError("Image encoding is empty or padded with spaces.")
    return f"data:{mime};base64,{encoded}"


def temperature_for_provider(provider: str, model: str, temperature: float) -> float | None:
    """Return the temperature to send, or None when that API rejects the parameter.

    GPT-6 rejects temperature while it is reasoning. Claude accepts 0 through 1.
    """
    if provider == "openai" and normalize_model_id(model).startswith("gpt-6"):
        return None
    if provider == "anthropic":
        return max(0.0, min(1.0, temperature))
    return temperature


def build_anthropic_user_content(user_text: str, image: tuple[str, str] | None):
    if image is None:
        return user_text
    mime, encoded = image
    image_data_url(mime, encoded)
    return [
        {
            "type": "image",
            "source": {"type": "base64", "media_type": mime, "data": encoded},
        },
        {"type": "text", "text": user_text},
    ]


def vision_block_reason(provider: str, model: str, has_image: bool) -> str | None:
    if not has_image:
        return None
    model = normalize_model_id(model)
    if model in VISION_MODELS.get(provider, set()):
        return None
    label = provider_label(provider)
    return (
        f"{model} cannot read images. Choose a vision-capable {label} model, "
        "or remove the image so every model receives the same text prompt."
    )


def build_system_prompt(technique: str, extra_instructions: str) -> str:
    base = TECHNIQUES.get(technique, TECHNIQUES["Zero-shot"])
    extra = extra_instructions.strip()
    if not extra:
        return base
    return f"{base}\n\nAdditional instructions:\n{extra}"


def build_chat_messages(system_prompt: str, user_text: str, image: tuple[str, str] | None) -> list[dict]:
    user_content: str | list[dict] = user_text
    if image is not None:
        mime, encoded = image
        user_content = [
            {"type": "text", "text": user_text},
            {"type": "image_url", "image_url": {"url": image_data_url(mime, encoded)}},
        ]
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]


def call_provider(
    provider: str,
    api_key: str,
    model: str,
    system_prompt: str,
    user_text: str,
    temperature: float,
    max_tokens: int,
    image: tuple[str, str] | None = None,
) -> CallResult:
    """Send one prompt to one provider. Exceptions stay in CallResult.error."""
    model = normalize_model_id(model)
    started = time.perf_counter()
    result = CallResult(provider=provider, model=model)
    reason = vision_block_reason(provider, model, image is not None)
    if reason:
        result.error = reason
        result.seconds = time.perf_counter() - started
        return result
    if not api_key.strip():
        result.error = f"Add a {provider_label(provider)} API key in the sidebar."
        result.seconds = time.perf_counter() - started
        return result
    try:
        if provider == "groq":
            result.text = _groq_chat(api_key, model, system_prompt, user_text, temperature, max_tokens, image)
        elif provider == "openai":
            result.text = _openai_chat(api_key, model, system_prompt, user_text, temperature, max_tokens, image)
        elif provider == "gemini":
            result.text = _gemini_chat(api_key, model, system_prompt, user_text, temperature, max_tokens, image)
        elif provider == "anthropic":
            result.text = _anthropic_chat(api_key, model, system_prompt, user_text, temperature, max_tokens, image)
        else:
            result.error = f"Unknown provider: {provider}"
    except Exception as exc:
        result.error = f"{provider_label(provider)} request failed: {exc}"
    result.seconds = time.perf_counter() - started
    return result


def _groq_chat(
    api_key: str,
    model: str,
    system_prompt: str,
    user_text: str,
    temperature: float,
    max_tokens: int,
    image: tuple[str, str] | None,
) -> str:
    from groq import Groq

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=build_chat_messages(system_prompt, user_text, image),
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return _choice_text(response)


def _openai_chat(
    api_key: str,
    model: str,
    system_prompt: str,
    user_text: str,
    temperature: float,
    max_tokens: int,
    image: tuple[str, str] | None,
) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    request = {
        "model": model,
        "messages": build_chat_messages(system_prompt, user_text, image),
        "max_completion_tokens": max_tokens,
    }
    sent_temperature = temperature_for_provider("openai", model, temperature)
    if sent_temperature is not None:
        request["temperature"] = sent_temperature
    response = client.chat.completions.create(**request)
    return _choice_text(response)


def _anthropic_chat(
    api_key: str,
    model: str,
    system_prompt: str,
    user_text: str,
    temperature: float,
    max_tokens: int,
    image: tuple[str, str] | None,
) -> str:
    from anthropic import Anthropic

    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": build_anthropic_user_content(user_text, image),
            }
        ],
        temperature=temperature_for_provider("anthropic", model, temperature),
        max_tokens=max_tokens,
    )
    pieces = []
    for block in response.content:
        if getattr(block, "type", None) == "text" and getattr(block, "text", None):
            pieces.append(block.text)
    if not pieces:
        raise RuntimeError("Claude returned an empty response.")
    return "\n".join(pieces)


def _gemini_chat(
    api_key: str,
    model: str,
    system_prompt: str,
    user_text: str,
    temperature: float,
    max_tokens: int,
    image: tuple[str, str] | None,
) -> str:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    parts = [types.Part.from_text(text=user_text)]
    if image is not None:
        mime, encoded = image
        parts.append(
            types.Part.from_bytes(data=base64.b64decode(encoded), mime_type=mime)
        )
    response = client.models.generate_content(
        model=model,
        contents=parts,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=temperature,
            max_output_tokens=max_tokens,
        ),
    )
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text


def _choice_text(response) -> str:
    content = response.choices[0].message.content
    if isinstance(content, list):
        pieces = []
        for part in content:
            if isinstance(part, str):
                pieces.append(part)
            elif isinstance(part, dict):
                pieces.append(str(part.get("text") or ""))
            else:
                pieces.append(str(getattr(part, "text", "") or ""))
        content = "\n".join(piece for piece in pieces if piece.strip())
    if not content or not str(content).strip():
        raise RuntimeError("The model returned an empty response.")
    return str(content)
