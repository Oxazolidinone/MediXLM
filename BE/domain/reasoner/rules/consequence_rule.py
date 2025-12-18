"""Consequence rule - Query consequences of violations."""
from typing import Dict, Any, List
from .base_rule import BaseRule


class ConsequenceRule(BaseRule):
    """Rule to query consequences of violations from Knowledge Graph."""
    
    @property
    def rule_name(self) -> str:
        return "ConsequenceRule"
    
    @property
    def description(self) -> str:
        return "Tra cứu hậu quả của hành vi vi phạm trong Luật BVMT 2020"
    
    async def execute(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query consequences of an action/violation.
        
        Args:
            params: {"action": "hành vi vi phạm"}
            
        Returns:
            List of consequences for the action
        """
        action = params.get("action", "").strip()
        if not action:
            return []
        
        # Query HanhVi -> consequences chain
        query = """
        MATCH (h:HanhVi)-[r:DAN_DEN|GAY_RA*1..3]->(c)
        WHERE toLower(h.ten) CONTAINS toLower($action)
           OR toLower(h.mo_ta) CONTAINS toLower($action)
        RETURN h.ten AS hanh_vi,
               h.trang_thai AS trang_thai,
               h.mo_ta AS mo_ta_hanh_vi,
               c.ten AS hau_qua,
               labels(c) AS loai_hau_qua,
               h.dieu_khoan AS dieu_khoan
        LIMIT 15
        """
        
        results = await self._run_query(query, {"action": action})
        
        # If no direct HanhVi found, search in CheTai
        if not results:
            fallback_query = """
            MATCH (ct:CheTai)
            WHERE toLower(ct.ten) CONTAINS toLower($action)
               OR toLower(ct.mo_ta) CONTAINS toLower($action)
            RETURN ct.ten AS che_tai,
                   ct.mo_ta AS mo_ta,
                   ct.muc_phat AS muc_phat,
                   ct.dieu_khoan AS dieu_khoan
            LIMIT 10
            """
            results = await self._run_query(fallback_query, {"action": action})
        
        # Try searching in KhaiNiem for violation-related concepts
        if not results:
            fallback_query2 = """
            MATCH (k:KhaiNiem)
            WHERE (toLower(k.ten) CONTAINS 'vi phạm'
               OR toLower(k.ten) CONTAINS 'xử lý'
               OR toLower(k.ten) CONTAINS 'xử phạt'
               OR toLower(k.ten) CONTAINS 'bồi thường')
              AND (toLower(k.noi_dung) CONTAINS toLower($action)
               OR toLower(k.ten) CONTAINS toLower($action))
            RETURN k.ten AS khai_niem,
                   k.noi_dung AS noi_dung,
                   k.dieu_khoan AS dieu_khoan
            LIMIT 10
            """
            results = await self._run_query(fallback_query2, {"action": action})
        
        return results
    
    def format_results(self, results: List[Dict[str, Any]]) -> str:
        """Format consequence results for LLM context."""
        if not results:
            return "Không tìm thấy thông tin về hậu quả của hành vi này trong cơ sở tri thức."
        
        formatted = []
        for r in results:
            if 'hanh_vi' in r:
                entry = f"**Hành vi: {r['hanh_vi']}**"
                if r.get('trang_thai'):
                    entry += f" (Trạng thái: {r['trang_thai']})"
                if r.get('mo_ta_hanh_vi'):
                    entry += f"\n- Mô tả: {r['mo_ta_hanh_vi']}"
                if r.get('hau_qua'):
                    entry += f"\n- Hậu quả: {r['hau_qua']}"
                if r.get('loai_hau_qua'):
                    entry += f" (Loại: {', '.join(r['loai_hau_qua'])})"
                if r.get('dieu_khoan'):
                    entry += f"\n- Căn cứ: {r['dieu_khoan']}"
            elif 'che_tai' in r:
                entry = f"**Chế tài: {r['che_tai']}**"
                if r.get('mo_ta'):
                    entry += f"\n- Mô tả: {r['mo_ta']}"
                if r.get('muc_phat'):
                    entry += f"\n- Mức phạt: {r['muc_phat']}"
                if r.get('dieu_khoan'):
                    entry += f"\n- Căn cứ: {r['dieu_khoan']}"
            elif 'khai_niem' in r:
                entry = f"**{r['khai_niem']}**"
                if r.get('noi_dung'):
                    entry += f"\n- Nội dung: {r['noi_dung']}"
                if r.get('dieu_khoan'):
                    entry += f"\n- Căn cứ: {r['dieu_khoan']}"
            else:
                entry = str(r)
            
            formatted.append(entry)
        
        return "\n\n".join(formatted)
