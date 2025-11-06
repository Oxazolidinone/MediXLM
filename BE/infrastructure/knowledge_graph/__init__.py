"""Knowledge Graph infrastructure (Neo4j)."""
from .neo4j_client import get_neo4j_driver, init_neo4j, close_neo4j

__all__ = ["get_neo4j_driver", "init_neo4j", "close_neo4j"]
