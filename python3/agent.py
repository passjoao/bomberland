# ABMAEL DANTAS GOMES E JOÃO V. SOARES OLIVEIRA 

# Contamos com observações feitas por Lucas de Oliveira Umbelino, amigo convidado
# LS4tLiAtLS0uIC0uLiAuLiAtLS4gLS0tIC8gLi0tLiAuLiAtLi0uIC4tIC8gLS4uLi0gLyAtLSAuLi0gLi4gLSAtLS0gLyAtLSAuLSAuLi4gLi4uIC4t (e.g.)

''' 
Link do problema
    Bomberland | Coder One (gocoder.one)
O que submeter
    Arquivo principal (agent.*) e eventuais arquivos secundários desenvolvidos pelo grupo; (agent.py, astar-test-bomberland-maze.py, imports/)
    README.md identificando os participantes do grupo, descrevendo a estratégia adotada (o que pretendeu ser feito) e as técnicas utilizadas e eventuais bibliotecas externas (nome e versão).
Compacte os arquivos em um único arquivo (.zip, tgz, .7z etc).
Critérios de avaliação
    Documentação e organização do código
    Adequação das técnicas utilizadas
    Qualidade do resultado
'''

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

    # returns coordinates of the first bomb placed by a unit
    # retorna coordenadas da primeira bomba plantada por uma unidade
    def _obter_coordenada_de_bomba_para_detonar(self, unit) -> Union[int, int] or None:
        entidades = self._client._state.get("entities")
        bombas = list(filter(lambda entity: entity.get(
            "unit_id") == unit and entity.get("type") == "b", entidades))
        bomb = next(iter(bombas or []), None)
        if bomb != None:
            return [bomb.get("x"), bomb.get("y")]
        else:
            return None

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

    # usar o A* para definir uma função que retorne o melhor posicionamento para a unidade no momento de explosao
    # essa func recebe o x e y da unidade e o x e y da bomba 
    # atualmente é feito por if(x !=agent_x or x !=agent_x+1 or y != agent_y or y != agent_y+1):
    # definir func para tomada de decisão de onde colocar a bomba

    # usar tentativa e erro na hora de verificar se existe uma entidade que 
    # seja relevante para a tomada de decisão

    async def _on_game_tick(self, tick_number, game_state):
        # get my units
        # recuperando os agentes/unidades
        my_agent_id = game_state.get("connection").get("agent_id")
        my_units = game_state.get("agents").get(my_agent_id).get("unit_ids")

        print('# ENTIDADES: ')
        print(agente._obter_entidades(agente.agente_id))

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

        # send each unit a random acao
        # tomada de decisão de cada unidade
        for unit_id in my_units:
            acao = random.choice(acoes)
            if acao in ["up", "left", "right", "down"]:
                await self._client.send_move(acao, unit_id)
            elif acao == "bomb":
                await self._client.send_bomb(unit_id)

            # quando for detonar, escolher melhor lugar para ir e o melhor momento para detonar
            elif acao == "detonate":
                bomba_coordenadas = self._obter_coordenada_de_bomba_para_detonar(unit_id)
                if bomba_coordenadas != None:
                    x, y = bomba_coordenadas
                    agent_x, agent_y = unit_id.get('coordinates')
                    if(x !=agent_x or x !=agent_x+1 or y != agent_y or y != agent_y+1):
                        await self._client.send_detonate(x, y, unit_id)
            else:
                print(f"Unhandled acao: {acao} for unit {unit_id}")

def main():
    Agent()

if __name__ == "__main__":
    main()