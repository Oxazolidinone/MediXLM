from ..base import BaseRule, Fact
from typing import List

class ConsequenceRule(BaseRule):
    pass

# RULE CONS_001: Hậu quả xả thải trái phép
class IllegalDischargeRule(ConsequenceRule):
    def __init__(self):
        super().__init__("CONS_001", "Xả thải trái phép dẫn đến xử phạt")
        
    def check(self, facts: List[Fact]) -> bool:
        for f in facts:
            if f.name == "action" and f.value in ["xả thải trái phép", "xả thải vượt chuẩn"]:
                return True
        return False
        
    def execute(self, facts: List[Fact]) -> List[Fact]:
        return [
            Fact(name="consequence", value="Xử phạt vi phạm hành chính", metadata={"source": "Nghị định 45/2022"}),
            Fact(name="consequence", value="Buộc khắc phục hậu quả", metadata={"source": "Điều 6 Luật BVMT"})
        ]

# RULE CONS_003: Không có GPMT
class NoLicenseRule(ConsequenceRule):
    def __init__(self):
        super().__init__("CONS_003", "Hoạt động không phép")
        
    def check(self, facts: List[Fact]) -> bool:
        has_license = False
        is_operating = False
        for f in facts:
            if f.name == "license_status" and f.value == "none": has_license = False
            if f.name == "status" and f.value == "operating": is_operating = True
            
        return is_operating and not has_license # Simplified logic
        
    def execute(self, facts: List[Fact]) -> List[Fact]:
        return [
            Fact(name="consequence", value="Đình chỉ hoạt động", metadata={"source": "Điều 6"}),
            Fact(name="consequence", value="Phạt tiền", metadata={"source": "Nghị định 45"})
        ]
