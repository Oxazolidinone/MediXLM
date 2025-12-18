from ..base import BaseRule, Fact
from typing import List

class TimeRule(BaseRule):
    pass

# RULE TIME_001: Thời hạn thẩm định ĐTM
class TimeDTMRule(TimeRule):
    def __init__(self):
        super().__init__("TIME_001", "Thời hạn thẩm định ĐTM theo nhóm")
        
    def check(self, facts: List[Fact]) -> bool:
        for f in facts:
            if f.name == "action" and f.value == "thẩm định ĐTM":
                return True
        return False
        
    def execute(self, facts: List[Fact]) -> List[Fact]:
        new_facts = []
        # Check project group context
        group = None
        for f in facts:
            if f.name == "project_group":
                group = f.value
                
        if group == "I":
            new_facts.append(Fact(name="deadline", value="45 ngày", metadata={"context": "Nhóm I"}))
        elif group == "II":
             new_facts.append(Fact(name="deadline", value="30 ngày", metadata={"context": "Nhóm II"}))
             
        return new_facts
