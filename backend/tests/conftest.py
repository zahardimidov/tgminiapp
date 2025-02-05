import logging
import os
import subprocess
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ['ENV'] = 'tests/.testenv'

import pytest
from fastapi.testclient import TestClient
from run import app
from config import BASE_DIR
import time
import asyncio


async def run_database():
    from sqlalchemy.ext.asyncio import create_async_engine
    from database.models import Base

    engine = create_async_engine(url=os.environ['ENGINE'], echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

@pytest.fixture(autouse=True, scope="session")
def logger() -> logging.Logger:
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)


@pytest.fixture(scope='session')
def docker_compose_file():
    return BASE_DIR.joinpath('tests/test-docker-compose.yml')


@pytest.fixture(scope='session', autouse=True)
def setup_session(docker_compose_file):
    env_file = BASE_DIR.joinpath(os.environ['ENV'])
    subprocess.run(
        f"docker compose --env-file {env_file} -f {docker_compose_file} up --build -d".split())
    time.sleep(2.5)
    asyncio.run(run_database())
    time.sleep(0.5)
    yield
    subprocess.run(
        f'docker compose  --env-file {env_file}  -f {docker_compose_file} down'.split())


@pytest.fixture(autouse=True, scope="module")
def client():
    return TestClient(app)
