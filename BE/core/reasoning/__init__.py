# -*- coding: utf-8 -*-
"""
EnvLawReasoner - Multi-Reasoner System for Environmental Law QA
"""
# Core components
from .engine import RuleEngine
from .base import Fact, BaseRule
from .query_parser import QueryParser

# Legacy engines (still used internally)
from .engines.forward_chaining import ForwardChainingEngine
from .engines.backward_chaining import BackwardChainingEngine
from .engines.graph_traversal import GraphTraversalEngine
from .engines.pattern_matcher import PatternMatchingEngine

# NEW: Multi-Reasoner System
from .reasoners import (
    BaseReasoner,
    ReasonerResult,
    ReasonerType,
    ForwardChainingReasoner,
    BackwardChainingReasoner,
    GraphTraversalReasoner,
    OntologyReasoner,
    HybridReasoner,
    GraphRAGReasoner,
)
from .orchestrator import ReasonerOrchestrator
from .comparator import ReasonerComparator, ComparisonReport

# Import rules to make them available
from .rules.obligation_rules import *
from .rules.authority_rules import *
from .rules.consequence_rules import *
from .rules.causal_rules import *
from .rules.exemption_rules import *
from .rules.time_rules import *

__all__ = [
    # Core
    "RuleEngine", "Fact", "BaseRule", "QueryParser",
    # Legacy engines
    "ForwardChainingEngine", "BackwardChainingEngine", 
    "GraphTraversalEngine", "PatternMatchingEngine",
    # NEW Multi-Reasoner
    "BaseReasoner", "ReasonerResult", "ReasonerType",
    "ForwardChainingReasoner", "BackwardChainingReasoner",
    "GraphTraversalReasoner", "OntologyReasoner",
    "HybridReasoner", "GraphRAGReasoner",
    "ReasonerOrchestrator", "ReasonerComparator", "ComparisonReport",
]
