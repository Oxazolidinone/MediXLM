from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class Fact(BaseModel):
    """Represents a piece of knowledge in Working Memory."""
    name: str
    value: Any
    metadata: Optional[Dict[str, Any]] = None

    def __hash__(self):
        return hash((self.name, str(self.value)))

    def __eq__(self, other):
        return self.name == other.name and self.value == other.value

class BaseRule:
    """Abstract base class for all reasoning rules."""
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description

    def check(self, facts: List[Fact]) -> bool:
        """Evaluate if the rule conditions are met given current facts."""
        raise NotImplementedError

    def execute(self, facts: List[Fact]) -> List[Fact]:
        """Return new facts derived from this rule."""
        raise NotImplementedError

class InferenceEngine:
    """Abstract base class for inference strategies."""
    def run(self, initial_facts: List[Fact], rules: List[BaseRule]) -> List[Fact]:
        raise NotImplementedError

    async def arun(self, initial_facts: List[Fact], rules: List[BaseRule]) -> List[Fact]:
        """Async version for IO-bound engines."""
        return self.run(initial_facts, rules)
