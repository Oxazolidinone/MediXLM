# scripts/seed_medical_knowledge.py

## Mục đích
File này là utility script để seed initial medical knowledge vào Qdrant vector database. Provides sample medical data về diabetes, hypertension, và cardiovascular diseases. Script này là essential tool để populate knowledge base cho RAG system testing và development.

## Chức năng chính

### SAMPLE_MEDICAL_DATA
List of sample medical knowledge dictionaries:
- **8 medical documents** covering:
  - Diabetes Type 2 (definition, symptoms, prevention)
  - Hypertension (definition, risk factors, treatment)
  - Coronary artery disease
  - Hyperlipidemia management

Each document contains:
- **text**: Medical knowledge content
- **source**: Attribution (WHO, Mayo Clinic, CDC, AHA, ACC)
- **category**: Medical category
- **metadata**: Disease type, knowledge type

### seed_data()
Main seeding function với 4 steps:

#### [1/4] Initialize Services
- Create QdrantClient với cloud URL và API key
- Initialize EmbeddingService
- Print connection info

#### [2/4] Check Collection
- Verify Qdrant collection exists
- Print current point count
- Exit nếu collection không exists

#### [3/4] Embed Documents
- Loop through SAMPLE_MEDICAL_DATA
- Generate embeddings cho each text
- Create PointStruct với:
  - ID: Sequential (1, 2, 3...)
  - Vector: Embedding vector (384 dimensions)
  - Payload: text, source, category, metadata
- Print progress cho each document

#### [4/4] Upload to Qdrant
- Upsert all points vào collection (batch upload)
- Verify upload success
- Print final collection point count
- Print example curl command để test

### Main Block
- Run seed_data() với error handling
- Handle KeyboardInterrupt gracefully
- Print full traceback on errors

## Liên kết với các file khác

### Dependencies
- **qdrant_client**: QdrantClient, models - Vector database client
- **infrastructure.services.embedding_service**: get_embedding_service
- **core.config**: settings - Qdrant configuration

### Được sử dụng bởi
- Manually run by developers/admins để populate knowledge base
- Run once during initial setup
- Re-run để refresh knowledge base

## Tác động nếu file này bị xóa

### 🟢 LOW - Seeding Utility Lost

Nếu bị xóa:
- **Knowledge base remains empty**: Không có initial medical data
- **RAG testing khó khăn**: No knowledge để test similarity search
- **Development slower**: Need manual data entry
- **Demo/testing affected**: No sample data cho showcasing RAG

Tuy nhiên, file này chỉ là utility script, không phải core application code.

### Cách thay thế
1. Recreate script với sample medical data
2. Manually insert data vào Qdrant
3. Create API endpoint để upload knowledge
4. Import từ medical databases/APIs

## Technical Notes

### Embedding Flow
```
Text → EmbeddingService → 384-dim vector → Qdrant PointStruct → Upsert
```

### Point IDs
Sequential IDs (1, 2, 3...):
- Simple và predictable
- Easy để debug
- Production nên dùng UUIDs

### Upsert vs Insert
Uses `upsert` instead of `insert`:
- Overwrites existing points với same ID
- Idempotent operation
- Safe để re-run script

### Batch Upload
All points uploaded trong single upsert call:
- More efficient than individual inserts
- Atomic operation
- Faster than loop

## Sample Medical Data Coverage

### Diabetes (3 documents)
- Definition và types
- Symptoms
- Prevention strategies

### Hypertension (3 documents)
- Definition và thresholds
- Risk factors
- Lifestyle modifications

### Cardiovascular (2 documents)
- Coronary artery disease pathophysiology
- Hyperlipidemia management

## Usage

### Run Script
```bash
cd BE
python scripts/seed_medical_knowledge.py
```

### Output Example
```
============================================================
SEEDING MEDICAL KNOWLEDGE TO QDRANT
============================================================

[1/4] Initializing services...
   Connected to Qdrant: https://...
   Embedding service ready (dimension: 384)

[2/4] Checking collection 'pubmedqa_vectors'...
   Collection exists with 0 points

[3/4] Embedding 8 medical documents...
   [1/8] Embedded: Diabetes - Diabetes mellitus is a chronic...
   [2/8] Embedded: Diabetes - Common symptoms of Type 2...
   ...

[4/4] Uploading 8 points to Qdrant...
   Successfully uploaded 8 points!
   Collection now has 8 total points

============================================================
SEEDING COMPLETE!
============================================================
```

### Test After Seeding
```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message":"What is diabetes?","user_id":"..."}'
```

## Future Improvements

1. **Expand medical data**: Add more diseases, treatments, medications
2. **Import từ datasets**: PubMedQA, MedQA, medical ontologies
3. **Multilingual data**: Vietnamese medical knowledge
4. **Knowledge validation**: Validate sources và facts
5. **Incremental seeding**: Add new knowledge without removing existing
6. **Knowledge versioning**: Track knowledge updates
7. **Deduplication**: Avoid duplicate knowledge entries
8. **Metadata enrichment**: Add ICD-10 codes, SNOMED CT codes
9. **Relationship seeding**: Also seed knowledge graph relationships
10. **Progress persistence**: Resume từ checkpoint nếu interrupted

## Production Considerations

### Data Sources
Production knowledge base nên từ:
- Medical textbooks
- Clinical guidelines (WHO, CDC, AHA)
- Medical databases (PubMed, UpToDate)
- Verified medical knowledge bases

### Quality Control
- Verify medical accuracy
- Cite authoritative sources
- Regular updates
- Medical professional review

### Compliance
- HIPAA compliance (nếu applicable)
- Medical disclaimer requirements
- Attribution requirements
- Copyright considerations
