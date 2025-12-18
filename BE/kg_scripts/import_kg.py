
import os
import asyncio
from neo4j import AsyncGraphDatabase
from dotenv import load_dotenv

# Load env from BE/.env
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
AUTH = (os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))

CYPHER_FILE = os.path.join(os.path.dirname(__file__), '../kg/import.cypher')

async def import_data():
    print(f"Connecting to Neo4j at {URI}...")
    driver = AsyncGraphDatabase.driver(URI, auth=AUTH)
    
    try:
        async with driver.session() as session:
            # 1. Wipe DB
            print("Wiping existing database...")
            await session.run("MATCH (n) DETACH DELETE n")
            print("Database wiped.")

            # 2. Read Cypher
            if not os.path.exists(CYPHER_FILE):
                print(f"Error: {CYPHER_FILE} not found!")
                return

            print(f"Reading {CYPHER_FILE}...")
            with open(CYPHER_FILE, 'r', encoding='utf-8') as f:
                cypher_content = f.read()

            # 3. Split and Execute
            # Split by ';\n' to avoid splitting text containing semi-colons (e.g. lists inside text)
            statements = cypher_content.split(';\n')
            
            count = 0
            for stmt in statements:
                stmt = stmt.strip()
                if not stmt:
                    continue
                
                try:
                    await session.run(stmt)
                    count += 1
                    if count % 100 == 0:
                        print(f"Executed {count} statements...")
                except Exception as e:
                    print(f"Error executing statement: {stmt[:50].encode('ascii', 'replace').decode('ascii')}... \nError: {e}")

            print(f"Import complete. Total statements executed: {count}")
            
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        await driver.close()

if __name__ == "__main__":
    asyncio.run(import_data())
