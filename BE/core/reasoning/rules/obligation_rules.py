from ..base import BaseRule, Fact
from typing import List

class ObligationRule(BaseRule):
    pass

# RULE OBL_001: Nghĩa vụ PEIA
class PEIARule(ObligationRule):
    def __init__(self):
        super().__init__("OBL_001", "Dự án Nhóm I phải thực hiện PEIA")
        
    def check(self, facts: List[Fact]) -> bool:
        for f in facts:
            if f.name == "project_group" and f.value == "I":
                return True
        return False
        
    def execute(self, facts: List[Fact]) -> List[Fact]:
        return [Fact(name="obligation", value="Thực hiện Đánh giá sơ bộ tác động môi trường (PEIA)", metadata={"source": "Điều 29, Khoản 1"})]

# RULE OBL_002: Nghĩa vụ ĐTM
class DTMRule(ObligationRule):
    def __init__(self):
        super().__init__("OBL_002", "Dự án Nhóm I/II phải lập ĐTM")
        
    def check(self, facts: List[Fact]) -> bool:
        group_i = False
        group_ii = False
        dtm_target = False
        
        for f in facts:
            if f.name == "project_group":
                if f.value == "I": group_i = True
                if f.value == "II": group_ii = True
            if f.name == "is_dtm_target" and f.value is True:
                dtm_target = True
                
        return group_i or (group_ii and dtm_target)
        
    def execute(self, facts: List[Fact]) -> List[Fact]:
        return [Fact(name="obligation", value="Lập Báo cáo đánh giá tác động môi trường (ĐTM)", metadata={"source": "Điều 30"})]

# RULE OBL_003: Giấy phép môi trường
class GPMTRule(ObligationRule):
    def __init__(self):
        super().__init__("OBL_003", "Dự án Nhóm I, II, III phải có GPMT")
        
    def check(self, facts: List[Fact]) -> bool:
        for f in facts:
            if f.name == "project_group" and f.value in ["I", "II", "III"]:
                return True
        return False
        
    def execute(self, facts: List[Fact]) -> List[Fact]:
        return [Fact(name="obligation", value="Phải có Giấy phép môi trường", metadata={"source": "Điều 39"})]
