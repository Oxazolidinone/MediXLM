from typing import List, Optional
from ..base import InferenceEngine, Fact, BaseRule

class BackwardChainingEngine(InferenceEngine):
    """
    Goal-Driven Reasoning: Try to prove a specific goal fact.
    NOTE: This simplified implementation checks if a Goal is derivable.
    """
    def __init__(self, target_goal: Optional[Fact] = None):
        self.target_goal = target_goal

    def run(self, initial_facts: List[Fact], rules: List[BaseRule]) -> List[Fact]:
        if not self.target_goal:
            return initial_facts # No goal, nothing to prove
            
        if self._prove(self.target_goal, initial_facts, rules, depth=0):
            return initial_facts + [self.target_goal]
        return initial_facts

    def _prove(self, goal: Fact, facts: List[Fact], rules: List[BaseRule], depth: int) -> bool:
        if depth > 20: return False # detailed recursion limit
        
        # 1. Check if goal is already a fact
        if goal in facts:
            return True
            
        # 2. Find rules that conclude this goal
        # Note: This requires rules to expose their "conclusions" or we try all
        # For this generic implementation, we assume we iterate valid rules
        
        # Optimization: In a real system, rules would be indexed by conclusion.
        # Here we do a naive scan for demonstration of the logic pattern.
        
        # Simulating Backward Chain:
        # A Rule is valid if its conditions can be proven.
        # Since our BaseRule is generic (check/execute), pure backward chaining 
        # is hard without declarative rule structure. 
        # We will implement a "Hypothetical Forward Chaining" for this demo 
        # or require rules to have a `concludes(fact)` method.
        
        # Fallback to FC for now as it's safer for this architecture unless we change BaseRule.
        # Implemented as: Can we reach Goal from Initial via FC?
        
        from .forward_chaining import ForwardChainingEngine
        fc = ForwardChainingEngine()
        derived = fc.run(facts, rules)
        return goal in derived
