# api/v1/endpoints/health.py

## Mục đích
Health check endpoint đơn giản để verify API availability. Sử dụng bởi load balancers, monitoring systems, và deployment pipelines.

## Chức năng chính

### GET /health - Health Check
- **Input**: None
- **Output**: `HealthResponse` (status, version)
- **Response**:
  ```json
  {
    "status": "healthy",
    "version": "1.0.0"
  }
  ```

## Liên kết với các file khác

### Dependencies (Import)
- `fastapi` - APIRouter, BaseModel
- Không có external dependencies

### Được sử dụng bởi
- Kubernetes liveness/readiness probes
- Load balancers (health checks)
- Monitoring systems (Prometheus, Datadog, etc.)
- CI/CD pipelines (deployment verification)
- Uptime monitoring services

### Được đăng ký trong
- `api/v1/__init__.py` - Router được include vào API v1
- `main.py` - Tag "health" trong OpenAPI

## Tác động nếu file này bị xóa

### 🟢 LOW IMPACT - HEALTH MONITORING BỊ ẢNH HƯỞNG

Nếu xóa file này:

1. **Load balancer checks fail**:
   - Deployment systems không verify được service health
   - Auto-scaling có thể bị ảnh hưởng

2. **Monitoring alerts**:
   - Health monitoring tools sẽ báo service down
   - On-call engineers sẽ nhận false alerts

3. **Deployment verification khó khăn**:
   - CI/CD pipelines không có simple endpoint để ping
   - Rollback decisions khó khăn hơn

4. **Application vẫn hoạt động bình thường**:
   - Core functionality không bị ảnh hưởng
   - Chỉ mất visibility vào service health

### Workaround
- Dùng root endpoint `/` thay thế (có trong `main.py`)
- Hoặc ping bất kỳ endpoint nào khác
- Nhưng không semantic và có thể có side effects

### Cách thay thế
Tạo health endpoint mới - rất đơn giản:
```python
@router.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
```

## Best Practices

### ✅ Current Implementation
- Lightweight (không có dependencies)
- Fast response (no I/O operations)
- Simple JSON response
- Semantic naming

### ⚠️ Limitations
- **Shallow health check**: Không verify database, Redis, Neo4j, Qdrant
- **No component status**: Không biết service nào down
- **No metrics**: Không có latency, memory, CPU info
- **Static version**: Hardcoded version string

### 🔧 Enhanced Health Check Example
```python
@router.get("/health")
async def health_check():
    """Basic health check."""
    return {"status": "healthy", "version": "1.0.0"}

@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with component status."""
    components = {}

    # Check database
    try:
        await check_database_connection()
        components["database"] = "healthy"
    except Exception as e:
        components["database"] = f"unhealthy: {str(e)}"

    # Check Redis
    try:
        redis = get_redis_client()
        await redis.ping()
        components["redis"] = "healthy"
    except:
        components["redis"] = "unhealthy"

    # Check Neo4j
    try:
        neo4j = get_neo4j_driver()
        await neo4j.verify_connectivity()
        components["neo4j"] = "healthy"
    except:
        components["neo4j"] = "unhealthy"

    # Check Qdrant
    try:
        qdrant = get_qdrant_client()
        qdrant.get_collections()
        components["qdrant"] = "healthy"
    except:
        components["qdrant"] = "unhealthy"

    # Check LLM service
    try:
        llm = get_llm_service()
        components["llm"] = "healthy" if llm else "unhealthy"
    except:
        components["llm"] = "unhealthy"

    # Overall status
    all_healthy = all(status == "healthy" for status in components.values())
    status_code = 200 if all_healthy else 503

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "healthy" if all_healthy else "degraded",
            "version": "1.0.0",
            "components": components,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@router.get("/health/live")
async def liveness():
    """Kubernetes liveness probe."""
    return {"status": "alive"}

@router.get("/health/ready")
async def readiness():
    """Kubernetes readiness probe."""
    # Check critical dependencies
    try:
        await check_database_connection()
        return {"status": "ready"}
    except:
        raise HTTPException(status_code=503, detail="Not ready")
```

## Kubernetes Integration

### Liveness Probe
```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
```

### Readiness Probe
```yaml
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
```

## Monitoring Integration

### Prometheus Metrics
```python
from prometheus_client import Counter, Histogram

health_check_counter = Counter('health_check_total', 'Health check requests')
health_check_latency = Histogram('health_check_latency_seconds', 'Health check latency')

@router.get("/health")
@health_check_latency.time()
async def health_check():
    health_check_counter.inc()
    return {"status": "healthy", "version": "1.0.0"}
```

## Security Considerations

### ⚠️ Information Disclosure
Current implementation là safe, nhưng detailed health checks có thể leak info:
- Database connection strings
- Service versions (vulnerability scanning)
- Internal architecture

### 🔒 Recommendations
- Detailed health check nên require authentication
- Chỉ expose basic health check publicly
- Log failed health checks (có thể là attack)
