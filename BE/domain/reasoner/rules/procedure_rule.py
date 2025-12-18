"""Procedure rule - Query required procedures for projects."""
from typing import Dict, Any, List
from .base_rule import BaseRule


class ProcedureRule(BaseRule):
    """Rule to query required procedures for project types."""
    
    @property
    def rule_name(self) -> str:
        return "ProcedureRule"
    
    @property
    def description(self) -> str:
        return "Tra cứu thủ tục hành chính cho loại dự án"
    
    async def execute(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query procedures for a project type.
        
        Args:
            params: {"project_type": "loại dự án", "project_group": "nhóm dự án (I, II, III, IV)"}
            
        Returns:
            List of required procedures
        """
        project_type = params.get("project_type", "").strip()
        project_group = params.get("project_group", "").strip()
        
        # Query procedures by project type or group
        query = """
        MATCH (d:DuAn)-[r:YEU_CAU]->(t:ThuTuc)
        WHERE ($project_type = '' OR toLower(d.ten) CONTAINS toLower($project_type))
          AND ($project_group = '' OR d.nhom = $project_group)
        RETURN d.ten AS du_an,
               d.nhom AS nhom,
               t.ten AS thu_tuc,
               t.mo_ta AS mo_ta,
               r.bat_buoc AS bat_buoc,
               r.dieu_khoan AS dieu_khoan,
               r.thu_tu AS thu_tu
        ORDER BY d.nhom, r.thu_tu
        LIMIT 20
        """
        
        results = await self._run_query(query, {
            "project_type": project_type,
            "project_group": project_group.upper() if project_group else ""
        })
        
        # If no direct procedures found, search in KhaiNiem relationships
        if not results:
            fallback_query = """
            MATCH (k:KhaiNiem)
            WHERE toLower(k.ten) CONTAINS 'thủ tục'
               OR toLower(k.ten) CONTAINS 'đăng ký'
               OR toLower(k.ten) CONTAINS 'giấy phép'
               OR toLower(k.ten) CONTAINS 'đánh giá'
            RETURN k.ten AS thu_tuc,
                   k.noi_dung AS mo_ta,
                   k.dieu_khoan AS dieu_khoan
            LIMIT 10
            """
            results = await self._run_query(fallback_query, {})
        
        return results
    
    def format_results(self, results: List[Dict[str, Any]]) -> str:
        """Format procedure results for LLM context."""
        if not results:
            return "Không tìm thấy thủ tục phù hợp trong cơ sở tri thức."
        
        formatted = []
        for r in results:
            if 'du_an' in r:
                entry = f"**Dự án: {r['du_an']}** (Nhóm {r.get('nhom', 'N/A')})"
                entry += f"\n- Thủ tục: {r['thu_tuc']}"
                if r.get('mo_ta'):
                    entry += f"\n- Mô tả: {r['mo_ta']}"
                if r.get('bat_buoc'):
                    entry += f"\n- Bắt buộc: {'Có' if r['bat_buoc'] else 'Không'}"
                if r.get('dieu_khoan'):
                    entry += f"\n- Căn cứ: {r['dieu_khoan']}"
            else:
                entry = f"**{r['thu_tuc']}**"
                if r.get('mo_ta'):
                    entry += f"\n- Mô tả: {r['mo_ta']}"
                if r.get('dieu_khoan'):
                    entry += f"\n- Căn cứ: {r['dieu_khoan']}"
            
            formatted.append(entry)
        
        return "\n\n".join(formatted)
