import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent.parent.resolve()
ENV_FILE = BASE_DIR.joinpath('.localenv')

load_dotenv(ENV_FILE)

os.environ['ENGINE'] = 'test:test@localhost:5432/test'

DOCKER_COMPOSE_FILE = BASE_DIR.joinpath('backend/tests/docker-compose.yml')
DOCKER_COMPOSE_DOWN = f'docker compose -f {DOCKER_COMPOSE_FILE} --env-file {ENV_FILE} down'
DOCKER_COMPOSE_UP = f"docker compose -f {DOCKER_COMPOSE_FILE} --env-file {ENV_FILE} up --build -d"

httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_json_serializable(obj):
    try:
        json.dumps(obj)
        return True
    except (TypeError, OverflowError):
        return False

def log(obj, indent = 4):
    if is_json_serializable(obj):
        return logger.info(json.dumps(obj, indent=indent, ensure_ascii=False ))
    logger.info(obj)