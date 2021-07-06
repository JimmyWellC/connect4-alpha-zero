from connect4_zero.env.connect4_env import Connect4Env
from fastapi import APIRouter

import threading

# https://pydantic-docs.helpmanual.io/datamodel_code_generator/

router = APIRouter(
    prefix="/rl/connect4",
    tags=["connect4"],
    responses={404: {"description": "Not found"}},
)


class Env(object):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(Env, "_instance"):
            with Env._instance_lock:
                if not hasattr(Env, "_instance"):
                    Env._instance = object.__new__(cls)

                    Env.env = Connect4Env().reset()

        return Env._instance

    def __init__(self):
        self.env = self.env

board = Env


# @router.post("/reset")
# async def reset():
