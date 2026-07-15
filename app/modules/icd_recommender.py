import json
import re
from pathlib import Path

import pandas as pd
from ollama import chat
from rapidfuzz import fuzz


class ICDRecommender:
    """
    Recommends ICD-10 codes from the SOAP assessment.
    """

    def __init__(self):

        self.df = pd.read_csv(
            "data/icd10.csv",
            header=None,
        )

        self.df.columns = [
            "category",
            "subcategory",
            "code",
            "description",
            "full_description",
            "short_description",
        ]

    def recommend(self, assessment):

        prompt = (
            Path("app/prompts/icd_prompt.txt")
            .read_text(encoding="utf-8")
            .replace(
                "{{ASSESSMENT}}",
                assessment,
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

        # Remove markdown code fences
        if response_text.startswith("```"):
            lines = [
                line
                for line in response_text.splitlines()
                if not line.startswith("```")
            ]
            response_text = "\n".join(lines)

        # Extract JSON object
        match = re.search(
            r"\{[\s\S]*\}",
            response_text,
        )

        if not match:
            raise ValueError(
                "No valid JSON returned by Ollama."
            )

        diagnoses = json.loads(
            match.group()
        )["diagnoses"]

        recommendations = []

        for diagnosis in diagnoses:

            scores = []

            for _, row in self.df.iterrows():

                score = fuzz.token_sort_ratio(
                    diagnosis.lower(),
                    str(row["short_description"]).lower(),
                )

                scores.append(
                    (
                        score,
                        str(row["code"]),
                        str(row["short_description"]),
                    )
                )

            scores.sort(
                key=lambda x: x[0],
                reverse=True,
            )

            score, code, desc = scores[0]

            recommendations.append(
                {
                    "diagnosis": diagnosis,
                    "code": code,
                    "description": desc,
                    "confidence": int(score),
                }
            )

        return {
            "assessment": assessment,
            "normalized_diagnoses": diagnoses,
            "recommendations": recommendations,
        }