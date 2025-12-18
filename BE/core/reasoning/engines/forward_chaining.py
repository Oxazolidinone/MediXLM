from typing import List
from ..base import InferenceEngine, Fact, BaseRule

class ForwardChainingEngine(InferenceEngine):
    """
    Data-Driven Reasoning: Start with known facts and assert new facts
    until no more rules can be applied.
    """
    def run(self, initial_facts: List[Fact], rules: List[BaseRule]) -> List[Fact]:
        working_memory = set(initial_facts)  # Use set for uniqueness
        new_facts_added = True
        
        iteration = 0
        MAX_ITERATIONS = 100 # Prevent infinite loops
        
        while new_facts_added and iteration < MAX_ITERATIONS:
            new_facts_added = False
            current_facts_list = list(working_memory)
            
            for rule in rules:
                if rule.check(current_facts_list):
                    derived_facts = rule.execute(current_facts_list)
                    for fact in derived_facts:
                        if fact not in working_memory:
                            working_memory.add(fact)
                            new_facts_added = True
            
            iteration += 1
            
        return list(working_memory)
