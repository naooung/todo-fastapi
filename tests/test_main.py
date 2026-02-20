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

@pytest.mark.asyncio
async def test_create_and_read(async_client):

    # Task 생성 요청
    response = await async_client.post("/tasks", json={"title": "테스트 작업"})
    assert response.status_code == starlette.status.HTTP_200_OK

    # 생성된 Task 응답 데이터 검증
    response_obj = response.json()
    assert response_obj["title"] == "테스트 작업"

    # 전체 Task 조회 요청
    response = await async_client.get("/tasks")
    assert response.status_code == starlette.status.HTTP_200_OK

    # DB에 실제로 저장되었는지 검증
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["title"] == "테스트 작업"

    # Done 기본 상태가 False인지 확인
    assert response_obj[0]["done"] is False

@pytest.mark.asyncio
async def test_done_flag(async_client):
    respone = await async_client.post("/tasks", json={"title": "테스트 작업2"})
    assert response.status_code == starlette.status.HTTP_200_OK

    # 완료 플래그 설정
    response = await async_client.put("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_200_OK

    # 이미 완료 플래그가 설정된 경우 - 400
    response = await async_client.put("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_400_BAD_REQUEST

    # 완료 플래그 해제
    response = await async_client.delete("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_200_OK

    # 이미 완료 플래그가 해제된 경우 - 404
    response = await async_client.delete("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND