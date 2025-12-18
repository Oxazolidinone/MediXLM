from ..base import BaseRule, Fact
from typing import List

class ExemptionRule(BaseRule):
    pass

# RULE EXEMPT_001: Miễn ĐTM (Đầu tư công khẩn cấp)
class ExemptDTMRule(ExemptionRule):
    def __init__(self):
        super().__init__("EXEMPT_001", "Dự án khẩn cấp miễn ĐTM")
        
    def check(self, facts: List[Fact]) -> bool:
        for f in facts:
            if f.name == "project_type" and f.value == "emergent_public_investment":
                return True
        return False
        
    def execute(self, facts: List[Fact]) -> List[Fact]:
        return [Fact(name="exemption", value="Miễn ĐTM", metadata={"source": "Điều 30, Khoản 2"})]
