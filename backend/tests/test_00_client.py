import asyncio
import atexit
import subprocess
from time import sleep

from env import DOCKER_COMPOSE_DOWN, DOCKER_COMPOSE_UP, log
from fastapi.testclient import TestClient
from run import app, text_query, run_database

@atexit.register
def shutdown():
    subprocess.run(DOCKER_COMPOSE_DOWN.split())


client = TestClient(app)

subprocess.run(DOCKER_COMPOSE_UP.split())
sleep(5)

loop = asyncio.new_event_loop()
loop.run_until_complete(run_database())
loop.run_until_complete(text_query(
    '''
INSERT INTO users (id, username) VALUES
  (7485502073, 'TestUser'),
  (7485502070, 'TestUser0'),
  (7485502071, 'TestUser1'),
  (7485502072, 'TestUser2');
'''
))

sleep(5)


def test_get_users():
    response = client.get('/users/all')
    log(response.json())
    assert response.status_code == 200
