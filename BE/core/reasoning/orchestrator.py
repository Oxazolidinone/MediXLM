# -*- coding: utf-8 -*-
"""
ReasonerOrchestrator - Runs multiple reasoners in parallel.
Part of EnvLawReasoner multi-reasoner system.
"""
import asyncio
from typing import List, Dict, Any
from .reasoners.base_reasoner import BaseReasoner, ReasonerResult


class ReasonerOrchestrator:
    """
    Orchestrates multiple reasoners to run in parallel.
    
    Features:
    - Concurrent execution using asyncio.gather
    - Intent-based reasoner filtering
    - Error isolation per reasoner
    """
    
    def __init__(self, reasoners: List[BaseReasoner] = None):
        self.reasoners = reasoners or []
    
    def add_reasoner(self, reasoner: BaseReasoner):
        """Add a reasoner to the orchestrator."""
        self.reasoners.append(reasoner)
    
    def get_reasoner_names(self) -> List[str]:
        """Get list of registered reasoner names."""
        return [r.name for r in self.reasoners]
    
    async def reason_all(
        self, 
        question: str, 
        intent: str, 
        entity: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, ReasonerResult]:
        """
        Execute all applicable reasoners in parallel.
        
        Args:
            question: User question
            intent: Detected intent
            entity: Extracted entity
            context: Additional context
            
        Returns:
            Dict mapping reasoner name to result
        """
        context = context or {}
        
        # Filter reasoners that support this intent
        applicable_reasoners = [
            r for r in self.reasoners
            if r.supports_intent(intent)
        ]
        
        if not applicable_reasoners:
            return {}
        
        # Create tasks for parallel execution
        async def safe_reason(reasoner: BaseReasoner) -> tuple:
            """Wrap reasoning in try-except to isolate errors."""
            try:
                result = await reasoner.reason(question, intent, entity, context)
                return (reasoner.name, result)
            except Exception as e:
                # Return error result
                return (reasoner.name, ReasonerResult(
                    reasoner_name=reasoner.name,
                    reasoner_type=reasoner.reasoner_type,
                    success=False,
                    explanation=f"Error: {str(e)}"
                ))
        
        # Run all reasoners concurrently
        tasks = [safe_reason(r) for r in applicable_reasoners]
        results = await asyncio.gather(*tasks)
        
        # Convert to dict
        return {name: result for name, result in results}
    
    async def reason_selected(
        self,
        reasoner_names: List[str],
        question: str,
        intent: str,
        entity: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, ReasonerResult]:
        """Run only selected reasoners by name."""
        context = context or {}
        
        selected = [r for r in self.reasoners if r.name in reasoner_names]
        
        async def safe_reason(reasoner: BaseReasoner) -> tuple:
            try:
                result = await reasoner.reason(question, intent, entity, context)
                return (reasoner.name, result)
            except Exception as e:
                return (reasoner.name, ReasonerResult(
                    reasoner_name=reasoner.name,
                    reasoner_type=reasoner.reasoner_type,
                    success=False,
                    explanation=f"Error: {str(e)}"
                ))
        
        tasks = [safe_reason(r) for r in selected]
        results = await asyncio.gather(*tasks)
        
        return {name: result for name, result in results}
