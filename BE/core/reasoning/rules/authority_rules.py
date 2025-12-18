from ..base import BaseRule, Fact
from typing import List

class AuthorityRule(BaseRule):
    pass

# RULE AUTH_001: Thẩm quyền Bộ TN&MT
class BoTNMTAuthorityRule(AuthorityRule):
    def __init__(self):
        super().__init__("AUTH_001", "Bộ TN&MT thẩm định Nhóm I")
        
    def check(self, facts: List[Fact]) -> bool:
        for f in facts:
            if f.name == "project_group" and f.value == "I":
                return True
        return False

    def execute(self, facts: List[Fact]) -> List[Fact]:
        return [
            Fact(name="authority", value="Bộ Tài nguyên và Môi trường", metadata={"action": "Thẩm định ĐTM", "source": "Điều 35"}),
            Fact(name="authority", value="Bộ Tài nguyên và Môi trường", metadata={"action": "Cấp GPMT", "source": "Điều 41"})
        ]

# RULE AUTH_002: Thẩm quyền UBND Tỉnh
class ProvinceAuthorityRule(AuthorityRule):
    def __init__(self):
        super().__init__("AUTH_002", "UBND Tỉnh thẩm định Nhóm II")
        
    def check(self, facts: List[Fact]) -> bool:
        for f in facts:
            if f.name == "project_group" and f.value == "II":
                return True
        return False

    def execute(self, facts: List[Fact]) -> List[Fact]:
        return [
            Fact(name="authority", value="UBND cấp Tỉnh", metadata={"action": "Thẩm định ĐTM", "source": "Điều 35"}),
            Fact(name="authority", value="UBND cấp Tỉnh", metadata={"action": "Cấp GPMT", "source": "Điều 41"})
        ]
