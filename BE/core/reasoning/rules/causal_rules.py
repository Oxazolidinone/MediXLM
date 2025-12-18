from ..base import BaseRule, Fact
from typing import List

class CausalRule(BaseRule):
    pass

# RULE CAUSAL_001: Chuỗi ô nhiễm
class PollutionChainRule(CausalRule):
    def __init__(self):
        super().__init__("CAUSAL_001", "Ô nhiễm -> Thiệt hại -> Bồi thường")
        
    def check(self, facts: List[Fact]) -> bool:
        for f in facts:
            if f.name == "event" and f.value == "ô nhiễm môi trường":
                return True
        return False
        
    def execute(self, facts: List[Fact]) -> List[Fact]:
        return [
            Fact(name="event", value="suy thoái môi trường"),
            Fact(name="obligation", value="Bồi thường thiệt hại", metadata={"type": "derived_consequence"})
        ]
