"""Seed sample medical knowledge to Qdrant vector database."""
import sys
sys.path.insert(0, 'c:\\Users\\Long\\Downloads\\Đồ án biểu diễn tri thức\\MediXLM\\BE')

from qdrant_client import QdrantClient
from qdrant_client.http import models
from infrastructure.services.embedding_service import get_embedding_service
from core.config import settings

# Sample medical knowledge (you can expand this)
SAMPLE_MEDICAL_DATA = [
    {
        "text": "Diabetes mellitus is a chronic metabolic disorder characterized by elevated blood glucose levels. Type 1 diabetes results from autoimmune destruction of pancreatic beta cells, while Type 2 diabetes is characterized by insulin resistance and relative insulin deficiency.",
        "source": "WHO Diabetes Fact Sheet 2023",
        "category": "Diabetes",
        "metadata": {"disease": "diabetes", "type": "definition"}
    },
    {
        "text": "Common symptoms of Type 2 diabetes include increased thirst (polydipsia), frequent urination (polyuria), increased hunger, unexplained weight loss, fatigue, blurred vision, slow-healing sores, and frequent infections.",
        "source": "Mayo Clinic - Diabetes Symptoms",
        "category": "Diabetes",
        "metadata": {"disease": "diabetes", "type": "symptoms"}
    },
    {
        "text": "Prevention of Type 2 diabetes includes: maintaining a healthy weight (BMI 18.5-24.9), engaging in regular physical activity (at least 150 minutes per week), eating a balanced diet rich in fiber and low in processed sugars, and avoiding tobacco use.",
        "source": "CDC Diabetes Prevention Program",
        "category": "Diabetes",
        "metadata": {"disease": "diabetes", "type": "prevention"}
    },
    {
        "text": "Hypertension (high blood pressure) is defined as systolic blood pressure ≥140 mmHg or diastolic blood pressure ≥90 mmHg. It is a major risk factor for cardiovascular disease, stroke, and chronic kidney disease.",
        "source": "WHO Hypertension Guidelines 2023",
        "category": "Hypertension",
        "metadata": {"disease": "hypertension", "type": "definition"}
    },
    {
        "text": "Risk factors for hypertension include: age (>65 years), family history, obesity, physical inactivity, high salt intake (>5g/day), excessive alcohol consumption, and chronic stress.",
        "source": "American Heart Association",
        "category": "Hypertension",
        "metadata": {"disease": "hypertension", "type": "risk_factors"}
    },
    {
        "text": "Lifestyle modifications for hypertension management: DASH diet (Dietary Approaches to Stop Hypertension), regular aerobic exercise, weight reduction, limiting alcohol intake, reducing sodium consumption to <2g/day, and stress management.",
        "source": "JNC 8 Hypertension Guidelines",
        "category": "Hypertension",
        "metadata": {"disease": "hypertension", "type": "treatment"}
    },
    {
        "text": "Coronary artery disease (CAD) is caused by atherosclerotic plaque buildup in coronary arteries, reducing blood flow to the myocardium. Major risk factors include: smoking, diabetes, hypertension, dyslipidemia, obesity, and sedentary lifestyle.",
        "source": "American College of Cardiology",
        "category": "Cardiovascular",
        "metadata": {"disease": "cad", "type": "pathophysiology"}
    },
    {
        "text": "Hyperlipidemia management guidelines: LDL cholesterol goal <100 mg/dL for high-risk patients, <70 mg/dL for very high-risk. First-line therapy includes statins, lifestyle modifications (diet, exercise), and weight management.",
        "source": "ACC/AHA Cholesterol Guidelines",
        "category": "Cardiovascular",
        "metadata": {"disease": "hyperlipidemia", "type": "treatment"}
    },
]

def seed_data():
    """Upload sample medical data to Qdrant."""
    print("=" * 60)
    print("SEEDING MEDICAL KNOWLEDGE TO QDRANT")
    print("=" * 60)

    # Initialize clients
    print("\n[1/4] Initializing services...")
    client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY
    )
    print(f"   Connected to Qdrant: {settings.QDRANT_URL}")

    embedding_service = get_embedding_service()
    print(f"   Embedding service ready (dimension: {embedding_service.dimension})")

    # Check collection
    print(f"\n[2/4] Checking collection '{settings.QDRANT_COLLECTION_NAME}'...")
    try:
        collection_info = client.get_collection(settings.QDRANT_COLLECTION_NAME)
        print(f"   Collection exists with {collection_info.points_count} points")
    except Exception as e:
        print(f"   Collection check failed: {e}")
        return

    # Prepare points
    print(f"\n[3/4] Embedding {len(SAMPLE_MEDICAL_DATA)} medical documents...")
    points = []
    for i, data in enumerate(SAMPLE_MEDICAL_DATA):
        # Embed the text
        vector = embedding_service.embed_text(data["text"])

        # Create point
        point = models.PointStruct(
            id=i + 1,  # Start from 1
            vector=vector,
            payload={
                "text": data["text"],
                "source": data["source"],
                "category": data["category"],
                "metadata": data.get("metadata", {})
            }
        )
        points.append(point)
        print(f"   [{i+1}/{len(SAMPLE_MEDICAL_DATA)}] Embedded: {data['category']} - {data['text'][:50]}...")

    # Upload to Qdrant
    print(f"\n[4/4] Uploading {len(points)} points to Qdrant...")
    try:
        client.upsert(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            points=points
        )
        print(f"   Successfully uploaded {len(points)} points!")

        # Verify
        collection_info = client.get_collection(settings.QDRANT_COLLECTION_NAME)
        print(f"\n   Collection now has {collection_info.points_count} total points")

    except Exception as e:
        print(f"   Upload failed: {e}")
        return

    print("\n" + "=" * 60)
    print("SEEDING COMPLETE!")
    print("=" * 60)
    print("\nYou can now test RAG-enhanced chat:")
    print('  curl -X POST http://localhost:8000/api/v1/chat/ \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"message":"What is diabetes?","user_id":"..."}\'')
    print("\nThe chat will now use your embedded medical knowledge!")

if __name__ == "__main__":
    try:
        seed_data()
    except KeyboardInterrupt:
        print("\n\nSeeding cancelled by user.")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
