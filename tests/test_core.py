import unittest

from comparison import (
    build_judge_prompt,
    history_expired,
    jaccard_similarity,
    parse_judge_payload,
    surface_overlap,
)
from llm_handler import (
    build_anthropic_user_content,
    build_chat_messages,
    build_system_prompt,
    call_provider,
    image_data_url,
    mime_from_upload,
    normalize_model_id,
    temperature_for_provider,
    vision_block_reason,
)


class HandlerTests(unittest.TestCase):
    def test_png_data_url_keeps_its_mime_type(self):
        url = image_data_url("image/png", "abc123")
        self.assertEqual(url, "data:image/png;base64,abc123")
        self.assertNotIn("jepg", url)
        self.assertNotIn("base64, ", url)

    def test_upload_mime_prefers_the_browser_type(self):
        self.assertEqual(mime_from_upload("photo.png", "image/webp"), "image/webp")
        self.assertEqual(mime_from_upload("photo.jpg", None), "image/jpeg")

    def test_text_only_model_is_not_silently_replaced(self):
        reason = vision_block_reason("groq", "openai/gpt-oss-120b", True)
        self.assertIn("cannot read images", reason)
        self.assertIsNone(vision_block_reason("groq", "qwen/qwen3.8-27b", True))
        self.assertIsNone(vision_block_reason("openai", "gpt-6.1-sol", True))
        self.assertIsNone(vision_block_reason("anthropic", "claude-sonnet-5-5", True))

    def test_gemini_model_prefix_is_removed(self):
        self.assertEqual(normalize_model_id("models/gemini-2.5-flash"), "gemini-2.5-flash")

    def test_image_message_uses_the_same_user_text(self):
        messages = build_chat_messages("Be brief.", "Describe this", ("image/jpeg", "zzz"))
        self.assertEqual(messages[0]["content"], "Be brief.")
        self.assertEqual(messages[1]["content"][0]["text"], "Describe this")
        self.assertEqual(
            messages[1]["content"][1]["image_url"]["url"],
            "data:image/jpeg;base64,zzz",
        )

    def test_shared_technique_prompt(self):
        prompt = build_system_prompt("Chain-of-thought", "Use metric units.")
        self.assertIn("step by step", prompt)
        self.assertIn("Use metric units.", prompt)

    def test_image_request_does_not_call_a_text_only_model(self):
        result = call_provider(
            "groq",
            "not-a-real-key",
            "openai/gpt-oss-120b",
            "Be brief.",
            "Describe this",
            0.7,
            256,
            ("image/png", "abc123"),
        )
        self.assertIn("cannot read images", result.error)
        self.assertEqual(result.text, "")

    def test_missing_key_is_reported_without_a_network_call(self):
        result = call_provider(
            "openai",
            "  ",
            "gpt-6.1-sol",
            "Be brief.",
            "Hello",
            0.7,
            256,
            None,
        )
        self.assertIn("API key", result.error)

    def test_claude_gets_the_same_prompt_and_a_capped_temperature(self):
        content = build_anthropic_user_content("Describe this", ("image/png", "abc123"))
        self.assertEqual(content[1]["text"], "Describe this")
        self.assertEqual(content[0]["source"]["media_type"], "image/png")
        self.assertEqual(temperature_for_provider("anthropic", "claude-sonnet-5-5", 1.4), 1.0)
        self.assertIsNone(temperature_for_provider("openai", "gpt-6.1-sol", 0.7))
        self.assertEqual(temperature_for_provider("groq", "openai/gpt-oss-120b", 0.7), 0.7)


class ComparisonTests(unittest.TestCase):
    def test_identical_answers_overlap_completely(self):
        self.assertEqual(jaccard_similarity("alpha beta gamma", "alpha beta gamma"), 1.0)

    def test_pairwise_overlap_labels_each_pair(self):
        rows = surface_overlap(
            {
                "ChatGPT": "red blue green",
                "Gemini": "red blue yellow",
                "Groq": "red blue green",
            }
        )
        pairs = {row["pair"] for row in rows}
        self.assertEqual(
            pairs,
            {"ChatGPT vs Gemini", "ChatGPT vs Groq", "Gemini vs Groq"},
        )

    def test_history_expires_at_the_idle_limit(self):
        self.assertFalse(history_expired(100.0, 699.0, 10))
        self.assertTrue(history_expired(100.0, 700.0, 10))
        self.assertFalse(history_expired(None, 700.0, 10))

    def test_judge_json_with_a_fence_is_parsed(self):
        payload = parse_judge_payload(
            '```json\n{"similarities": ["both say 4"], "differences": []}\n```'
        )
        self.assertEqual(payload["similarities"], ["both say 4"])

    def test_judge_json_with_surrounding_prose_is_parsed(self):
        payload = parse_judge_payload(
            'Here is the comparison:\n{"similarities": ["same answer"], "differences": ["tone"]}\nDone.'
        )
        self.assertEqual(payload["differences"], ["tone"])

    def test_judge_prompt_includes_every_answer_and_the_reference(self):
        text = build_judge_prompt("What is 2+2?", {"ChatGPT": "4", "Groq": "four"}, "4")
        self.assertIn("What is 2+2?", text)
        self.assertIn("Answer from ChatGPT:\n4", text)
        self.assertIn("Answer from Groq:\nfour", text)
        self.assertIn("Reference answer:\n4", text)


if __name__ == "__main__":
    unittest.main()
