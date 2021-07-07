from connect4_zero.env.connect4_env import Connect4Env
from fastapi import APIRouter

import threading

# https://pydantic-docs.helpmanual.io/datamodel_code_generator/

router = APIRouter(
    prefix="/rl/connect4",
    tags=["connect4"],
    responses={404: {"description": "Not found"}},
)


class EnvLock(object):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(EnvLock, "_instance"):
            with EnvLock._instance_lock:
                if not hasattr(EnvLock, "_instance"):
                    EnvLock._instance = object.__new__(cls)

                    EnvLock.env = Connect4Env().reset()

        return EnvLock._instance

    def __init__(self):
        self.env = self.env


Env = EnvLock()


@router.put("/reset")
async def reset():
    Env.env.reset()
    return


@router.post("/move")
async def move(movement: int):
    legal_moves = Env.env.legal_moves()
    if legal_moves[movement] == 1:
        action = movement
        Env.env.step(action)