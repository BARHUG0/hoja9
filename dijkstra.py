import networkx as nx
import matplotlib.pyplot as plt
import re
import math



def read_graph_file(filename):
    file = open(filename, "r", encoding="utf8")
    lines = file.readlines()
    file.close
    return lines

def get_edges_tuples(stringlist):
    regex = "(?:“|\")([^“”\"]*)(?:”|\"),? *(?:“|\")([^“”\"]*)(?:”|\"),? *(\\d*)"
    not_parsed_tuples = []


    for string in stringlist:
        matches = re.findall(regex,string)
        for i in range (0, len(matches)):
            not_parsed_tuples.append(matches[i])

    parsed_tuples = []
    for string_edge in not_parsed_tuples:
        parsed_tuples.append((string_edge[0], string_edge[1], int(string_edge[2])))

    return parsed_tuples

def create_graph_from_file(filename):
    stringlist = read_graph_file(filename=filename)
    edge_tuples =  get_edges_tuples(stringlist=stringlist)
    graph = nx.Graph()
    graph.add_weighted_edges_from(edge_tuples)
    return graph

def show_graph(graph):
    pos = nx.spring_layout(graph, seed=7)  # positions for all nodes - seed for reproducibility

    # nodes
    nx.draw_networkx_nodes(graph, pos, node_size=1300)

    # edges
    nx.draw_networkx_edges(graph, pos, width=6, node_size=1300)

    # node labels
    nx.draw_networkx_labels(graph, pos, font_size=5, font_family="sans-serif")
    # edge weight labels
    edge_labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels, font_size=5)

    #ax = plt.gca()
    #ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.figure(1,figsize=(30,30)) 
    plt.show()

def get_dijkstra_paths(graph, starting_node):
    all_nodes_list = list(graph.nodes)
    all_nodes_lenght = len(all_nodes_list)
    starting_node_index = all_nodes_list.index(starting_node)

    matrix_L = []
    for n, nbrs in graph.adj.items():

        row = [math.inf] * (all_nodes_lenght)
        row[all_nodes_list.index(n)] = 0
        for nbr, eattr in nbrs.items():

            wt = eattr['weight']
            row[all_nodes_list.index(nbr)] = wt
 
        if(row not in matrix_L):
            matrix_L.append(row)

    cheaper_route_matrix = matrix_L[starting_node_index]
    previous_node_index_matrix = [-1] * len(matrix_L[starting_node_index])
    for i in range(0, len(matrix_L[starting_node_index])):
        if(not math.isinf(matrix_L[starting_node_index][i])):
            previous_node_index_matrix[i] = starting_node_index

    pending_node_indices = []
    for i in range(0, len(all_nodes_list)):
        if(i != starting_node_index):
           pending_node_indices.append(i)

    for i in range(0, all_nodes_lenght-1):

        current_index = None
        for j in pending_node_indices:
            if(not math.isinf(cheaper_route_matrix[j])):
                current_index = j
                pending_node_indices.remove(j)
                break
        
        if(current_index == None):
            break

        for j in range(0, all_nodes_lenght):
            if(cheaper_route_matrix[j]>(cheaper_route_matrix[current_index] + matrix_L[current_index][j])):
                cheaper_route_matrix[j]= cheaper_route_matrix[current_index] + matrix_L[current_index][j]
                previous_node_index_matrix[j] = current_index


    return [previous_node_index_matrix, cheaper_route_matrix]


def get_dijkstra_path(graph, dijkstra_paths_matrix, end_node, return_path_as_nodes=True):
    all_nodes_list = list(graph.nodes)
    starting_node_index = dijkstra_paths_matrix[1].index(0)
    end_node_index = all_nodes_list.index(end_node)
    dijkstra_index_path = []
    
    current_index = end_node_index
    dijkstra_index_path.append(current_index)
    while(current_index != starting_node_index):
        
        current_index = dijkstra_paths_matrix[0][current_index]
        if(current_index == -1):
            break
        dijkstra_index_path.append(current_index)

    if(current_index == -1):
        return None
    elif(return_path_as_nodes):
        cost = dijkstra_paths_matrix[1][end_node_index]
        dijkstra_index_path.reverse()
        dijkstra_node_path = []
        for i in dijkstra_index_path:
            dijkstra_node_path.append(all_nodes_list[i])
        return(dijkstra_node_path, cost)
    else:
        cost = dijkstra_paths_matrix[1][end_node_index]
        dijkstra_index_path.reverse()
        return(dijkstra_index_path, cost)

def get_edges_between_nodes(nodelist):
    if(len(nodelist) == 1):
        return nodelist[0]
    
    edgelist = []
    previous_node = nodelist[0]
    for i in range(1, len(nodelist)):
        edgelist.append((previous_node, nodelist[i]))
        previous_node = nodelist[i]

    return edgelist

    

