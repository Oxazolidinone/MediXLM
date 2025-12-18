import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

# Add BE to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.reasoning import RuleEngine, Fact, ForwardChainingEngine
from core.reasoning.rules.obligation_rules import PEIARule, DTMRule, GPMTRule
from core.reasoning.rules.time_rules import TimeDTMRule

def main():
    print("=== DEMO: REASONING ENGINE INDEPENDENT TEST ===")
    
    # 1. Setup Engine
    engine = RuleEngine()
    engine.register_strategy("forward", ForwardChainingEngine())
    
    # Add rules manually for transparent demo
    engine.add_rule(PEIARule())
    engine.add_rule(DTMRule())
    engine.add_rule(TimeDTMRule())
    
    # 2. Define Input Facts (Simulating "Dự án Nhóm I")
    print("\n[INPUT] Fact: Project Group = I")
    initial_facts = [
        Fact(name="project_group", value="I"),
        Fact(name="action", value="thẩm định ĐTM") # To trigger time rule
    ]
    
    # 3. Run Inference
    print("[LOGIC] Running Forward Chaining...")
    results = engine.infer("forward", initial_facts)
    
    # 4. Show Results
    print(f"\n[OUTPUT] Derived {len(results)} new facts:")
    for f in results:
        if f in initial_facts: continue # Skip inputs
        print(f"  + [{f.name.upper()}] {f.value}")
        if f.metadata:
            print(f"    Context: {f.metadata}")
            
    print("\n=== CONCLUSION ===")
    if len(results) > len(initial_facts):
        print("SUCCESS: The engine successfully derived new legal obligations from raw facts.")
    else:
        print("FAILURE: No new facts derived.")

if __name__ == "__main__":
    main()
