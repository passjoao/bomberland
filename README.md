# Bomberland, IA de multi-conexões 

- **Discipline**: DIM0126 - INTELIGÊNCIA ARTIFICIAL PARA JOGOS I
- **Teacher**: ANDRE MAURICIO CUNHA CAMPOS [![Open GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/amccampos/)
- **Teacher**: CHARLES ANDRYE GALVAO MADEIRA [![Open GitHub](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](linkedin.com/in/charles-madeira-25b4426)
- **author** João Victor Soares Oliveira [![Open GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/passjoao/)
- **author** Abmael Dantas Gomes [![Open GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/abmaeld)

## Sobre
 Esse proejeto se deve a disciplina de Inteligencia artificial para jogos com o intuito de participar de uma competição entre os discentes no famoso jogo Bomberman.
Os professores da disciplina aproveitaram da plataforma do [Code One](gocoder.one), que permitiu a implementação da nossa IA.
O Bomberland é uma plataforma que podemos submeter nossos códigos e testá-los contra outras IAs pelo mundo, acesse a documentação por meio desse link [Bomberland](https://www.gocoder.one/bomberland)



## Desenvolvimento

O desafio inicial da dupla foi de escolher qual linguagem seria usada para a competição, visto que a plataforma oferece algumas opções como Python, Go, C++, TypeScript e outros. Então, devido a experiência dos dois foi escolhido a linguagem Python e assim começando o desenvolvimento da IA.

### Movimentação
<p>
A primeira parte a ser desenvolvida é a de movimentação das unidades da IA, com as inúmeras possibilidades de algorítimos de movimentação, um dos que mais foi melhor visto foi o A-estrela, um algorítimo de busca de caminho, ou mais conhecido como Path Finder, ele busca o melhor caminho entre dois pontos de uma malha de navegação.
Nele são selecionados dois pontos, a origem e o destino, e é feito um grafo de caminho procurando a rota com a menor distância possível, no nosso caso, utilizando a destância euclidiana como heuristica.
  
![image](https://miro.medium.com/max/420/1*HppvOLfDxXqQRFn0Cv2dHQ.gif)

</p>
<p>
  
> Criação de função Nó, para o A*
  
</p>

``` python
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
```

Em seguida, a criação do prórpio A* que tem como parâmetros o ponto inicial, o ponto final e a malha de navegação, que iremos aprofundarmos mais em breve


``` python
def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Criação dos nós de início e fim
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # lista de abertura e fechamento
    open_list = []
    closed_list = []

    # Adicionando nó inicial
    open_list.append(start_node)

    # percorrer até o fim da lista
    while len(open_list) > 0:

        # o nó atual
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # removendo  no autal da lista aberta e colocando na fechada 
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Procurando o objetivo, nó final
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # retorna o caminho inverso

        # Nós Filhos, quando é encontrado o nó objetivo, é selecionado os nós adjacentes para a procura do melhor caminho
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # nós adjacentes

            # Renotornando o no atual
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # verificando se o nó entá dentro da malha
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Verificando se existe algum obstáculo no nó adjacente selecionado
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Cria um novo nó caso passe nos testes
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

``` 

> O código do A* foi baseado no artigo publicado pelo medium, pode ser visto no link a seguir [link](https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2)

> tivemos um problema na implementação do A* que foi a movimentação na diagonal, visto que o código que nos baseamos contem essa movimentação e na plataforma não é possível se mover na diagonal, criamos um algorítimo simples para resolver isso. Veja no código fonte entre as linhas 170 a 212 do arquivo agent.py


### Malha de navegação
Para conseguir criar a malha de navegação mencionada anteriormente, utilizando os métodos da plataforma de retornar todas as entidades criamos  uma função que diz se exite uma entidade ou não em uma determinada coordenada

``` Python
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
```

O Maze é criado uma matriz de 15x15e adicionando 0 ou 1 a cada ponto da matriz, as unidade só podem se mover caso a entidade no local não seja uma das descritas no código acima 

> * b: Bomb
> * x: Blast
> * m: Metal Block
> * o: Ore Block
> * w: Wooden Block

<p>
A cada tick do jogo essa função é refeita e assim criando uma novo caminho para o objetivo mais próximo, a escolha desse objetivo é devido a um algorítimo de escolha probabilístico que será descito em breve. Quando a ação for de mover a unidade, o caminho que ela irá realizar será passar do ponto original até o ponto seguinte do algoritimo A*, por exemplo, caso o objetivo seja a unidade inimiga mais próxima, e esteja a cinco passos, o movimento será de ir do passo 0 ao passo 1, e no prox tick, caso a ação seja a mesma de mover, irá do 1 ao 2. entretanto a unidade inimiga também estaá se movimentando, então o maze é atualizado a cada tick do jogo.
</p>

## Máquina de estado probabilístico

Para a escolha da ação realizada pela unidade, criamos uma máquina de estado probabilístico simples, com a possibilidade de movimentação tendencionada a ação de "mover"

o código abaixo mostra o início da união da máquina de estado até a movimentação


``` python
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
            elif tipo_acao == "move":
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
```

## Finalizações
Com isso criamos a nossa IA de forma simples a prática, certamente pode ser melhor desenvolvida aprofundando os conceitos que foram abordados em aula e ajudatando ao nosso projeto. Pretendemos continuar futuramente com esse projeto, mas estamos satisfeitos com os resultados obtidos no decorrer do desenvolvimento. Queremos deixar os nossos agradecimentos aos professores e até uma próxima oportunidade de trabalhar-mos juntos novamente.

![Bomberland multi-agent environment](https://www.gocoder.one/static/bomberland-529e18e676d8d28feca69f8f78a35c55.gif "Bomberland")

