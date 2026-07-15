import json
import re
from pathlib import Path

from ollama import chat


class SOAPGenerator:

    def generate(self, transcript: str):

        prompt = (
            Path("app/prompts/soap_prompt.txt")
            .read_text(encoding="utf-8")
            .replace(
                "{{TRANSCRIPT}}",
                transcript,
            )
        )

        response = chat(
            model="mistral:latest",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        response_text = response.message.content.strip()

        # Remove markdown fences
        if response_text.startswith("```"):
            lines = [
                line
                for line in response_text.splitlines()
                if not line.startswith("```")
            ]
            response_text = "\n".join(lines)

        # Extract first JSON object
        match = re.search(
            r"\{[\s\S]*\}",
            response_text,
        )

        if not match:
            raise ValueError(
                "Model did not return valid JSON."
            )

        return json.loads(match.group())