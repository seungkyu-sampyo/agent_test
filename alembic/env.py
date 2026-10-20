import asyncio
import importlib
import os
import pkgutil
import sys
from logging.config import fileConfig
from pathlib import Path
from urllib.parse import quote_plus

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.database import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

load_dotenv()

# 환경변수 로드
db_engine: str = os.getenv("DB_ENGINE", "mssql+aioodbc")
db_user: str = os.getenv("DB_USER")
# 비밀번호 내 특수문자(#, @ 등) 인코딩 처리
db_password: str = quote_plus(os.getenv("DB_PASSWORD", ""))
db_host: str = os.getenv("DB_HOST", "localhost")
db_port: str = os.getenv("DB_PORT", "1433")
db_name: str = os.getenv("DB_NAME")

# 1. ODBC 드라이버 이름 가져오기 및 URL 인코딩 처리 (가장 중요)
odbc_driver: str = os.getenv("DB_ODBC_DRIVER", "ODBC Driver 17 for SQL Server")
encoded_driver: str = quote_plus(odbc_driver)

# 2. URL 끝에 ?driver={encoded_driver} 파라미터 명시
DATABASE_URL = f"{db_engine}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?driver={encoded_driver}"
config.set_main_option("sqlalchemy.url", DATABASE_URL.replace("%", "%%"))


def load_all_entities_auto():
    alembic_dir = Path(__file__).resolve().parent
    project_root = alembic_dir.parent

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    for entities_dir in project_root.rglob("entity"):
        for _, module_name, _ in pkgutil.iter_modules([str(entities_dir)]):
            relative_path = entities_dir.relative_to(project_root)
            module_path = f"{str(relative_path).replace('/', '.').replace('\\', '.')}.{module_name}"
            importlib.import_module(module_path)


load_all_entities_auto()

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    # async_engine_from_config 사용
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
