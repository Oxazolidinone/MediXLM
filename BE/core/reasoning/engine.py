from typing import List, Type
from .base import BaseRule, Fact, InferenceEngine

class RuleEngine:
    def __init__(self):
        self.rules: List[BaseRule] = []
        self.engines: dict[str, InferenceEngine] = {}

    def add_rule(self, rule: BaseRule):
        self.rules.append(rule)

    def register_strategy(self, name: str, engine: InferenceEngine):
        self.engines[name] = engine

    def infer(self, strategy: str, initial_facts: List[Fact]) -> List[Fact]:
        if strategy not in self.engines:
            raise ValueError(f"Strategy {strategy} not registered")
        return self.engines[strategy].run(initial_facts, self.rules)

    async def ainfer(self, strategy: str, initial_facts: List[Fact]) -> List[Fact]:
        if strategy not in self.engines:
            raise ValueError(f"Strategy {strategy} not registered")
        return await self.engines[strategy].arun(initial_facts, self.rules)
