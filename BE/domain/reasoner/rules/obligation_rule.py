"""Obligation rule - Query obligations of subjects from ChuThe nodes."""
from typing import Dict, Any, List
from .base_rule import BaseRule


class ObligationRule(BaseRule):
    """Rule to query obligations of subjects from Knowledge Graph."""
    
    @property
    def rule_name(self) -> str:
        return "ObligationRule"
    
    @property
    def description(self) -> str:
        return "Tra cứu nghĩa vụ của chủ thể trong Luật BVMT 2020"
    
    async def execute(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query obligations of a subject.
        
        Args:
            params: {"subject": "tên chủ thể"}
            
        Returns:
            List of obligations for the subject
        """
        subject = params.get("subject", "").strip()
        if not subject:
            return []
        
        query = """
        MATCH (c:ChuThe)-[r:CO_NGHIA_VU]->(k)
        WHERE toLower(c.ten) CONTAINS toLower($subject)
           OR toLower(c.mo_ta) CONTAINS toLower($subject)
        RETURN c.ten AS chu_the,
               c.loai AS loai_chu_the,
               k.ten AS nghia_vu,
               r.dieu_khoan AS dieu_khoan,
               r.dieu_kien AS dieu_kien,
               r.thoi_han AS thoi_han,
               r.noi_dung AS mo_ta_nghia_vu
        ORDER BY c.ten
        LIMIT 20
        """
        
        return await self._run_query(query, {"subject": subject})
    
    def format_results(self, results: List[Dict[str, Any]]) -> str:
        """Format obligation results for LLM context."""
        if not results:
            return "Không tìm thấy nghĩa vụ của chủ thể này trong cơ sở tri thức."
        
        # Group by subject
        by_subject = {}
        for r in results:
            subj = r['chu_the']
            if subj not in by_subject:
                by_subject[subj] = {
                    'loai': r.get('loai_chu_the', ''),
                    'nghia_vu': []
                }
            
            obligation = f"- {r['nghia_vu']}"
            if r.get('dieu_kien'):
                obligation += f" (Điều kiện: {r['dieu_kien']})"
            if r.get('thoi_han'):
                obligation += f" - Thời hạn: {r['thoi_han']}"
            if r.get('dieu_khoan'):
                obligation += f" [Căn cứ: {r['dieu_khoan']}]"
            
            by_subject[subj]['nghia_vu'].append(obligation)
        
        formatted = []
        for subj, data in by_subject.items():
            entry = f"**{subj}**"
            if data['loai']:
                entry += f" (Loại: {data['loai']})"
            entry += "\n" + "\n".join(data['nghia_vu'])
            formatted.append(entry)
        
        return "\n\n".join(formatted)