def show_dijkstra_path_graph(graph, nodelist, edgelist):
    pos = nx.spring_layout(graph, seed=7)  # positions for all nodes - seed for reproducibility

    # nodes
    nx.draw_networkx_nodes(graph, pos, node_size=1300, nodelist=nodelist)

    # edges
    nx.draw_networkx_edges(graph, pos, width=6, node_size=1300, nodelist=nodelist, edgelist=edgelist)

    # node labels
    nx.draw_networkx_labels(graph, pos, font_size=5, font_family="sans-serif")
    # edge weight labels
    edge_labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels, font_size=5)

    #ax = plt.gca()
    #ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.figure(1,figsize=(30,30)) 
    plt.show()


def select_starting_ending_nodes(nodelist):
    for i in range(0, len(nodelist)):
        print(f"{i}. {nodelist[i]}")

    
    starting_node_index = input("Ingrese el número del nodo de partida: ")
    ending_node_index = input("Ingrese el número del nodo de destino: ")
    repeat_question = True
    while(repeat_question):
        if(not starting_node_index.isdigit() or not ending_node_index.isdigit()):
            print("Únicamente ingresar valores numéricos válidos")
            starting_node_index = input("Ingrese el número del nodo de partida: ")
            ending_node_index = input("Ingrese el número del nodo de destino: ")
        elif(int(starting_node_index) < 0 or int(starting_node_index) > len(nodelist) or int(ending_node_index) < 0 or int(ending_node_index) > len(nodelist)): 
            print("Únicamente ingresar valores dentro del rango")
            starting_node_index = input("Ingrese el número del nodo de partida: ")
            ending_node_index = input("Ingrese el número del nodo de destino: ")
        else:
            repeat_question = False


    return(nodelist[int(starting_node_index)], nodelist[int(ending_node_index)])



        

    


#print(select_starting_ending_nodes(nodelist=list(town_graph.nodes())))       
        
         


#show_graph(graph=town_graph)  
#dijkstra_paths_matrix = get_dijkstra_paths(graph=town_graph,starting_node=list(town_graph.nodes)[2])
#print(dijkstra_paths_matrix)
#dijkstra_path = get_dijkstra_path(graph=town_graph, dijkstra_paths_matrix=dijkstra_paths_matrix, end_node=list(town_graph.nodes)[3])
#print(get_dijkstra_path(graph=town_graph, dijkstra_paths_matrix=dijkstra_paths_matrix, end_node=list(town_graph.nodes)[3], return_path_as_nodes=False))
#edgelist = get_edges_between_nodes(nodelist=dijkstra_path[0])
#show_dijkstra_path_graph(graph=town_graph, nodelist=dijkstra_path[0], edgelist=edgelist)


def main():
    program = True
    print("Bienvenido la implementación del algoritmo Dijkstra")
    while(program):
        print(" 1. Cargar grafo de prueba \n 2. Cargar grafo del usuario \n 3. Salir")
        option = input("Ingrese la opción a ejecutar: ")
        match option:
            case "1":
                graph = create_graph_from_file("dijkstraTestGraph.txt")
                graph_menu(graph=graph)
                break
            case "2":
                filename = input("Ingrese el nombre del archivo que contiene un grafo \nEste debe seguir el formato establecido \n")
                graph = create_graph_from_file(filename=filename)
                graph_menu(graph=graph)
                break
            case "3":
                program = False
                break

def graph_menu(graph):
    menu = True
    print("Grafo cargado exitosamente")
    while(menu):
        print("1. Mostrar el grafo completo \n2. Calcular el camino entro dos nodos \n3. Mostrar el camino entre dos nodos \n4. Salir")
        op = input("Ingrese la opción a ejecutar: ")
        match op:
            case "1":
                show_graph(graph=graph)
                break
            case "2": 
                nodes = select_starting_ending_nodes(list(graph.nodes()))
                dijkstra_paths_matrix = get_dijkstra_paths(graph=graph,starting_node=nodes[0])
                dijkstra_path = get_dijkstra_path(graph=graph, dijkstra_paths_matrix=dijkstra_paths_matrix, end_node=nodes[1])
                print(dijkstra_path)
                break
            case "3":
                nodes = select_starting_ending_nodes(list(graph.nodes()))
                dijkstra_paths_matrix = get_dijkstra_paths(graph=graph,starting_node=nodes[0])
                dijkstra_path = get_dijkstra_path(graph=graph, dijkstra_paths_matrix=dijkstra_paths_matrix, end_node=nodes[1])
                edgelist = get_edges_between_nodes(nodelist=dijkstra_path[0])
                show_dijkstra_path_graph(graph=graph, nodelist=dijkstra_path[0], edgelist=edgelist)
                break
            case "4":
                menu = False
                break

main()