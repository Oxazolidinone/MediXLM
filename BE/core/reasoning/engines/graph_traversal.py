from typing import List, Dict, Any
from ..base import InferenceEngine, Fact, BaseRule

class GraphTraversalEngine(InferenceEngine):
    """
    Graph-Based Reasoning: Traverse nodes and relationships to find connections.
    Includes algorithms like BFS for causal chains.
    """
    def __init__(self, neo4j_driver):
        self.driver = neo4j_driver

    async def arun(self, initial_facts: List[Fact], rules: List[BaseRule]) -> List[Fact]:
        results = []
        for fact in initial_facts:
            # Trigger traversal if we have a starting point and a direction hint
            # Heuristic: If we have an "event" or "action", trace consequences
            if fact.name in ["event", "action"]:
                start_node = fact.value
                # Try to find consequences in graph
                traversal_res = await self._traverse_consequences(start_node)
                results.extend(traversal_res)
        return results

    async def _traverse_consequences(self, start_term: str) -> List[Fact]:
        if not self.driver: return []
        
        # Use FTS to find starting nodes specifically using the global index
        # This aligns with "All reasoning uses FTS" requirement
        # Clean term for Lucene
        import re
        clean_term = re.sub(r'[^\w\s]', '', start_term).strip()
        if not clean_term: return []
        search_query = f"{clean_term}*" # Simple prefix search
        
        # Cypher: FTS Index Scan -> Traverse relationships
        query = """
        CALL db.index.fulltext.queryNodes("envLawIndex", $term) YIELD node, score
        MATCH (node)-[r:DAN_DEN|BI_XU_LY]->(target)
        WHERE score > 0.5  /* Basic threshold */
        RETURN node.ten as hanh_vi, type(r) as rel, target.ten as target, labels(target) as labels
        LIMIT 5
        """
        
        derived = []
        try:
            async with self.driver.session() as session:
                result = await session.run(query, term=search_query)
                records = await result.values()
                
                for r in records:
                    hanh_vi, rel, target, labels = r
                    if "CheTai" in labels:
                        derived.append(Fact(name="consequence", value=f"Bị {target}", metadata={"source_action": hanh_vi, "type": "che_tai"}))
                    elif "HauQua" in labels:
                        derived.append(Fact(name="consequence", value=f"Gây ra {target}", metadata={"source_action": hanh_vi, "type": "hau_qua"}))
        except Exception as e:
            print(f"GraphTraversal Error: {e}")
            
        return derived
