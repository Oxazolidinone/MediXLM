# -*- coding: utf-8 -*-
"""
GraphRAGReasoner - LLM-augmented retrieval on Knowledge Graph.
Uses community detection and summarization for answering.
"""
import time
import re
from typing import Dict, Any, List
from .base_reasoner import BaseReasoner, ReasonerResult, ReasonerType


class GraphRAGReasoner(BaseReasoner):
    """
    GraphRAG Reasoner (LLM-Augmented Retrieval).
    
    Strategy:
    1. Search KG for relevant nodes via FTS
    2. Get local context (neighbors, relationships)
    3. Use LLM to generate answer based on structured context
    
    Note: This is NOT symbolic reasoning but retrieval-augmented generation.
    Best for: Fallback, exploration, open-ended questions
    """
    
    def __init__(self, kg_repo, llm_service):
        self.kg_repo = kg_repo
        self.llm_service = llm_service
    
    @property
    def name(self) -> str:
        return "GraphRAG"
    
    @property
    def reasoner_type(self) -> ReasonerType:
        return ReasonerType.GRAPHRAG
    
    @property
    def supported_intents(self) -> List[str]:
        # GraphRAG can handle all intents as fallback
        return ["dinh_nghia", "nghia_vu", "quyen", "hau_qua", "che_tai", "co_quan", "hanh_vi", "yes_no", "who"]
    
    async def reason(
        self, 
        question: str, 
        intent: str, 
        entity: str,
        context: Dict[str, Any]
    ) -> ReasonerResult:
        start_time = time.time()
        
        if not self.kg_repo or not self.llm_service:
            return self._create_result(
                success=False,
                explanation="KG repo or LLM service not configured",
                execution_time_ms=self._measure_time(start_time)
            )
        
        try:
            # Step 1: Retrieve relevant subgraph
            subgraph = await self._retrieve_subgraph(entity, question)
            
            if not subgraph:
                return self._create_result(
                    success=False,
                    conclusions=[],
                    explanation=f"No relevant information found for '{entity}'",
                    execution_time_ms=self._measure_time(start_time)
                )
            
            # Step 2: Generate answer using LLM
            llm_response = await self._generate_answer(question, intent, subgraph)
            
            return self._create_result(
                success=True,
                conclusions=[llm_response["answer"]],
                evidence=subgraph[:5],
                confidence=llm_response.get("confidence", 0.7),
                explanation="Generated via GraphRAG (LLM + KG retrieval)",
                execution_time_ms=self._measure_time(start_time),
                metadata={
                    "nodes_retrieved": len(subgraph),
                    "llm_model": "local_qwen"
                }
            )
            
        except Exception as e:
            return self._create_result(
                success=False,
                explanation=f"GraphRAG error: {str(e)}",
                execution_time_ms=self._measure_time(start_time)
            )
    
    async def _retrieve_subgraph(self, entity: str, question: str) -> List[Dict]:
        """Retrieve relevant subgraph from KG."""
        subgraph = []
        
        try:
            # Search for entity
            search_term = entity if entity else question
            fts_results = await self.kg_repo.search_full_text(search_term, limit=3)
            
            for node, score in fts_results:
                # Get full context
                node_context = await self.kg_repo.get_node_full_context(node.id)
                
                if node_context:
                    entity_obj = node_context.get("entity")
                    
                    item = {
                        "central_node": node.name,
                        "description": entity_obj.description if entity_obj else node.description,
                        "source": entity_obj.source if entity_obj else None,
                        "score": score,
                        "outgoing": [],
                        "incoming": []
                    }
                    
                    # Collect relationships
                    for out in node_context.get("outgoing", [])[:10]:  # Increased limit
                        item["outgoing"].append({
                            "relation": out["type"],
                            "target": out["target"],
                            "target_desc": out.get("target_desc", ""),  # Full content
                            "dieu_khoan": out.get("props", {}).get("dieu_khoan")
                        })
                    
                    for inc in node_context.get("incoming", [])[:10]:  # Increased limit
                        item["incoming"].append({
                            "relation": inc["type"],
                            "source": inc["source"],
                            "source_desc": inc.get("source_desc", ""),  # Full content
                            "dieu_khoan": inc.get("props", {}).get("dieu_khoan")
                        })
                    
                    subgraph.append(item)
        except Exception as e:
            print(f"[GraphRAG] Retrieve subgraph error: {e}")
        
        return subgraph
    
    async def _generate_answer(self, question: str, intent: str, subgraph: List[Dict]) -> Dict:
        """Use LLM to generate answer from subgraph."""
        
        # Format subgraph for prompt
        context_parts = []
        for item in subgraph[:5]:  # Increased from 3
            part = f"\n**{item['central_node']}**"
            if item.get("description"):
                part += f": {item['description']}"  # Full description
            if item.get("source"):
                part += f" [Căn cứ: {item['source']}]"
            
            # Add key relationships
            relations = []
            for out in item.get("outgoing", [])[:8]:  # Increased from 5
                rel_str = f"  → {out['relation']}: {out['target']}"
                if out.get("target_desc"):
                    rel_str += f" ({out['target_desc']})"  # Full content
                if out.get("dieu_khoan"):
                    rel_str += f" [Căn cứ: {out['dieu_khoan']}]"
                relations.append(rel_str)
            
            for inc in item.get("incoming", [])[:5]:
                rel_str = f"  ← {inc['source']} --[{inc['relation']}]--"
                relations.append(rel_str)
            
            if relations:
                part += "\n" + "\n".join(relations)
            
            context_parts.append(part)
        
        context_str = "\n".join(context_parts)
        
        prompt = f"""
Bạn là trợ lý pháp luật chuyên về Luật Bảo vệ Môi trường Việt Nam 2020.

DỮ LIỆU KNOWLEDGE GRAPH:
{context_str}

CÂU HỎI: {question}

YÊU CẦU:
1. Trả lời trực tiếp vào câu hỏi dựa trên dữ liệu.
2. Trích dẫn điều khoản nếu có.
3. Nếu dữ liệu không đủ, nói rõ "Dựa trên dữ liệu hiện có...".
4. KHÔNG bịa đặt thông tin ngoài dữ liệu.

TRẢ LỜI:
"""
        
        try:
            answer = await self.llm_service.generate_response(prompt, temperature=0.1)
            
            # Estimate confidence based on context quality
            confidence = 0.6
            if subgraph:
                avg_score = sum(s.get("score", 0) for s in subgraph) / len(subgraph)
                confidence = min(0.9, 0.5 + avg_score * 0.3)
            
            return {
                "answer": answer.strip(),
                "confidence": confidence
            }
        except Exception as e:
            return {
                "answer": f"Lỗi khi tạo câu trả lời: {str(e)}",
                "confidence": 0.0
            }
