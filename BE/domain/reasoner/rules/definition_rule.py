"""Definition rule - Query concept definitions from KhaiNiem nodes."""
from typing import Dict, Any, List
from .base_rule import BaseRule


class DefinitionRule(BaseRule):
    """Rule to query concept definitions from Knowledge Graph."""
    
    @property
    def rule_name(self) -> str:
        return "DefinitionRule"
    
    @property
    def description(self) -> str:
        return "Tra cứu định nghĩa khái niệm trong Luật BVMT 2020"
    
    async def execute(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query definition of a concept.
        
        Args:
            params: {"term": "tên khái niệm cần tra cứu"}
            
        Returns:
            List of matching KhaiNiem nodes
        """
        term = params.get("term", "").strip()
        if not term:
            return []
        
        # Try exact match first, then fuzzy match
        query = """
        MATCH (k:KhaiNiem)
        WHERE toLower(k.ten) = toLower($term)
           OR toLower(k.ten) CONTAINS toLower($term)
           OR toLower(k.keyphrase) CONTAINS toLower($term)
        RETURN k.ten AS ten, 
               k.noi_dung AS noi_dung, 
               k.dieu_khoan AS dieu_khoan,
               k.chuong AS chuong,
               k.viet_tat AS viet_tat
        ORDER BY CASE WHEN toLower(k.ten) = toLower($term) THEN 0 ELSE 1 END
        LIMIT 5
        """
        
        return await self._run_query(query, {"term": term})
    
    def format_results(self, results: List[Dict[str, Any]]) -> str:
        """Format definition results for LLM context."""
        if not results:
            return "Không tìm thấy định nghĩa phù hợp trong cơ sở tri thức."
        
        formatted = []
        for r in results:
            entry = f"**{r['ten']}**"
            if r.get('viet_tat'):
                entry += f" ({r['viet_tat']})"
            entry += f"\n- Định nghĩa: {r['noi_dung']}"
            if r.get('dieu_khoan'):
                entry += f"\n- Căn cứ: {r['dieu_khoan']}"
            if r.get('chuong'):
                entry += f" (Chương {r['chuong']})"
            formatted.append(entry)
        
        return "\n\n".join(formatted)
