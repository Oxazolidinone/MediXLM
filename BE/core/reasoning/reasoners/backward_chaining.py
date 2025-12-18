# -*- coding: utf-8 -*-
"""
BackwardChainingReasoner - Goal-driven proof-based reasoning.
Proves a goal by finding rules that conclude it and recursively proving preconditions.
"""
import time
from typing import Dict, Any, List, Optional, Set
from .base_reasoner import BaseReasoner, ReasonerResult, ReasonerType
from ..base import Fact, BaseRule


class BackwardChainingReasoner(BaseReasoner):
    """
    Backward Chaining (Goal-Driven) Reasoner.
    
    Strategy:
    1. Start with goal to prove (from question)
    2. Find rules that can conclude goal
    3. Recursively prove preconditions
    4. Return proof path
    
    Best for: Yes/No verification, compliance checking
    """
    
    def __init__(self, rule_engine=None, query_parser=None):
        self.rule_engine = rule_engine
        self.query_parser = query_parser
        self.max_depth = 10
    
    @property
    def name(self) -> str:
        return "BackwardChaining"
    
    @property
    def reasoner_type(self) -> ReasonerType:
        return ReasonerType.BACKWARD_CHAINING
    
    @property
    def supported_intents(self) -> List[str]:
        return ["yes_no", "nghia_vu", "quyen"]
    
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
            # 1. Extract goal from question/entity
            goal = self._extract_goal(intent, entity, question)
            if not goal:
                return self._create_result(
                    success=False,
                    explanation="Could not extract goal from question",
                    execution_time_ms=self._measure_time(start_time)
                )
            
            # 2. Get initial facts (known conditions)
            initial_facts = self.query_parser.create_facts_from_intent(intent, entity)
            
            # 3. Try to prove the goal
            proof_path = []
            proven = self._prove_goal(goal, set(initial_facts), self.rule_engine.rules, proof_path, 0)
            
            # 4. Build result
            if proven:
                return self._create_result(
                    success=True,
                    conclusions=[f"CÓ - {goal.value}"],
                    evidence=[{"goal": goal.value, "proven": True}],
                    confidence=0.9,
                    explanation=f"Goal proven via backward chaining",
                    proof_path=proof_path,
                    execution_time_ms=self._measure_time(start_time),
                    metadata={"goal": goal.value}
                )
            else:
                return self._create_result(
                    success=True,  # Reasoning succeeded, just couldn't prove
                    conclusions=[f"KHÔNG THỂ CHỨNG MINH - {goal.value}"],
                    evidence=[{"goal": goal.value, "proven": False}],
                    confidence=0.7,
                    explanation=f"Could not prove goal with available rules",
                    proof_path=proof_path,
                    execution_time_ms=self._measure_time(start_time),
                    metadata={"goal": goal.value}
                )
                
        except Exception as e:
            return self._create_result(
                success=False,
                explanation=f"Backward chaining error: {str(e)}",
                execution_time_ms=self._measure_time(start_time)
            )
    
    def _extract_goal(self, intent: str, entity: str, question: str) -> Optional[Fact]:
        """
        Extract the goal fact to prove from the question.
        Maps intent + entity to a provable goal.
        """
        if intent == "yes_no":
            # Goal is based on the claim in entity
            if "nghĩa vụ" in entity.lower() or "phải" in entity.lower():
                return Fact(name="obligation", value=entity)
            elif "quyền" in entity.lower() or "được" in entity.lower():
                return Fact(name="right", value=entity)
            elif "đtm" in entity.lower() or "báo cáo" in entity.lower():
                return Fact(name="obligation", value="Lập Báo cáo đánh giá tác động môi trường (ĐTM)")
            elif "gpmt" in entity.lower() or "giấy phép" in entity.lower():
                return Fact(name="obligation", value="Phải có Giấy phép môi trường")
            else:
                return Fact(name="claim", value=entity)
        
        elif intent == "nghia_vu":
            # Check if entity has specific obligations
            return Fact(name="has_obligation", value=entity)
        
        return None
    
    def _prove_goal(
        self, 
        goal: Fact, 
        known_facts: Set[Fact], 
        rules: List[BaseRule],
        proof_path: List[str],
        depth: int
    ) -> bool:
        """
        Recursively prove a goal using backward chaining.
        """
        if depth > self.max_depth:
            proof_path.append(f"[MAX_DEPTH] Stopped at depth {depth}")
            return False
        
        # Check if goal already known
        for fact in known_facts:
            if fact.name == goal.name and self._values_match(fact.value, goal.value):
                proof_path.append(f"[FACT] Found: {goal.value}")
                return True
        
        # Find rules that can conclude this goal
        for rule in rules:
            # Check if rule's execute could produce this goal
            # This requires checking the rule's conclusion type
            if self._rule_can_conclude(rule, goal):
                proof_path.append(f"[RULE] Trying: {rule.name}")
                
                # Get preconditions the rule needs
                preconditions = self._get_rule_preconditions(rule)
                
                # Try to prove all preconditions
                all_proven = True
                for precond in preconditions:
                    if precond not in known_facts:
                        if not self._prove_goal(precond, known_facts, rules, proof_path, depth + 1):
                            all_proven = False
                            break
                
                if all_proven:
                    # Rule fires - derive the conclusion
                    proof_path.append(f"[DERIVED] Via {rule.name}: {goal.value}")
                    return True
        
        proof_path.append(f"[FAILED] Could not prove: {goal.value}")
        return False
    
    def _values_match(self, v1: Any, v2: Any) -> bool:
        """Fuzzy match for fact values."""
        if v1 == v2:
            return True
        s1, s2 = str(v1).lower(), str(v2).lower()
        return s1 in s2 or s2 in s1
    
    def _rule_can_conclude(self, rule: BaseRule, goal: Fact) -> bool:
        """
        Check if a rule can conclude the given goal.
        This is a heuristic based on rule name/description.
        """
        rule_name = rule.name.lower()
        goal_value = str(goal.value).lower()
        
        # Map rule types to conclusion types
        if "obl" in rule_name and goal.name == "obligation":
            return True
        if "auth" in rule_name and goal.name == "authority":
            return True
        if "cons" in rule_name and goal.name == "consequence":
            return True
        if "exempt" in rule_name and goal.name == "exemption":
            return True
        
        # Check description
        if hasattr(rule, 'description') and goal_value in rule.description.lower():
            return True
            
        return False
    
    def _get_rule_preconditions(self, rule: BaseRule) -> List[Fact]:
        """
        Extract preconditions needed for a rule.
        This is based on rule name/type heuristics.
        """
        rule_name = rule.name.upper()
        
        # Map specific rules to their known preconditions
        precondition_map = {
            "OBL_001": [Fact(name="project_group", value="I")],  # PEIA Rule
            "OBL_002": [Fact(name="project_group", value="I")],  # DTM Rule
            "OBL_003": [Fact(name="project_group", value="I")],  # GPMT Rule
            "AUTH_001": [Fact(name="project_group", value="I")],
            "CONS_001": [Fact(name="action", value="xả thải trái phép")],
        }
        
        return precondition_map.get(rule_name, [])
