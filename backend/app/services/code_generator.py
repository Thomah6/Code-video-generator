from groq import Groq
import re
import json
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class CodeGenerator:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"
        logger.info(f"🤖 CodeGenerator initialized with model: {self.model}")

    def generate_concept(self, animation_type: str):
        logger.info(f"🎨 Generating concept for type: {animation_type}")
        prompt = f"""Tu es un expert en visualisations Python créatives.
Génère un concept ORIGINAL et UNIQUE pour une animation de type: {animation_type}.

Réponds UNIQUEMENT en JSON:
{{
  "title": "Titre accrocheur",
  "concept": "Description détaillée",
  "library": "matplotlib|pygame|turtle",
  "complexity": "medium|advanced"
}}"""
        
        logger.info("📡 Calling Groq API for concept generation...")
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=1.0,
            response_format={"type": "json_object"}
        )
        logger.info("✅ Groq API responded for concept")
        
        concept = json.loads(response.choices[0].message.content)
        logger.info(f"📝 Concept: {concept.get('title', 'Unknown')}")
        return concept

    def generate_code(self, concept: dict, duration: int):
        logger.info(f"💻 Generating code for: {concept.get('title', 'Unknown')}")
        prompt = f"""Génère le code Python complet pour cette animation: {concept['title']}.
Description: {concept['concept']}
Bibliothèque: {concept['library']}
Durée: {duration} secondes.

Le code doit être autonome, impressionnant, et se fermer après {duration} secondes.
Réponds UNIQUEMENT avec le code Python dans un bloc de code.
"""
        logger.info("📡 Calling Groq API for code generation...")
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        logger.info("✅ Groq API responded with code")
        
        content = response.choices[0].message.content
        code_match = re.search(r"```python\n(.*?)\n```", content, re.DOTALL)
        code = code_match.group(1).strip() if code_match else content.strip()
        
        logger.info(f"📊 Generated code length: {len(code)} characters")
        return code

code_generator = CodeGenerator()
