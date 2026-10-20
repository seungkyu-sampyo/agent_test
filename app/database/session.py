import os
from typing import AsyncGenerator
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

load_dotenv()


def database_url() -> str:
    """
    환경 변수를 기반으로 비동기 MSSQL(aioodbc) 연결 URL 문자열을 생성합니다.

    Returns:
        str: SQLAlchemy 데이터베이스 연결 DSN
             (예: 'mssql+aioodbc://sa:pass%23word@10.50.20.71:1433/UNIHR_DB?driver=ODBC+Driver+17+for+SQL+Server').
    """
    db_engine: str = os.getenv("DB_ENGINE", "mssql+aioodbc")
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: str = os.getenv("DB_PORT", "1433")
    db_name: str = os.getenv("DB_NAME")
    db_user: str = os.getenv("DB_USER")

    # 1. 비밀번호 내 특수문자(#, @ 등) 인코딩 처리
    db_password: str = quote_plus(os.getenv("DB_PASSWORD", ""))

    # 2. ODBC 드라이버 명시 및 URL 인코딩 (SAWarning 방지 핵심)
    odbc_driver: str = os.getenv("DB_ODBC_DRIVER", "ODBC Driver 17 for SQL Server")
    encoded_driver: str = quote_plus(odbc_driver)

    # 3. URL 끝에 ?driver={encoded_driver} 필수 포함
    return f"{db_engine}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?driver={encoded_driver}"


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