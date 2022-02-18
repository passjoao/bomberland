# ABMAEL DANTAS GOMES (https://github.com/abmaeld/) e 
# JOÃO V. SOARES OLIVEIRA (https://github.com/passjoao/)

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
from imports.mathfuncs import dist # distância euclidiana

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
        world = game_state.get("world")
        #

        # print('# ENTIDADES: ')
        # print(agente._obter_entidades(agente.agente_id))

        # inicializando o mapa na variável 'maze'
        maze = [[ 0 for i in range(world['width']) ] for j in range(world['height']) ]

        for i in range(world['width']):
            for j in range(world['height']):
                entidades = self._client._state.get("entities")
                celulas_1 = list(filter(lambda entity: 
                    entity.get(entity.get("type") == "m", entidades) or
                    entity.get(entity.get("type") == "w", entidades) or 
                    entity.get(entity.get("type") == "o", entidades) or 
                    entity.get(entity.get("type") == "b", entidades) or 
                    entity.get(entity.get("type") == "x", entidades)))
                cell = next(iter(celulas_1 or []), None)
                if cell != None:
                    maze[i][j] = 1
                else:
                    maze[i][j] = 0

        # 0 para pode passar
        # 1 para não pode passar
        # na destruição de bloco mudar para 0
        # não pode passar por cima da bomba, ao plantar mudar para 1
        # não tem colisão com inimigo

        # a* vai ser usado para:
        # chegar na unidade inimiga (viva) mais próxima da unidade atual (achar melhor caminho)
        # se puder plantar 1 bomba, planta
        # segue o inimigo se não tiver bomba perto dele, senão foge (switch case)
        
        # send each unit a random acao
        # tomada de decisão de cada unidade

        # só detonar ou plantar se tiver bomba no inventario
        # ir atras de bomba

        for unit_id in my_units: 
            # recupera agents
            agents = self._client._state.get("agents")
            unidade_estado = self._client._state.get("unit_state")[unit_id]

            # escolhe a ação que toma no tick:
            # decisão probabilística:
            tipo_acao = "move"
            possibilities = ([["detonate", 0.22], ["bomb", 0.55],["move", 0.66]]) # maquina de estados probabilística
            for possibility in possibilities:
                if random.randrange(100) < possibility[1] * 100:
                    tipo_acao = possibility[0]
                    break

            tem_bomba_plantada = True
            
            if tem_bomba_plantada and tipo_acao == "detonate":
                acao = tipo_acao
            elif tipo_acao == "bomb" and unidade_estado['inventory']['bombs'] > 0:
                acao = tipo_acao
            elif tipo_acao == "move" and unidade_estado['inventory']['bombs'] == 0:
                # escolhe o movimento:
                coordenadas = unidade_estado['coordinates']
                unit_x, unit_y = coordenadas['x'], coordenadas['y']
                start = (unit_x, unit_y)
                alvo_x, alvo_y = 0, 0
                d_min = 99999999

                if unidade_estado['inventory']['bombs'] >= 0:    
                    for agente in agents:
                        if agente['agent_id'] != my_agent_id:
                            for unidade_id in agente['unit_ids']:
                                #entidade = self._client._state.get(unidade_id)
                                unit_state = self._client._state.get("unit_state")
                                unidade = unit_state[unidade_id]
                                distancia = dist(unit_x, unit_y, unidade['coordinates']['x'], unidade['coordinates']['y'])
                                if distancia <= d_min:
                                    alvo_x = unidade['coordinates']['x']
                                    alvo_y = unidade['coordinates']['y']
                                    d_min = distancia
                else:
                    todas_entidades = self._client._state.get("entities")
                    for enti in todas_entidades:
                        if enti['type'] == 'a':
                            bomba_pra_pegar = enti
                            distancia = dist(unit_x, unit_y, bomba_pra_pegar['x'], bomba_pra_pegar['y'])
                            if distancia <= d_min:
                                alvo_x = bomba_pra_pegar['x']
                                alvo_y = bomba_pra_pegar['y']
                                d_min = distancia

                end = (alvo_x, alvo_y)
                path = astar(maze, start, end)
                
                # tansforma pares de pares ordenados (x,y) (z,w) para "up", "down", "left", "right"
                # tratar diagonais do A* 
                # path[0] -> path[1]
                
                if path[1][0] > path[0][0] and path[1][1] == path[0][1]: # simple right
                    acao = "right"
                elif path[1][0] < path[0][0] and path[1][1] == path[0][1]: # simple left
                    acao = "left"
                elif path[1][0] > path[0][0] and path[1][1] > path[0][1]: # diagonal down right
                    if path[1][0] < world['width']-1 and path[1][1] < world['height']-1: # se o bloco destino estiver dentro do mapa
                        if maze[path[0][0], path[0][1]+1] != 1: # se pra baixo não for bloqueado
                            acao = "down"
                        elif maze[path[0][0]+1, path[0][1]] != 1: # se pro lado não for bloqueado
                            acao = "right"
                        else:
                            acao = random.choice(["up", "left"])
                elif path[1][0] > path[0][0] and path[1][1] < path[0][1]: # diagonal up right
                    if path[1][0] < world['width']-1 and path[1][1] > 0: 
                        if maze[path[0][0], path[0][1]-1] != 1: # se pra cima não for bloqueado
                            acao = "up"
                        elif maze[path[0][0]+1, path[0][1]] != 1: # se pro lado não for bloqueado
                            acao = "right"
                        else:
                            acao = random.choice(["left", "down"])
                elif path[1][0] < path[0][0] and path[1][1] > path[0][1]: # diagonal down left
                    if path[1][0] > 0 and path[1][1] < world['height']-1: 
                        if maze[path[0][0], path[0][1]+1] != 1: # se pra baixo não for bloqueado
                            acao = "down"
                        elif maze[path[0][0]-1, path[0][1]] != 1: # se pro lado não for bloqueado
                            acao = "left"
                        else:
                            acao = random.choice(["up", "right"])
                elif path[1][0] < path[0][0] and path[1][1] < path[0][1]: # diagonal up left
                    if path[1][0] > 0 and path[1][1] > 0: 
                        if maze[path[0][0], path[0][1]-1] != 1: # se pra cima não for bloqueado
                            acao = "up"
                        elif maze[path[0][0]-1, path[0][1]] != 1: # se pro lado não for bloqueado
                            acao = "left"
                        else:
                            acao = random.choice(["right", "down"])
                elif path[1][0] == path[0][0] and path[1][1] > path[0][1]:
                    acao = "down"
                elif path[1][0] == path[0][0] and path[1][1] < path[0][1]:
                    acao = "up"
                else:
                    acao = random.choice(["up", "left", "right", "down"])
            else:
                acao = tipo_acao
                
            # movimento:
            if acao in ["up", "left", "right", "down"]:
                await self._client.send_move(acao, unit_id)

            # planta bomba:
            elif acao == "bomb":
                await self._client.send_bomb(unit_id)

            # quando for detonar, escolher melhor lugar para ir e o melhor momento para detonar
            # usar blast_diameter
            elif acao == "detonate":
                bomba_coordenadas = self._obter_coordenada_de_bomba_para_detonar(unit_id)
                if bomba_coordenadas != None:
                    x, y = bomba_coordenadas
                    # unit_x, unit_y = unit_id.get('coordinates')
                    if((x != unit_x and x != unit_x+1 and x != unit_x-1) and (y != unit_y and y != unit_y+1 and y != unit_y-1)):
                        await self._client.send_detonate(x, y, unit_id)
            else:
                print(f"Unhandled acao: {acao} for unit {unit_id}")

def main():
    Agent()

if __name__ == "__main__":
    main()