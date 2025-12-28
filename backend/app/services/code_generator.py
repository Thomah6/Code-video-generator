from groq import Groq
import re
import json
from app.core.config import settings

class CodeGenerator:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"

    def generate_concept(self, animation_type: str):
        prompt = f"""Tu es un expert en visualisations Python créatives.
Génère un concept ORIGINAL et UNIQUE pour une animation de type: {animation_type}.

Réponds UNIQUEMENT en JSON:
{{
  "title": "Titre accrocheur",
  "concept": "Description détaillée",
  "library": "matplotlib|pygame|turtle",
  "complexity": "medium|advanced"
}}"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=1.0,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    def generate_code(self, concept: dict, duration: int):
        prompt = f"""Génère le code Python complet pour cette animation: {concept['title']}.
Description: {concept['concept']}
Bibliothèque: {concept['library']}
Durée: {duration} secondes.

Le code doit être autonome, impressionnant, et se fermer après {duration} secondes.
Réponds UNIQUEMENT avec le code Python dans un bloc de code.
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        content = response.choices[0].message.content
        code_match = re.search(r"```python\n(.*?)\n```", content, re.DOTALL)
        return code_match.group(1).strip() if code_match else content.strip()

code_generator = CodeGenerator()
