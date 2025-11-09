# infrastructure/database/connection.py

## Mục đích
File này quản lý database connection pool và session management cho PostgreSQL. Sử dụng synchronous SQLAlchemy để tránh greenlet spawn errors với async SQLAlchemy. Provides session factory và context managers cho database operations.

## Chức năng chính

### Global Objects
- **engine**: SQLAlchemy synchronous engine với connection pooling
- **SessionLocal**: Session factory tạo database sessions
- **Base**: Declarative base cho ORM models

### init_database()
Async function initialize database:
- Import models từ .models
- Tạo tất cả tables với Base.metadata.create_all()
- Called during application startup

### close_database()
Async function đóng database connections:
- Dispose engine và close all connections
- Called during application shutdown

### get_database_session() -> Session
Context manager tạo database session:
- Create new session từ SessionLocal
- Auto-commit on success
- Auto-rollback on exception
- Always close session trong finally block
- Usage: `with get_database_session() as session:`

### get_sync_session() -> Session
Get synchronous session without context manager:
- Return raw session instance
- Caller responsible for closing session
- Used trong thread executors

## Liên kết với các file khác

### Dependencies (Import)
- **sqlalchemy**: create_engine, Session - Core SQLAlchemy
- **sqlalchemy.orm**: declarative_base, sessionmaker
- **contextlib**: contextmanager
- **core.config**: settings - Database configuration

### Được sử dụng bởi
- **main.py**: Initialize và close database on startup/shutdown
- **application/use_cases/user_use_case.py**: Get sessions cho user operations
- **application/use_cases/chat_use_case.py**: Get sessions cho chat operations
- **infrastructure/repositories/**: All repository implementations
- **api/dependencies.py**: Dependency injection

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - Complete Database Access Failure

File này là ONLY WAY để connect với database. Nếu bị xóa:

- **Application không thể start**: Không initialize database tables
- **Tất cả database operations fail**: Không có sessions
- **Users không thể tạo account**: No database access
- **Chat không thể save messages**: No database access
- **Complete application failure**: Tất cả features cần database

### Cách thay thế
1. Recreate engine với synchronous SQLAlchemy
2. Recreate SessionLocal factory
3. Recreate get_database_session context manager
4. Implement init_database và close_database lifecycle hooks

## Technical Notes

### Synchronous Driver Choice
Dùng synchronous psycopg2 driver thay vì asyncpg:
```python
DATABASE_URL = "postgresql://..." # psycopg2
# Not: "postgresql+asyncpg://..." # causes greenlet errors
```

### Connection Pooling
- **pool_size**: 20 connections
- **max_overflow**: 10 additional connections
- **pool_pre_ping**: Test connections before use

### Session Configuration
- **expire_on_commit=False**: Don't expire objects after commit
- **autoflush=False**: Manual control of flush operations

### Thread Safety
Sessions are NOT thread-safe. Each thread needs own session.
