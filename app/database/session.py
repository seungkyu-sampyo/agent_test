import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

load_dotenv()


def database_url() -> str:
    """
    환경 변수를 기반으로 비동기 PostgreSQL 연결 URL 문자열을 생성합니다.

    Returns:
        str: SQLAlchemy 데이터베이스 연결 DSN (예: 'postgresql+asyncpg://user:pass@host:5432/db').
    """
    db_engine: str = os.getenv("DB_ENGINE", "postgresql+asyncpg")
    db_user: str = os.getenv("DB_USER")
    db_password: str = os.getenv("DB_PASSWORD")
    db_host: str = os.getenv("DB_HOST")
    db_port: str = os.getenv("DB_PORT")
    db_name: str = os.getenv("DB_NAME")

    return f"{db_engine}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


# 비동기 데이터베이스 엔진 인스턴스
engine = create_async_engine(
    url=database_url(),
)

# 비동기 세션 생성 팩토리
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI 의존성 주입을 위한 비동기 세션 제너레이터.

    요청마다 새로운 세션을 열고 작업 완료 후 자동으로 닫습니다.

    Yields:
        AsyncSession: 비동기 데이터베이스 세션.
    """
    async with async_session_maker() as session:
        yield session
