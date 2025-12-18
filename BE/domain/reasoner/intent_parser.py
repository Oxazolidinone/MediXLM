"""Intent parser - Parse user questions to extract intent and entities."""
import re
from typing import Dict, Any, Tuple, Optional
from enum import Enum


class Intent(Enum):
    """Supported query intents."""
    DEFINITION = "definition"       # "X là gì?"
    OBLIGATION = "obligation"       # "Nghĩa vụ của X?"
    PROCEDURE = "procedure"         # "Thủ tục cho X?"
    CONSEQUENCE = "consequence"     # "Hậu quả của X?"
    AUTHORITY = "authority"         # "Ai có thẩm quyền?"
    GENERAL = "general"             # General questions


class IntentParser:
    """Parse user questions to determine intent and extract entities."""
    
    # Intent patterns (Vietnamese)
    PATTERNS = {
        Intent.DEFINITION: [
            r"(.+?)\s*là\s*gì",
            r"định\s*nghĩa\s*(.+)",
            r"(.*?)\s*có\s*nghĩa\s*là",
            r"giải\s*thích\s*(.+)",
            r"(.+?)\s*được\s*hiểu\s*như\s*thế\s*nào",
        ],
        Intent.OBLIGATION: [
            r"nghĩa\s*vụ\s*(?:của\s*)?(.+)",
            r"(.+?)\s*(?:cần|phải)\s*làm\s*gì",
            r"(.+?)\s*có\s*(?:những\s*)?nghĩa\s*vụ",
            r"trách\s*nhiệm\s*(?:của\s*)?(.+)",
            r"(.+?)\s*(?:bắt\s*buộc|yêu\s*cầu)",
        ],
        Intent.PROCEDURE: [
            r"thủ\s*tục\s*(?:cho|của)?\s*(.+)",
            r"(.+?)\s*cần\s*(?:những\s*)?thủ\s*tục",
            r"quy\s*trình\s*(.+)",
            r"(.+?)\s*(?:phải|cần)\s*(?:đăng\s*ký|xin\s*phép)",
            r"hồ\s*sơ\s*(.+)",
            r"(.+?)\s*(?:được|phải)\s*(?:thực\s*hiện|tiến\s*hành)\s*như\s*thế\s*nào",
        ],
        Intent.CONSEQUENCE: [
            r"(?:hậu\s*quả|xử\s*lý|xử\s*phạt)\s*(?:của|khi|nếu)?\s*(.+)",
            r"(.+?)\s*(?:bị|sẽ)\s*(?:xử\s*lý|xử\s*phạt)",
            r"(.+?)\s*(?:bị|sẽ)\s*(?:như\s*thế\s*nào|ra\s*sao)",
            r"vi\s*phạm\s*(.+?)\s*(?:bị|thì)",
            r"(.+?)\s*(?:trái\s*(?:phép|quy\s*định))",
            r"chế\s*tài\s*(.+)",
        ],
        Intent.AUTHORITY: [
            r"(?:ai|cơ\s*quan\s*nào)\s*(?:có\s*)?thẩm\s*quyền\s*(.+)",
            r"thẩm\s*quyền\s*(.+)",
            r"(?:ai|cơ\s*quan\s*nào)\s*cấp\s*(.+)",
            r"(.+?)\s*(?:do|thuộc)\s*(?:ai|cơ\s*quan\s*nào)",
            r"(?:ai|cơ\s*quan\s*nào)\s*(?:phê\s*duyệt|thẩm\s*định)\s*(.+)",
        ],
    }
    
    # Keywords for entity extraction
    SUBJECT_KEYWORDS = [
        "chủ dự án", "chủ đầu tư", "nhà đầu tư", "doanh nghiệp", 
        "tổ chức", "cá nhân", "hộ gia đình", "cộng đồng",
        "nhà sản xuất", "nhà nhập khẩu", "chủ nguồn thải"
    ]
    
    PROJECT_GROUP_PATTERN = r"(?:dự\s*án\s*)?(?:nhóm\s*)?([IiVv]+|1|2|3|4)"
    
    def parse(self, question: str) -> Tuple[Intent, Dict[str, Any]]:
        """Parse a question to extract intent and entities.
        
        Args:
            question: User's question in Vietnamese
            
        Returns:
            Tuple of (Intent, extracted entities dict)
        """
        question_lower = question.lower().strip()
        question_clean = self._normalize_text(question_lower)
        
        # Try to match intent patterns
        for intent, patterns in self.PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, question_clean, re.IGNORECASE)
                if match:
                    entity = match.group(1).strip() if match.groups() else ""
                    entities = self._extract_entities(entity, question_clean, intent)
                    return intent, entities
        
        # Default to general query with keyword extraction
        entities = self._extract_general_entities(question_clean)
        return Intent.GENERAL, entities
    
    def _normalize_text(self, text: str) -> str:
        """Normalize Vietnamese text for pattern matching."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove punctuation at end
        text = re.sub(r'[?.!]+$', '', text)
        return text.strip()
    
    def _extract_entities(
        self, 
        primary_entity: str, 
        full_question: str, 
        intent: Intent
    ) -> Dict[str, Any]:
        """Extract entities based on intent type."""
        entities = {}
        
        if intent == Intent.DEFINITION:
            entities["term"] = self._clean_entity(primary_entity)
            
        elif intent == Intent.OBLIGATION:
            entities["subject"] = self._extract_subject(primary_entity, full_question)
            
        elif intent == Intent.PROCEDURE:
            entities["project_type"] = self._clean_entity(primary_entity)
            group = self._extract_project_group(full_question)
            if group:
                entities["project_group"] = group
                
        elif intent == Intent.CONSEQUENCE:
            entities["action"] = self._clean_entity(primary_entity)
            
        elif intent == Intent.AUTHORITY:
            entities["permission"] = self._clean_entity(primary_entity)
            group = self._extract_project_group(full_question)
            if group:
                entities["project_group"] = group
        
        return entities
    
    def _extract_general_entities(self, question: str) -> Dict[str, Any]:
        """Extract entities from a general question."""
        entities = {"query": question}
        
        # Try to find any recognizable terms
        for keyword in self.SUBJECT_KEYWORDS:
            if keyword in question:
                entities["subject"] = keyword
                break
        
        group = self._extract_project_group(question)
        if group:
            entities["project_group"] = group
        
        return entities
    
    def _extract_subject(self, entity: str, full_question: str) -> str:
        """Extract subject from entity or full question."""
        # Check for known subject keywords
        for keyword in self.SUBJECT_KEYWORDS:
            if keyword in entity.lower():
                return keyword
            if keyword in full_question.lower():
                return keyword
        
        return self._clean_entity(entity) if entity else ""
    
    def _extract_project_group(self, text: str) -> Optional[str]:
        """Extract project group (I, II, III, IV) from text."""
        match = re.search(self.PROJECT_GROUP_PATTERN, text, re.IGNORECASE)
        if match:
            group = match.group(1).upper()
            # Convert numeric to Roman
            num_to_roman = {"1": "I", "2": "II", "3": "III", "4": "IV"}
            return num_to_roman.get(group, group)
        return None
    
    def _clean_entity(self, entity: str) -> str:
        """Clean an extracted entity."""
        # Remove common filler words
        fillers = [
            "của", "cho", "về", "khi", "nếu", "thì", "là", "có",
            "những", "các", "một", "như", "thế", "nào", "gì"
        ]
        words = entity.split()
        cleaned = [w for w in words if w.lower() not in fillers]
        return " ".join(cleaned).strip()
