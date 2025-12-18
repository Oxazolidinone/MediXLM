# -*- coding: utf-8 -*-
"""
OntologyReasoner - OWL-RL style reasoning on Knowledge Graph.
Handles class hierarchy, subsumption, and transitive inference.
"""
import time
import re
from typing import Dict, Any, List, Set
from .base_reasoner import BaseReasoner, ReasonerResult, ReasonerType


class OntologyReasoner(BaseReasoner):
    """
    Ontology Reasoner (OWL-RL Style).
    
    Strategy:
    1. Infer class hierarchy via LA_LOAI, THUOC relationships
    2. Apply transitivity rules
    3. Infer subsumption (subclass relationships)
    4. Propagate properties along hierarchy
    
    Best for: Definitions, classification, hierarchical queries
    """
    
    # Relationship types indicating class hierarchy
    HIERARCHY_RELS = ['LA_LOAI', 'THUOC', 'LA', 'BAO_GOM']
    
    def __init__(self, neo4j_driver):
        self.driver = neo4j_driver
    
    @property
    def name(self) -> str:
        return "Ontology"
    
    @property
    def reasoner_type(self) -> ReasonerType:
        return ReasonerType.ONTOLOGY
    
    @property
    def supported_intents(self) -> List[str]:
        return ["dinh_nghia", "nghia_vu", "quyen", "yes_no"]
    
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
            conclusions = []
            evidence = []
            
            # 1. Get class hierarchy (superclasses)
            superclasses = await self._get_superclasses(entity)
            if superclasses:
                conclusions.append(f"'{entity}' thuộc các phân loại: {', '.join(superclasses)}")
                evidence.append({"type": "hierarchy", "superclasses": superclasses})
            
            # 2. Get subclasses (instances/specializations)
            subclasses = await self._get_subclasses(entity)
            if subclasses:
                conclusions.append(f"'{entity}' bao gồm: {', '.join(subclasses[:5])}")
                evidence.append({"type": "subclasses", "items": subclasses})
            
            # 3. Get definition with inferred properties
            definition = await self._get_definition_with_inference(entity)
            if definition:
                conclusions.append(definition["text"])
                evidence.append({"type": "definition", "data": definition})
            
            # 4. Get inherited obligations/rights from superclasses
            if intent in ["nghia_vu", "quyen"]:
                inherited = await self._get_inherited_properties(entity, superclasses, intent)
                for item in inherited:
                    conclusions.append(item["text"])
                    evidence.append(item)
            
            confidence = min(1.0, 0.4 + len(conclusions) * 0.15)
            
            return self._create_result(
                success=len(conclusions) > 0,
                conclusions=conclusions,
                evidence=evidence,
                confidence=confidence,
                explanation=f"Ontology reasoning: found {len(superclasses)} superclasses, {len(subclasses)} subclasses",
                execution_time_ms=self._measure_time(start_time),
                metadata={
                    "superclasses": superclasses,
                    "subclasses": subclasses
                }
            )
            
        except Exception as e:
            return self._create_result(
                success=False,
                explanation=f"Ontology reasoning error: {str(e)}",
                execution_time_ms=self._measure_time(start_time)
            )
    
    async def _get_superclasses(self, entity: str) -> List[str]:
        """Get all superclasses via transitive closure."""
        clean_entity = re.sub(r'[^\w\s]', '', entity).strip()
        if not clean_entity:
            return []
        
        rel_types_str = "|".join(self.HIERARCHY_RELS)
        query = f"""
        CALL db.index.fulltext.queryNodes("envLawIndex", $term) YIELD node, score
        WHERE score > 0.5
        WITH node
        LIMIT 1
        MATCH path = (node)-[:{rel_types_str}*1..5]->(parent)
        RETURN DISTINCT parent.ten as parent_name
        """
        
        parents = []
        try:
            async with self.driver.session() as session:
                result = await session.run(query, {"term": f"{clean_entity}*"})
                records = await result.data()
                parents = [r["parent_name"] for r in records if r["parent_name"]]
        except Exception as e:
            print(f"[Ontology] Get superclasses error: {e}")
        
        return parents
    
    async def _get_subclasses(self, entity: str) -> List[str]:
        """Get all subclasses/instances."""
        clean_entity = re.sub(r'[^\w\s]', '', entity).strip()
        if not clean_entity:
            return []
        
        rel_types_str = "|".join(self.HIERARCHY_RELS)
        query = f"""
        CALL db.index.fulltext.queryNodes("envLawIndex", $term) YIELD node, score
        WHERE score > 0.5
        WITH node
        LIMIT 1
        MATCH (child)-[:{rel_types_str}*1..3]->(node)
        RETURN DISTINCT child.ten as child_name
        LIMIT 10
        """
        
        children = []
        try:
            async with self.driver.session() as session:
                result = await session.run(query, {"term": f"{clean_entity}*"})
                records = await result.data()
                children = [r["child_name"] for r in records if r["child_name"]]
        except Exception as e:
            print(f"[Ontology] Get subclasses error: {e}")
        
        return children
    
    async def _get_definition_with_inference(self, entity: str) -> Dict:
        """Get definition with properties from hierarchy."""
        clean_entity = re.sub(r'[^\w\s]', '', entity).strip()
        if not clean_entity:
            return {}
        
        query = """
        CALL db.index.fulltext.queryNodes("envLawIndex", $term) YIELD node, score
        WHERE score > 0.5
        WITH node
        LIMIT 1
        OPTIONAL MATCH (node)-[:QUY_DINH_TAI]->(dl:DieuLuat)
        RETURN node.ten as name, 
               node.noi_dung as definition,
               labels(node) as labels,
               dl.ten as source
        """
        
        try:
            async with self.driver.session() as session:
                result = await session.run(query, {"term": f"{clean_entity}*"})
                record = await result.single()
                
                if record:
                    name = record["name"] or entity
                    definition = record["definition"] or "Chưa có định nghĩa chi tiết"
                    source = record["source"]
                    labels = record["labels"] or []
                    
                    text = f"**{name}**: {definition}"
                    if source:
                        text += f" [Căn cứ: {source}]"
                    
                    return {
                        "text": text,
                        "name": name,
                        "definition": definition,
                        "source": source,
                        "labels": labels
                    }
        except Exception as e:
            print(f"[Ontology] Get definition error: {e}")
        
        return {}
    
    async def _get_inherited_properties(
        self, 
        entity: str, 
        superclasses: List[str],
        intent: str
    ) -> List[Dict]:
        """Get obligations/rights inherited from superclasses."""
        if not superclasses:
            return []
        
        rel_type = "CO_NGHIA_VU" if intent == "nghia_vu" else "CO_QUYEN"
        prop_name = "nghĩa vụ" if intent == "nghia_vu" else "quyền"
        
        inherited = []
        try:
            async with self.driver.session() as session:
                for superclass in superclasses[:3]:  # Limit to avoid too many queries
                    query = f"""
                    MATCH (d)-[:{rel_type}]->(q)
                    WHERE toLower(d.ten) CONTAINS toLower($name)
                    RETURN d.ten as subject, q.noi_dung as content
                    LIMIT 3
                    """
                    result = await session.run(query, {"name": superclass})
                    records = await result.data()
                    
                    for r in records:
                        inherited.append({
                            "text": f"(Kế thừa từ {superclass}) {prop_name}: {r['content'][:100]}",
                            "type": "inherited",
                            "from_class": superclass,
                            "content": r["content"]
                        })
        except Exception as e:
            print(f"[Ontology] Get inherited properties error: {e}")
        
        return inherited
