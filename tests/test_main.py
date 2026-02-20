import pytest
import pytest_asyncio
import starlette.status

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api.db import get_db, Base
from api.main import app

ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    # 비동기식 DB 접속을 위한 엔진과 세션 작성
    async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
    async_session = sessionmaker(
        autocommit=False, 
        autoflush=False, 
        bind=async_engine, 
        class_=AsyncSession
    )

    # 테스트용 인메모리 SQLite 테이블 초기화 (함수별 재설정)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # 의존성 주입으로 FastAPI가 테스트용 DB를 참조하도록 변경
    async def get_test_db():
        async with async_session() as session:
            yield session

    
    app.dependency_overrides[get_db] = get_test_db

    # 테스트용 비동기 HTTP 클라이언트 반환
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

