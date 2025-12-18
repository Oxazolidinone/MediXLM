"""Authority rule - Query authorities for permissions/licenses."""
from typing import Dict, Any, List
from .base_rule import BaseRule


class AuthorityRule(BaseRule):
    """Rule to query authorities with jurisdiction from Knowledge Graph."""
    
    @property
    def rule_name(self) -> str:
        return "AuthorityRule"
    
    @property
    def description(self) -> str:
        return "Tra cứu cơ quan có thẩm quyền trong Luật BVMT 2020"
    
    async def execute(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query authorities for a specific permission/action.
        
        Args:
            params: {"permission": "loại giấy phép/thẩm quyền", "project_group": "nhóm dự án"}
            
        Returns:
            List of authorities with jurisdiction
        """
        permission = params.get("permission", "").strip()
        project_group = params.get("project_group", "").strip()
        
        # Query CoQuan with CO_THAM_QUYEN relationship
        query = """
        MATCH (cq:CoQuan)-[r:CO_THAM_QUYEN]->(k)
        WHERE ($permission = '' OR toLower(k.ten) CONTAINS toLower($permission))
           AND ($project_group = '' OR r.nhom_du_an = $project_group)
        RETURN cq.ten AS co_quan,
               cq.cap AS cap,
               cq.tham_quyen AS tham_quyen_chung,
               k.ten AS doi_tuong,
               r.noi_dung AS noi_dung_tham_quyen,
               r.dieu_khoan AS dieu_khoan,
               r.nhom_du_an AS nhom_du_an
        ORDER BY cq.cap
        LIMIT 15
        """
        
        results = await self._run_query(query, {
            "permission": permission,
            "project_group": project_group.upper() if project_group else ""
        })
        
        # If no direct results, query CoQuan general info
        if not results:
            fallback_query = """
            MATCH (cq:CoQuan)
            WHERE toLower(cq.ten) CONTAINS toLower($permission)
               OR toLower(cq.tham_quyen) CONTAINS toLower($permission)
            RETURN cq.ten AS co_quan,
                   cq.cap AS cap,
                   cq.tham_quyen AS tham_quyen,
                   cq.mo_ta AS mo_ta
            ORDER BY cq.cap
            LIMIT 10
            """
            results = await self._run_query(fallback_query, {"permission": permission})
        
        return results
    
    def format_results(self, results: List[Dict[str, Any]]) -> str:
        """Format authority results for LLM context."""
        if not results:
            return "Không tìm thấy thông tin về cơ quan thẩm quyền trong cơ sở tri thức."
        
        # Group by authority level
        by_level = {}
        for r in results:
            level = r.get('cap', 'Khác')
            if level not in by_level:
                by_level[level] = []
            by_level[level].append(r)
        
        level_order = ['trung_uong', 'tinh', 'huyen', 'xa', 'Khác']
        level_names = {
            'trung_uong': 'Cấp Trung ương',
            'tinh': 'Cấp Tỉnh/Thành phố',
            'huyen': 'Cấp Quận/Huyện',
            'xa': 'Cấp Xã/Phường',
            'Khác': 'Khác'
        }
        
        formatted = []
        for level in level_order:
            if level in by_level:
                formatted.append(f"### {level_names.get(level, level)}")
                for r in by_level[level]:
                    entry = f"**{r['co_quan']}**"
                    if r.get('doi_tuong'):
                        entry += f"\n- Thẩm quyền về: {r['doi_tuong']}"
                    if r.get('noi_dung_tham_quyen'):
                        entry += f"\n- Nội dung: {r['noi_dung_tham_quyen']}"
                    if r.get('tham_quyen_chung'):
                        entry += f"\n- Thẩm quyền chung: {r['tham_quyen_chung']}"
                    if r.get('nhom_du_an'):
                        entry += f"\n- Áp dụng cho: Dự án nhóm {r['nhom_du_an']}"
                    if r.get('dieu_khoan'):
                        entry += f"\n- Căn cứ: {r['dieu_khoan']}"
                    formatted.append(entry)
        
        return "\n\n".join(formatted)
