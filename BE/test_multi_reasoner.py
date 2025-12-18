# -*- coding: utf-8 -*-
"""
Test script for EnvLawReasoner Multi-Reasoner System.
Run: python test_multi_reasoner.py
"""
import asyncio
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from neo4j import AsyncGraphDatabase
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")


async def test_multi_reasoner():
    """Test all reasoners running in parallel."""
    from infrastructure.services.local_llm_service import LocalLLMService
    from infrastructure.repositories.knowledge_graph_repository_impl import KnowledgeGraphRepositoryImpl
    from core.reasoning import (
        RuleEngine, QueryParser,
        ForwardChainingEngine,
        ForwardChainingReasoner,
        BackwardChainingReasoner,
        GraphTraversalReasoner,
        OntologyReasoner,
        HybridReasoner,
        GraphRAGReasoner,
        ReasonerOrchestrator,
        ReasonerComparator,
        # Rules
        PEIARule, DTMRule, GPMTRule,
        BoTNMTAuthorityRule, ProvinceAuthorityRule,
        IllegalDischargeRule, NoLicenseRule,
    )
    
    print("=" * 60)
    print("TEST: EnvLawReasoner Multi-Reasoner System")
    print("=" * 60)
    
    # Initialize services
    print("\n[1] Initializing services...")
    
    try:
        llm_service = LocalLLMService()
        print("  ✓ LLM Service initialized")
    except Exception as e:
        print(f"  ✗ LLM Service error: {e}")
        return
    
    try:
        driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        await driver.verify_connectivity()
        print("  ✓ Neo4j connected")
    except Exception as e:
        print(f"  ✗ Neo4j error: {e}")
        return
    
    # Initialize RuleEngine
    rule_engine = RuleEngine()
    rule_engine.register_strategy("forward", ForwardChainingEngine())
    
    rules = [PEIARule(), DTMRule(), GPMTRule(), BoTNMTAuthorityRule(), 
             ProvinceAuthorityRule(), IllegalDischargeRule(), NoLicenseRule()]
    for r in rules:
        rule_engine.add_rule(r)
    
    query_parser = QueryParser()
    
    # Initialize KG Repo (simplified for test)
    kg_repo = KnowledgeGraphRepositoryImpl(driver)
    
    # Create all reasoners
    print("\n[2] Creating reasoners...")
    reasoners = [
        ForwardChainingReasoner(rule_engine, query_parser),
        BackwardChainingReasoner(rule_engine, query_parser),
        GraphTraversalReasoner(driver),
        OntologyReasoner(driver),
        HybridReasoner(kg_repo, llm_service, rule_engine),
        GraphRAGReasoner(kg_repo, llm_service),
    ]
    
    for r in reasoners:
        print(f"  ✓ {r.name} ({r.reasoner_type.value})")
    
    # Create orchestrator and comparator
    orchestrator = ReasonerOrchestrator(reasoners)
    comparator = ReasonerComparator()
    
    # Test questions
    test_cases = [
        {
            "question": "Dự án Nhóm I có phải làm ĐTM không?",
            "intent": "yes_no",
            "entity": "Dự án Nhóm I lập báo cáo đtm"
        },
        {
            "question": "Nghĩa vụ của doanh nghiệp là gì?",
            "intent": "nghia_vu", 
            "entity": "doanh nghiệp"
        },
        {
            "question": "Xả thải trái phép bị xử lý thế nào?",
            "intent": "hau_qua",
            "entity": "xả thải trái phép"
        },
    ]
    
    print("\n[3] Running tests...")
    
    for i, tc in enumerate(test_cases, 1):
        print(f"\n{'='*50}")
        print(f"TEST {i}: {tc['question']}")
        print(f"Intent: {tc['intent']}, Entity: {tc['entity']}")
        print("="*50)
        
        # Run all reasoners in parallel
        results = await orchestrator.reason_all(
            question=tc["question"],
            intent=tc["intent"],
            entity=tc["entity"],
            context={}
        )
        
        # Generate comparison report
        report = comparator.compare(results)
        print(report.comparison_text)
        
        # Get consensus answer
        consensus = comparator.get_consensus_answer(results)
        print(f"\n>>> CONSENSUS ANSWER:\n{consensus}")
    
    # Cleanup
    await driver.close()
    print("\n\n✓ All tests completed!")


if __name__ == "__main__":
    asyncio.run(test_multi_reasoner())
