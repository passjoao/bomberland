
from typing import Union
from game_state import GameState
import asyncio
import random
import os
from imports.astar import Node, astar # importando implementação do A*

uri = os.environ.get(
    'GAME_CONNECTION_STRING') or "ws://127.0.0.1:3000/?role=agent&agentId=agentId&name=defaultName"

acoes = ["up", "down", "left", "right", "bomb", "detonate"]

class Agent():
    def __init__(self):
        self._client = GameState(uri)

        # any initialization code can go here
        self._client.set_game_tick_callback(self._on_game_tick)

        loop = asyncio.get_event_loop()
        connection = loop.run_until_complete(self._client.connect())
        tasks = [
            asyncio.ensure_future(self._client._handle_messages(connection)),
        ]
        loop.run_until_complete(asyncio.wait(tasks))

    def _obter_entidades(self, unit) -> Union[int, int] or None:
        entidades = self._client._state.get("entities")
        return list(filter(lambda entity: entity.get(
            (entity.get("type") == "m" or
            entity.get("type") == "w" or
            entity.get("type") == "o" or 
            entity.get("type") == "b" or
            entity.get("type") == "x"), entidades)))
        # return list(filter(lambda entity: entity.get(
        #     "unit_id") == unit and entity.get("type") == "b", entidades))

    async def _on_game_tick(self, tick_number, game_state):
        # get my units
        # recuperando os agentes/unidades
        my_agent_id = game_state.get("connection").get("agent_id")
        my_units = game_state.get("agents").get(my_agent_id).get("unit_ids")
        #print(my_units)

agente = Agent()

maze2 = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 1, 1],
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# 0 para pode passar
# 1 para não pode passar
# na destruição de bloco mudar para 0
# não pode passar por cima da bomba, ao plantar mudar para 1
# não tem colisão com inimigo

# a* vai ser usado para:
# chegar na unidade inimiga (viva) mais próxima da unidade atual (achar melhor caminho)
# se puder plantar 1 bomba, planta
# segue o inimigo se não tiver bomba perto dele, senão foge (switch case)

start = (0, 0)
end = (9, 9)

path = astar(maze2, start, end)
print(path)