from typing import List, Dict, Any
import re
from .base import Fact

class QueryParser:
    """
    Parses natural language queries into Facts for the Reasoning Engine.
    In a real system, this would use an LLM or NLU service.
    For this demo, we use simple keyword matching and Regex.
    """
    
    def parse(self, query: str) -> List[Fact]:
        facts = []
        q = query.lower()
        
        # 1. Project Group detection
        if "nhóm i" in q or "nhom i" in q:
            facts.append(Fact(name="project_group", value="I"))
        elif "nhóm ii" in q or "nhom ii" in q:
            facts.append(Fact(name="project_group", value="II"))
        elif "nhóm iii" in q or "nhom iii" in q:
            facts.append(Fact(name="project_group", value="III"))
            
        # 2. Action / Behavior detection
        if "xả thải" in q:
            if "trái phép" in q or "vượt" in q:
                 facts.append(Fact(name="action", value="xả thải trái phép"))
            else:
                 facts.append(Fact(name="event", value="xả thải"))
                 
        if "ô nhiễm" in q:
            facts.append(Fact(name="event", value="ô nhiễm môi trường"))
            
        if "thẩm định" in q and "đtm" in q:
            facts.append(Fact(name="action", value="thẩm định ĐTM"))
            
        return facts

    def create_facts_from_intent(self, intent: str, entity: str) -> List[Fact]:
        """
        Create facts generic to the intent/entity extracted by NLU/Regex.
        This bridges the gap between the Service's intent detection and Rule Engine.
        """
        facts = []
        e_lower = entity.lower().strip()
        
        # 1. Project Group/Type Facts
        if "nhóm i" in e_lower or "nhom i" in e_lower:
            facts.append(Fact(name="project_group", value="I"))
        elif "nhóm ii" in e_lower or "nhom ii" in e_lower:
            facts.append(Fact(name="project_group", value="II"))
        elif "nhóm iii" in e_lower or "nhom iii" in e_lower:
            facts.append(Fact(name="project_group", value="III"))
        elif "nhóm iv" in e_lower or "nhom iv" in e_lower:
             facts.append(Fact(name="project_group", value="IV"))
             
        # 2. Action Facts (for Consequences/Exemptions)
        if intent in ["che_tai", "hau_qua", "hanh_vi"]:
            facts.append(Fact(name="action", value=entity))
            # Heuristics for specific known actions
            if "xả thải" in e_lower:
                 if "trái phép" in e_lower or "vượt" in e_lower or "không phép" in e_lower:
                      facts.append(Fact(name="action", value="xả thải trái phép"))
                      
            if "không" in e_lower and "gpmt" in e_lower:
                 facts.append(Fact(name="action", value="không có giấy phép môi trường"))

        # 3. Time/Deadline Facts
        if intent == "thoi_han":
             facts.append(Fact(name="request", value="thời hạn"))
             if "thẩm định" in e_lower: facts.append(Fact(name="context", value="thẩm định"))
             if "cấp phép" in e_lower: facts.append(Fact(name="context", value="cấp phép"))

        # 4. Authority Facts
        if intent == "co_quan":
             facts.append(Fact(name="request", value="thẩm quyền"))
             
        # 5. Generic Context Fact
        # If we didn't extract specific facts, create a generic one so rules MIGHT match fuzzily
        if not facts:
             facts.append(Fact(name="context", value=entity))
             
        return facts
