"""Knowledge Graph repository implementation using Neo4j for Environmental Law."""
from typing import List, Optional, Dict, Any, Tuple
from neo4j import AsyncDriver
import re

from domain.entities.env_law_knowledge import EnvLawKnowledge, KnowledgeType
from domain.repositories.knowledge_graph_repository import IKnowledgeGraphRepository


class KnowledgeGraphRepositoryImpl(IKnowledgeGraphRepository):
    def __init__(self, driver: AsyncDriver):
        self.driver = driver

    async def get_node_by_id(self, node_id: str) -> Optional[EnvLawKnowledge]:
        query = """
        MATCH (n)
        WHERE n.id = $id
        RETURN n, labels(n) as labels
        """
        async with self.driver.session() as session:
            result = await session.run(query, id=str(node_id))
            record = await result.single()

            if record:
                return self._to_entity(record["n"], record["labels"])
            return None

    async def search_full_text(self, query: str, limit: int = 10) -> List[Tuple[EnvLawKnowledge, float]]:
        """Search using Full Text Index."""
        # Clean query for FTS lucene syntax if needed, simple approach for now
        # Escape special characters or just use standard text search
        # Using ~ for fuzzy search or wildcard * might be needed
        clean_query = re.sub(r'[^\w\s]', '', query)
        if not clean_query.strip():
            return []
            
        fts_query = f"{clean_query}*" 
        
        cypher = """
        CALL db.index.fulltext.queryNodes("envLawIndex", $search_term, {limit: $limit})
        YIELD node, score
        RETURN node, score, labels(node) as labels
        """
        
        async with self.driver.session() as session:
            result = await session.run(cypher, search_term=fts_query, limit=limit)
            records = await result.values()
            
            return [(self._to_entity(record[0], record[2]), record[1]) for record in records]

    async def search_by_name(self, name: str, knowledge_type: Optional[KnowledgeType] = None) -> List[EnvLawKnowledge]:
        if knowledge_type:
            query = """
            MATCH (n)
            WHERE toLower(n.ten) CONTAINS toLower($name) AND $label IN labels(n)
            RETURN n, labels(n) as labels
            LIMIT 20
            """
            params = {"name": name, "label": knowledge_type.value}
        else:
            query = """
            MATCH (n)
            WHERE toLower(n.ten) CONTAINS toLower($name)
            RETURN n, labels(n) as labels
            LIMIT 20
            """
            params = {"name": name}

        async with self.driver.session() as session:
            result = await session.run(query, **params)
            records = await result.values()

            return [self._to_entity(record[0], record[1]) for record in records]
            
    async def get_node_full_context(self, node_id: str) -> Dict[str, Any]:
        """
        Fetch the node and ALL its relationships (incoming and outgoing).
        """
        query = """
        MATCH (n) 
        WHERE n.id = $id OR elementId(n) = $id OR toString(id(n)) = $id
        OPTIONAL MATCH (n)-[r_out]->(target)
        OPTIONAL MATCH (source)-[r_in]->(n)
        RETURN n, labels(n) as labels,
               collect(DISTINCT {
                   type: type(r_out), 
                   target: target.ten, 
                   target_desc: coalesce(target.mo_ta, target.noi_dung, ""),
                   target_label: labels(target)[0], 
                   props: properties(r_out)
               }) as outgoing,
               collect(DISTINCT {
                   type: type(r_in), 
                   source: source.ten, 
                   source_desc: coalesce(source.mo_ta, source.noi_dung, ""),
                   source_label: labels(source)[0], 
                   props: properties(r_in)
               }) as incoming
        """
        async with self.driver.session() as session:
            result = await session.run(query, id=str(node_id))
            record = await result.single()
            
            if not record:
                return {}
            
            # Reconstruct node object
            node_entity = self._to_entity(record["n"], record["labels"])
            
            return {
                "entity": node_entity,
                "outgoing": [r for r in record["outgoing"] if r['type'] is not None], # Filter out nulls from OPTIONAL MATCH
                "incoming": [r for r in record["incoming"] if r['type'] is not None]
            }

    async def get_related_nodes(self, node_id: str, relationship_type: Optional[str] = None, depth: int = 1) -> List[EnvLawKnowledge]:
        if relationship_type:
            query = """
            MATCH (n {id: $id})-[r:%s*1..%d]-(related)
            RETURN DISTINCT related, labels(related) as labels
            """ % (relationship_type, depth)
        else:
            query = """
            MATCH (n {id: $id})-[*1..%d]-(related)
            RETURN DISTINCT related, labels(related) as labels
            """ % depth

        async with self.driver.session() as session:
            result = await session.run(query, id=str(node_id))
            records = await result.values()

            return [self._to_entity(record[0], record[1]) for record in records]

    # --- Specific Env Law Queries (Ported from chatbot_v2.py) ---

    async def get_obligations(self, subject: str) -> List[Dict[str, Any]]:
        # 1. DoiTuong - CO_NGHIA_VU -> QuyenNghiaVu -> QUY_DINH_TAI -> DieuLuat
        query_doituong = """
        MATCH (d:DoiTuong)-[r:CO_NGHIA_VU]->(q:QuyenNghiaVu)
        WHERE toLower(d.ten) CONTAINS toLower($subject)
        OPTIONAL MATCH (q)-[:QUY_DINH_TAI]->(dl:DieuLuat)
        RETURN d.ten AS chu_the,
               q.noi_dung AS nghia_vu,
               q.loai AS loai_nghia_vu,
               q.id AS doi_tuong,
               COALESCE(dl.ten, q.dieu_khoan, '') AS dieu_khoan,
               q.pham_vi AS pham_vi,
               "nghia_vu_doi_tuong" as source_type
        LIMIT 25
        """
        
        # 2. CoQuan - CHIU_TRACH_NHIEM -> TrachNhiem -> QUY_DINH_TAI -> DieuLuat
        query_coquan = """
        MATCH (c:CoQuan)-[r:CHIU_TRACH_NHIEM]->(tn:TrachNhiem)
        WHERE toLower(c.ten) CONTAINS toLower($subject)
           OR ($subject IN ['Chính phủ', 'nhà nước', 'nha nuoc'] AND c.ten = 'Chính phủ')
        OPTIONAL MATCH (tn)-[:QUY_DINH_TAI]->(dl:DieuLuat)
        RETURN c.ten AS chu_the,
               tn.noi_dung AS nghia_vu,
               tn.ten AS ten_trach_nhiem,
               "Trách nhiệm nhà nước" AS loai_trach_nhiem,
               COALESCE(dl.ten, tn.dieu_khoan, '') AS dieu_khoan,
               "trach_nhiem_co_quan" as source_type
        LIMIT 25
        """
        
        results = []
        async with self.driver.session() as session:
            # Map "nhà nước" to "Chính phủ" done in query parameter or python logic
            search_subject = "Chính phủ" if subject.lower() in ["nhà nước", "nha nuoc"] else subject
            
            res1 = await session.run(query_doituong, {"subject": search_subject})
            results.extend(await res1.data())
            
            res2 = await session.run(query_coquan, {"subject": search_subject})
            results.extend(await res2.data())
            
        return results

    async def get_rights(self, subject: str) -> List[Dict[str, Any]]:
        query = """
        MATCH (d:DoiTuong)-[r:CO_QUYEN]->(q:QuyenNghiaVu)
        WHERE toLower(d.ten) CONTAINS toLower($subject)
        RETURN d.ten AS chu_the,
               q.noi_dung AS quyen,
               q.loai AS loai_quyen,
               q.id AS doi_tuong,
               q.dieu_khoan AS dieu_khoan
        LIMIT 15
        """
        async with self.driver.session() as session:
            result = await session.run(query, {"subject": subject})
            return await result.data()


    async def get_consequences(self, action: str) -> List[Dict[str, Any]]:
        query = """
        MATCH (h:HanhVi)
        WHERE toLower(h.ten) CONTAINS toLower($term)
           OR toLower(h.noi_dung) CONTAINS toLower($term)
        RETURN h.ten AS hanh_vi, 
               h.noi_dung AS noi_dung_hanh_vi, 
               h.che_tai AS che_tai, 
               "N/A" AS dieu_khoan
        LIMIT 10
        """
        async with self.driver.session() as session:
            result = await session.run(query, {"term": action})
            return await result.data()

    async def get_agencies(self) -> List[EnvLawKnowledge]:
        query = """
        MATCH (cq:CoQuan)
        RETURN cq, labels(cq) as labels
        ORDER BY CASE cq.cap
            WHEN 'trung_uong' THEN 1
            WHEN 'tinh' THEN 2
            WHEN 'huyen' THEN 3
            WHEN 'xa' THEN 4
            ELSE 5 END
        """
        async with self.driver.session() as session:
            result = await session.run(query)
            records = await result.values()
            return [self._to_entity(record[0], record[1]) for record in records]

    async def get_all_by_type(self, knowledge_type: KnowledgeType) -> List[EnvLawKnowledge]:
        query = """
        MATCH (n)
        WHERE $label IN labels(n)
        RETURN n, labels(n) as labels
        ORDER BY n.id
        """
        async with self.driver.session() as session:
            result = await session.run(query, label=knowledge_type.value)
            records = await result.values()
            return [self._to_entity(record[0], record[1]) for record in records]

    @staticmethod
    def _to_entity(node, labels) -> EnvLawKnowledge:
        # Determine KnowledgeType from labels
        # Assuming one main label from our enum maps to KnowledgeType
        # If multiple, pick the first valid one
        k_type = KnowledgeType.KHAI_NIEM # Default
        for label in labels:
            try:
                # Map old/new labels to Enum
                # Check directly if label is in KnowledgeType values
                # KnowledgeType is string Enum, so we can cast
                # But 'ChuThe' might exist in old data, new is 'DoiTuong'
                k_type = KnowledgeType(label)
                break
            except ValueError:
                continue
                
        # Map props
        props = dict(node)
        
        return EnvLawKnowledge(
            id=props.get("id", str(node.id)),
            name=props.get("ten", "Unknown"),
            knowledge_type=k_type,
            description=props.get("mo_ta") or props.get("noi_dung"),
            source=props.get("dieu_khoan"),
            properties=props
        )
