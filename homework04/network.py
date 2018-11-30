import time
from igraph import Graph, plot
import igraph
import numpy as np
from numpy import ndarray
from api import get_friends
from typing import List, Union


def get_network(users_ids: list, as_edgelist: bool = True) \
        -> Union[List, ndarray]:
    edges = []
    matrix = np.zeros((len(users_ids), len(users_ids)))
    for x in range(len(users_ids)):
        try:
            friends_ids_x = get_friends_id(users_ids[x])
            time.sleep(1 / 3)
            for y in range(x + 1, len(users_ids)):
                if users_ids[y] in friends_ids_x:
                    if as_edgelist:
                        edges.append((x, y))
                    else:
                        matrix[x][y] = 1
        except Exception:
            pass
    if as_edgelist:
        return edges
    else:
        return matrix


def get_friends_id(user_id: int) -> list:
    user_id = user_id
    friendslist = get_friends(user_id, 'id')
    users_id: list = []
    for j in range(friendslist['count']):
        users_id.append([])
        try:
            users_id[j] = int(friendslist['items'][j]['id'])
        except Exception:
            pass
    return users_id


def plot_graph(graph: int):
    lastname = get_friends(graph, 'last_name')
    vertices = [lastname['items'][i]['first_name']
                + ' ' + lastname['items'][i]['last_name']
                for i in range(lastname['count'])]
    edges = get_network(get_friends_id(graph), False)
    if isinstance(edges, ndarray):
        g = Graph.Adjacency(edges.tolist(), mode='undirected')
        g.vs['label'] = vertices
        g.vs['shape'] = 'triangle'
        g.vs['size'] = 10
    else:
        # Создание графа
        g = Graph(vertex_attrs={"shape": "triangle",
                                "label": vertices,
                                "size": 10},
                  edges=edges, directed=False)

    # Задаем стиль отображения графа
    n = len(vertices)
    visual_style = {"vertex_size": 20,
                    "bbox": (2000, 2000),  # размер поля
                    "margin": 100,  # расстояние от края до вершин
                    "vertex_label_dist": 1.6,  # расстояние между вершинами
                    "edge_color": "gray",
                    "autocurve": True,  # кривизна ребер
                    "layout": g.layout_fruchterman_reingold(
                        # Fruchterman-Reingold force-directed algorithm
                        # алгоритм компоновки
                        maxiter=1000,
                        # the maximum distance to move a vertex in an
                        # iteration. The default is the number of vertices
                        area=n ** 3,
                        # he area of the square on which the vertices will
                        #  be placed. The default is the square of the number
                        # of vertices.
                        repulserad=n ** 3
                        # determines the radius at which vertex-vertex
                        # repulsion cancels out attraction of adjacent
                        # vertices. The default is the number of vertices^3.
                    )}
    g.simplify(multiple=True, loops=True)
    # Отрисовываем граф
    clusters = g.community_multilevel()
    # Finds the community structure of the graph according
    # to the multilevel algorithm of Blondel et al.
    '''
    Это восходящий алгоритм: первоначально каждая вершина принадлежит 
    отдельному сообществу, а вершины перемещаются между сообществами 
    итеративно таким образом, чтобы максимизировать локальный вклад 
    вершин в общий показатель модульности. Когда достигнут консенсус 
    (т. Е. Ни один шаг не увеличит оценку модульности), каждое сообщество 
    исходного графа сократится до одной вершины (при сохранении общего 
    веса краев инцидентов), и процесс продолжит на следующем уровне. 
    Алгоритм останавливается, когда невозможно увеличить модульность 
    после сжатия сообществ до вершин.
    '''
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    # A palette suitable for coloring vertices when plotting a clustering.
    g.vs['color'] = pal.get_many(clusters.membership)
    plot(g, **visual_style)

# plot_graph(183344311)
