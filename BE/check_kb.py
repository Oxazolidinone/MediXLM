
import asyncio
import os
from neo4j import AsyncGraphDatabase
from dotenv import load_dotenv

import sys
sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()
URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
AUTH = (os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))

async def check_node():
    driver = AsyncGraphDatabase.driver(URI, auth=AUTH)
    async with driver.session() as session:
        print("Searching for exact 'Môi trường' node...")
        query = "MATCH (n:KhaiNiem) WHERE toLower(n.ten) = 'môi trường' RETURN n.ten, labels(n)"
        result = await session.run(query)
        record = await result.single()
        if record:
            print(f"Found: {record['n.ten']} - Labels: {record['labels(n)']}")
        else:
            print("Exact match 'Môi trường' NOT FOUND.")
            
        print("\nSearching contains 'Môi trường'...")
        query2 = "MATCH (n:KhaiNiem) WHERE toLower(n.ten) CONTAINS 'môi trường' RETURN n.ten LIMIT 10"
        result2 = await session.run(query2)
        records = await result2.values()
        for r in records:
            print(f"- {r[0]}")
            
    await driver.close()

if __name__ == "__main__":
    asyncio.run(check_node())
