# -*- coding: utf-8 -*-
"""
EnvLawReasoner - Multi-Reasoner System for Environmental Law QA
Base interfaces and data structures.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
import time


class ReasonerType(Enum):
    """Types of reasoning strategies."""
    FORWARD_CHAINING = "forward_chaining"
    BACKWARD_CHAINING = "backward_chaining"
    GRAPH_TRAVERSAL = "graph_traversal"
    ONTOLOGY = "ontology"
    HYBRID = "hybrid"
    GRAPHRAG = "graphrag"


@dataclass
class ReasonerResult:
    """
    Standard output from all reasoners.
    Enables comparison across different reasoning strategies.
    """
    reasoner_name: str
    reasoner_type: ReasonerType
    success: bool
    conclusions: List[str] = field(default_factory=list)
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.0  # 0.0 - 1.0
    explanation: str = ""
    proof_path: List[str] = field(default_factory=list)  # For BC
    execution_time_ms: float = 0.0
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "reasoner_name": self.reasoner_name,
            "reasoner_type": self.reasoner_type.value,
            "success": self.success,
            "conclusions": self.conclusions,
            "evidence": self.evidence,
            "confidence": self.confidence,
            "explanation": self.explanation,
            "proof_path": self.proof_path,
            "execution_time_ms": self.execution_time_ms,
            "metadata": self.metadata
        }


class BaseReasoner(ABC):
    """
    Abstract base class for all reasoners in EnvLawReasoner system.
    Each reasoner implements a specific reasoning strategy.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique reasoner name for display."""
        pass
    
    @property
    @abstractmethod
    def reasoner_type(self) -> ReasonerType:
        """Type of reasoning strategy."""
        pass
    
    @property
    def supported_intents(self) -> List[str]:
        """List of intents this reasoner supports. Override in subclass."""
        return ["nghia_vu", "quyen", "che_tai", "hau_qua", "dinh_nghia", "yes_no"]
    
    def supports_intent(self, intent: str) -> bool:
        """Check if reasoner supports this intent."""
        return intent in self.supported_intents
    
    @abstractmethod
    async def reason(
        self, 
        question: str, 
        intent: str, 
        entity: str,
        context: Dict[str, Any]
    ) -> ReasonerResult:
        """
        Execute reasoning and return result.
        
        Args:
            question: Original user question
            intent: Detected intent (nghia_vu, quyen, etc.)
            entity: Extracted entity from question
            context: Additional context (kg_data, etc.)
            
        Returns:
            ReasonerResult with conclusions, evidence, confidence
        """
        pass
    
    def _create_result(
        self,
        success: bool,
        conclusions: List[str] = None,
        evidence: List[Dict] = None,
        confidence: float = 0.0,
        explanation: str = "",
        proof_path: List[str] = None,
        execution_time_ms: float = 0.0,
        metadata: Dict = None
    ) -> ReasonerResult:
        """Helper to create standardized result."""
        return ReasonerResult(
            reasoner_name=self.name,
            reasoner_type=self.reasoner_type,
            success=success,
            conclusions=conclusions or [],
            evidence=evidence or [],
            confidence=confidence,
            explanation=explanation,
            proof_path=proof_path or [],
            execution_time_ms=execution_time_ms,
            metadata=metadata
        )
    
    def _measure_time(self, start_time: float) -> float:
        """Calculate elapsed time in ms."""
        return (time.time() - start_time) * 1000
