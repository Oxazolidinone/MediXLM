
import asyncio
import os
from neo4j import AsyncGraphDatabase
from dotenv import load_dotenv

load_dotenv()
URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
AUTH = (os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))

async def setup_indexes():
    driver = AsyncGraphDatabase.driver(URI, auth=AUTH)
    async with driver.session() as session:
        print("Checking indexes...")
        result = await session.run("SHOW INDEXES")
        indexes = [record["name"] for record in await result.data()]
        print(f"Existing indexes: {indexes}")
        
        if "envLawIndex" in indexes:
            print("Dropping old index...")
            await session.run("DROP INDEX envLawIndex")

        print("Creating Full Text Index 'envLawIndex'...")
        # Create index on common text properties for all main nodes
        query = """
        CREATE FULLTEXT INDEX envLawIndex FOR (n:KhaiNiem|DoiTuong|CoQuan|HanhVi|QuyenNghiaVu|TrachNhiem|NhomDuAn|BuocQuyTrinh|KetQua) 
        ON EACH [n.ten, n.mo_ta, n.noi_dung, n.keyphrase, n.viet_tat]
        """
        await session.run(query)
        print("Index created.")
            
    await driver.close()

if __name__ == "__main__":
    asyncio.run(setup_indexes())
