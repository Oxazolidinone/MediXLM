"""Prompt templates for medical assistant."""
from pathlib import Path
from typing import Optional

# Base directory for prompt files
PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def load_system_prompt() -> str:
    """Load the main system prompt."""
    prompt_file = PROMPTS_DIR / "system_prompt.txt"
    if prompt_file.exists():
        return prompt_file.read_text(encoding="utf-8")
    return get_default_system_prompt()


def get_default_system_prompt() -> str:
    """Get default system prompt if file doesn't exist."""
    return """You are MediXLM, an AI medical assistant providing accurate, evidence-based medical information.

IMPORTANT:
- Base answers on the provided medical knowledge
- Acknowledge uncertainty when information is limited
- Recommend consulting healthcare professionals for diagnoses and treatment
- Never provide definitive diagnoses or prescribe medications
- Use clear, empathetic language

If patient describes emergency symptoms (chest pain, difficulty breathing, stroke signs, severe bleeding, suicidal thoughts), immediately recommend emergency care."""


def build_chat_prompt(knowledge_context: Optional[str] = None) -> str:
    """Build chat prompt with optional knowledge context."""
    base_prompt = load_system_prompt()

    if knowledge_context:
        return f"""{base_prompt}

## Relevant Medical Knowledge:
{knowledge_context}

Use this knowledge to inform your response, but always recommend professional medical evaluation for specific medical advice."""

    return base_prompt


def build_emergency_prompt() -> str:
    """Build prompt for emergency situations."""
    return """⚠️ EMERGENCY SITUATION DETECTED

Based on the symptoms described, this may be a medical emergency.

IMMEDIATE ACTION REQUIRED:
- Call emergency services (911 in US, 112 in EU) immediately
- Or go to the nearest Emergency Room
- Do not wait or drive yourself if symptoms are severe

Common emergency symptoms include:
- Chest pain or pressure
- Difficulty breathing
- Signs of stroke (Face drooping, Arm weakness, Speech difficulty)
- Severe bleeding
- Loss of consciousness
- Severe allergic reaction
- Suicidal thoughts with plan

Time is critical in medical emergencies. Please seek immediate help."""


def build_symptom_assessment_prompt() -> str:
    """Build prompt for symptom assessment."""
    return """To better understand your symptoms, I need to gather more information.

Please help me understand:
1. When did the symptoms start?
2. How severe are they (scale 1-10)?
3. What makes them better or worse?
4. Are there any other symptoms?
5. Have you tried anything for them?

Based on your answers, I'll provide guidance on whether this needs immediate medical attention, urgent care, or can be monitored at home."""


def format_knowledge_context(knowledge_items: list) -> str:
    """Format knowledge graph results for prompt."""
    if not knowledge_items:
        return "No specific medical knowledge found for this query."

    context_parts = []
    for item in knowledge_items:
        name = item.get("name", "")
        type_ = item.get("type", "")
        description = item.get("description", "")

        if name and description:
            context_parts.append(f"- {name} ({type_}): {description}")

    return "\n".join(context_parts)
