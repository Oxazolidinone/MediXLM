# -*- coding: utf-8 -*-
"""
ForwardChainingReasoner - Data-driven rule-based reasoning.
Fires rules until no more facts can be derived.
"""
import time
from typing import Dict, Any, List
from .base_reasoner import BaseReasoner, ReasonerResult, ReasonerType
from ..base import Fact


class ForwardChainingReasoner(BaseReasoner):
    """
    Forward Chaining (Data-Driven) Reasoner.
    
    Strategy:
    1. Start with known facts
    2. Fire all applicable rules
    3. Add derived facts to working memory
    4. Repeat until no new facts
    
    Best for: Deriving all obligations/rights from known conditions
    """
    
    def __init__(self, rule_engine=None, query_parser=None):
        self.rule_engine = rule_engine
        self.query_parser = query_parser
    
    @property
    def name(self) -> str:
        return "ForwardChaining"
    
    @property
    def reasoner_type(self) -> ReasonerType:
        return ReasonerType.FORWARD_CHAINING
    
    @property
    def supported_intents(self) -> List[str]:
        return ["nghia_vu", "quyen", "thoi_han", "che_tai", "hau_qua", "hanh_vi"]
    
    async def reason(
        self, 
        question: str, 
        intent: str, 
        entity: str,
        context: Dict[str, Any]
    ) -> ReasonerResult:
        start_time = time.time()
        
        if not self.rule_engine or not self.query_parser:
            return self._create_result(
                success=False,
                explanation="Rule engine not configured",
                execution_time_ms=self._measure_time(start_time)
            )
        
        try:
            # 1. Create initial facts from intent/entity
            initial_facts = self.query_parser.create_facts_from_intent(intent, entity)
            if not initial_facts:
                return self._create_result(
                    success=False,
                    explanation=f"Could not create facts from entity: {entity}",
                    execution_time_ms=self._measure_time(start_time)
                )
            
            # 2. Run forward chaining
            derived_facts = self.rule_engine.infer("forward", initial_facts)
            
            # 3. Filter relevant conclusions (not the initial facts)
            conclusions = []
            evidence = []
            for fact in derived_facts:
                if fact not in initial_facts:
                    if fact.name in ["obligation", "authority", "consequence", "deadline", "exemption"]:
                        conclusions.append(fact.value)
                        evidence.append({
                            "type": fact.name,
                            "value": fact.value,
                            "source": fact.metadata.get("source") if fact.metadata else None
                        })
            
            # 4. Calculate confidence
            confidence = min(1.0, len(conclusions) * 0.2 + 0.3) if conclusions else 0.0
            
            return self._create_result(
                success=len(conclusions) > 0,
                conclusions=conclusions,
                evidence=evidence,
                confidence=confidence,
                explanation=f"Derived {len(conclusions)} conclusions from {len(initial_facts)} initial facts using forward chaining.",
                execution_time_ms=self._measure_time(start_time),
                metadata={"initial_facts": [f.value for f in initial_facts]}
            )
            
        except Exception as e:
            return self._create_result(
                success=False,
                explanation=f"Forward chaining error: {str(e)}",
                execution_time_ms=self._measure_time(start_time)
            )
