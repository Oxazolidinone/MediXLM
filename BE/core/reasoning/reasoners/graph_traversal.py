# -*- coding: utf-8 -*-
"""
GraphTraversalReasoner - Graph-based path finding and chain reasoning.
Uses BFS/DFS to traverse relationships in the Knowledge Graph.
"""
import time
import re
from typing import Dict, Any, List
from .base_reasoner import BaseReasoner, ReasonerResult, ReasonerType


class GraphTraversalReasoner(BaseReasoner):
    """
    Graph Traversal Reasoner.
    
    Strategy:
    1. Find starting node via FTS
    2. Traverse outgoing/incoming relationships
    3. Build causal chains (A -> B -> C)
    4. Return all reachable conclusions
    
    Best for: Consequences, causal chains, impact analysis
    """
    
    # Relationship types grouped by semantic meaning
    CONSEQUENCE_RELS = ['DAN_DEN', 'BI_XU_LY', 'CO_CHE_TAI', 'GAY_RA', 'PHAI']
    OBLIGATION_RELS = ['CO_NGHIA_VU', 'CHIU_TRACH_NHIEM', 'PHAI', 'BAT_BUOC']
    RIGHT_RELS = ['CO_QUYEN', 'DUOC_PHEP', 'DUOC']
    DEFINITION_RELS = ['LA_LOAI', 'THUOC', 'BAO_GOM', 'LA']
    
    def __init__(self, neo4j_driver):
        self.driver = neo4j_driver
    
    @property
    def name(self) -> str:
        return "GraphTraversal"
    
    @property
    def reasoner_type(self) -> ReasonerType:
        return ReasonerType.GRAPH_TRAVERSAL
    
    @property
    def supported_intents(self) -> List[str]:
        return ["hau_qua", "che_tai", "dinh_nghia", "nghia_vu", "quyen", "hanh_vi"]
    
    async def reason(
        self, 
        question: str, 
        intent: str, 
        entity: str,
        context: Dict[str, Any]
    ) -> ReasonerResult:
        start_time = time.time()
        
        if not self.driver:
            return self._create_result(
                success=False,
                explanation="Neo4j driver not configured",
                execution_time_ms=self._measure_time(start_time)
            )
        
        try:
            # 1. Select relationship types based on intent
            rel_types = self._get_rel_types_for_intent(intent)
            
            # 2. Find paths from entity
            paths = await self._traverse_from_entity(entity, rel_types, max_depth=3)
            
            if not paths:
                return self._create_result(
                    success=False,
                    conclusions=[],
                    explanation=f"No paths found from '{entity}'",
                    execution_time_ms=self._measure_time(start_time)
                )
            
            # 3. Extract conclusions from paths
            conclusions = []
            evidence = []
            for path in paths:
                conclusion = self._format_path_conclusion(path, intent)
                if conclusion and conclusion not in conclusions:
                    conclusions.append(conclusion)
                    evidence.append(path)
            
            # 4. Calculate confidence based on path depth and count
            confidence = min(1.0, 0.5 + len(conclusions) * 0.1)
            
            return self._create_result(
                success=True,
                conclusions=conclusions[:10],  # Limit
                evidence=evidence[:10],
                confidence=confidence,
                explanation=f"Found {len(conclusions)} paths via graph traversal",
                execution_time_ms=self._measure_time(start_time),
                metadata={"rel_types": rel_types, "path_count": len(paths)}
            )
            
        except Exception as e:
            return self._create_result(
                success=False,
                explanation=f"Graph traversal error: {str(e)}",
                execution_time_ms=self._measure_time(start_time)
            )
    
    def _get_rel_types_for_intent(self, intent: str) -> List[str]:
        """Map intent to relevant relationship types."""
        mapping = {
            "hau_qua": self.CONSEQUENCE_RELS,
            "che_tai": self.CONSEQUENCE_RELS,
            "nghia_vu": self.OBLIGATION_RELS,
            "quyen": self.RIGHT_RELS,
            "dinh_nghia": self.DEFINITION_RELS,
        }
        return mapping.get(intent, self.CONSEQUENCE_RELS + self.OBLIGATION_RELS)
    
    async def _traverse_from_entity(
        self, 
        entity: str, 
        rel_types: List[str], 
        max_depth: int = 3
    ) -> List[Dict]:
        """
        Traverse graph from entity node.
        Returns list of path dictionaries.
        """
        # Clean entity for FTS
        clean_entity = re.sub(r'[^\w\s]', '', entity).strip()
        if not clean_entity:
            return []
        
        rel_types_str = "|".join(rel_types)
        
        # Cypher query with variable-length paths
        query = f"""
        CALL db.index.fulltext.queryNodes("envLawIndex", $term) YIELD node, score
        WHERE score > 0.3
        WITH node, score
        ORDER BY score DESC
        LIMIT 3
        MATCH path = (node)-[r:{rel_types_str}*1..{max_depth}]->(target)
        RETURN 
            node.ten as start_node,
            [rel in relationships(path) | type(rel)] as rel_chain,
            [n in nodes(path) | n.ten] as node_chain,
            target.ten as end_node,
            target.noi_dung as end_content,
            labels(target) as end_labels
        LIMIT 20
        """
        
        paths = []
        try:
            async with self.driver.session() as session:
                result = await session.run(query, {"term": f"{clean_entity}*"})
                records = await result.data()
                
                for r in records:
                    paths.append({
                        "start": r["start_node"],
                        "relations": r["rel_chain"],
                        "nodes": r["node_chain"],
                        "end": r["end_node"],
                        "end_content": r["end_content"],
                        "end_labels": r["end_labels"]
                    })
        except Exception as e:
            print(f"[GraphTraversal] Query error: {e}")
        
        return paths
    
    def _format_path_conclusion(self, path: Dict, intent: str) -> str:
        """Format a path into a readable conclusion."""
        rel_chain = " → ".join(path["relations"])
        
        if intent in ["hau_qua", "che_tai"]:
            if "CheTai" in (path.get("end_labels") or []):
                return f"Chế tài: {path['end']} (từ {path['start']})"
            elif path.get("end_content"):
                return f"Hậu quả: {path['end_content']}"  # Full content
            else:
                return f"{path['start']} → {path['end']}"
        
        elif intent == "nghia_vu":
            if "QuyenNghiaVu" in (path.get("end_labels") or []):
                content = path.get("end_content") or path["end"]
                return f"Nghĩa vụ: {content}"  # Full content
        
        elif intent == "quyen":
            if path.get("end_content"):
                return f"Quyền: {path['end_content']}"  # Full content
        
        elif intent == "dinh_nghia":
            if path.get("end_content"):
                return f"{path['end']}: {path['end_content']}"  # Full content
        
        # Default format
        return f"{path['start']} -[{rel_chain}]-> {path['end']}"
