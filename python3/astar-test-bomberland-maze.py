from imports.astar import Node, astar

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