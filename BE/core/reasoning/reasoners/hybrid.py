# -*- coding: utf-8 -*-
"""
HybridReasoner - Combines KG retrieval + Rules + LLM for complex reasoning.
Best of all worlds approach.
"""
import time
from typing import Dict, Any, List
from .base_reasoner import BaseReasoner, ReasonerResult, ReasonerType


class HybridReasoner(BaseReasoner):
    """
    Hybrid Reasoner.
    
    Strategy:
    1. Retrieve relevant context from KG (via FTS)
    2. Apply rule-based reasoning
    3. Use LLM to synthesize and fill gaps
    
    Best for: Complex questions requiring multi-step reasoning
    """
    
    def __init__(self, kg_repo, llm_service, rule_engine=None):
        self.kg_repo = kg_repo
        self.llm_service = llm_service
        self.rule_engine = rule_engine
    
    @property
    def name(self) -> str:
        return "Hybrid"
    
    @property
    def reasoner_type(self) -> ReasonerType:
        return ReasonerType.HYBRID
    
    @property
    def supported_intents(self) -> List[str]:
        return ["nghia_vu", "quyen", "hau_qua", "che_tai", "dinh_nghia", "yes_no"]
    
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
            # Step 1: Retrieve KG context
            kg_context = await self._retrieve_kg_context(entity, intent)
            
            # Step 2: Apply rules if available
            rule_conclusions = []
            if self.rule_engine:
                rule_conclusions = self._apply_rules(entity, intent)
            
            # Step 3: Use LLM to synthesize
            synthesis = await self._llm_synthesize(
                question, intent, entity, kg_context, rule_conclusions
            )
            
            # Combine all
            all_conclusions = synthesis.get("conclusions", [])
            if rule_conclusions:
                all_conclusions = list(set(rule_conclusions + all_conclusions))
            
            confidence = synthesis.get("confidence", 0.7)
            
            return self._create_result(
                success=len(all_conclusions) > 0,
                conclusions=all_conclusions,
                evidence=[
                    {"type": "kg_context", "data": kg_context[:5]},
                    {"type": "rules", "data": rule_conclusions}
                ],
                confidence=confidence,
                explanation=synthesis.get("explanation", "Hybrid reasoning completed"),
                execution_time_ms=self._measure_time(start_time),
                metadata={
                    "kg_nodes_used": len(kg_context),
                    "rules_fired": len(rule_conclusions)
                }
            )
            
        except Exception as e:
            return self._create_result(
                success=False,
                explanation=f"Hybrid reasoning error: {str(e)}",
                execution_time_ms=self._measure_time(start_time)
            )
    
    async def _retrieve_kg_context(self, entity: str, intent: str) -> List[Dict]:
        """Retrieve relevant context from KG via FTS."""
        context_items = []
        
        try:
            # Search by entity
            fts_results = await self.kg_repo.search_full_text(entity, limit=3)
            
            for node, score in fts_results:
                # Get full context for each node
                node_context = await self.kg_repo.get_node_full_context(node.id)
                
                if node_context:
                    item = {
                        "name": node.name,
                        "description": node.description,
                        "score": score,
                        "relations": []
                    }
                    
                    # Add relevant relations based on intent
                    for out in node_context.get("outgoing", [])[:5]:
                        item["relations"].append({
                            "direction": "out",
                            "type": out["type"],
                            "target": out["target"],
                            "desc": out.get("target_desc", "")[:100]
                        })
                    
                    for inc in node_context.get("incoming", [])[:5]:
                        item["relations"].append({
                            "direction": "in",
                            "type": inc["type"],
                            "source": inc["source"],
                            "desc": inc.get("source_desc", "")[:100]
                        })
                    
                    context_items.append(item)
        except Exception as e:
            print(f"[Hybrid] KG retrieval error: {e}")
        
        return context_items
    
    def _apply_rules(self, entity: str, intent: str) -> List[str]:
        """Apply rule-based reasoning."""
        conclusions = []
        
        if not self.rule_engine:
            return conclusions
        
        try:
            from ..query_parser import QueryParser
            parser = QueryParser()
            facts = parser.create_facts_from_intent(intent, entity)
            
            derived = self.rule_engine.infer("forward", facts)
            
            for fact in derived:
                if fact.name in ["obligation", "authority", "consequence"]:
                    conclusions.append(fact.value)
        except Exception as e:
            print(f"[Hybrid] Rule application error: {e}")
        
        return conclusions
    
    async def _llm_synthesize(
        self, 
        question: str, 
        intent: str, 
        entity: str,
        kg_context: List[Dict],
        rule_conclusions: List[str]
    ) -> Dict:
        """Use LLM to synthesize final answer."""
        
        # Format context for LLM
        context_str = ""
        for item in kg_context[:3]:
            context_str += f"\n- {item['name']}: {item.get('description', '')[:150]}"
            for rel in item.get("relations", [])[:3]:
                context_str += f"\n  → {rel['type']}: {rel.get('target') or rel.get('source')}"
        
        rules_str = "\n".join([f"- {c}" for c in rule_conclusions]) if rule_conclusions else "(Không có)"
        
        prompt = f"""
Bạn đang hỗ trợ trả lời câu hỏi về Luật Bảo vệ Môi trường 2020.

CÂU HỎI: {question}
INTENT: {intent}
ENTITY: {entity}

DỮ LIỆU TỪ KNOWLEDGE GRAPH:
{context_str}

KẾT LUẬN TỪ RULES:
{rules_str}

Hãy tổng hợp thông tin và trả lời. Nếu cần đánh giá yes/no, hãy so sánh claim với dữ liệu.
Trả về JSON:
{{"conclusions": ["kết luận 1", "kết luận 2"], "confidence": 0.0-1.0, "explanation": "giải thích"}}
"""
        
        try:
            response = await self.llm_service.generate_response(prompt, temperature=0.1)
            
            import json
            import re
            match = re.search(r'\{.*\}', response, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except Exception as e:
            print(f"[Hybrid] LLM synthesis error: {e}")
        
        return {"conclusions": rule_conclusions, "confidence": 0.5, "explanation": "LLM synthesis failed"}
