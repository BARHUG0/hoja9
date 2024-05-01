import networkx as nx
import matplotlib.pyplot as plt
import re
import math



text = "“Pueblo Paleta”, “Aldea Azalea”, 100 “Aldea Azalea”, “Ciudad Safiro”, 150 “Pueblo Paleta”, “Ciudad Safiro”, 800“Ciudad Lavanda”, “Aldea Fuego”, 300 “Ciudad Safiro”, “Aldea Fuego”, 50 "
regex = "(?:“|\")([^“”\"]*)(?:”|\"),? *(?:“|\")([^“”\"]*)(?:”|\"),? *(\\d*)"
not_parsed_tuples = re.findall(regex,text )
parsed_tuples = []
for string_edge in not_parsed_tuples:
    parsed_tuples.append((string_edge[0], string_edge[1], int(string_edge[2])))

town_graph = nx.Graph()

town_graph.add_weighted_edges_from(parsed_tuples)

def show_graph(graph):
    pos = nx.spring_layout(graph, seed=7)  # positions for all nodes - seed for reproducibility

    # nodes
    nx.draw_networkx_nodes(graph, pos, node_size=1300)

    # edges
    nx.draw_networkx_edges(graph, pos, width=6,)

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

    #List which will contains sublists with the following format:
    #Index 0: Destination node, Index 1: Origin node, Index 2: Cost
    print(all_nodes_list)
    matrix_L = []
    for n, nbrs in graph.adj.items():
        #print(nbrs)
        row = [math.inf] * (all_nodes_lenght)
        row[all_nodes_list.index(n)] = 0
        for nbr, eattr in nbrs.items():

            wt = eattr['weight']
            row[all_nodes_list.index(nbr)] = wt
            #print(f"({n}, {nbr}, {wt})")   
        if(row not in matrix_L):
            matrix_L.append(row)
    

    cheaper_route_matrix = matrix_L[starting_node_index]
    previous_node_index_matrix = [-1] * len(matrix_L[starting_node_index])
    for i in range(0, len(matrix_L[starting_node_index])):
        if(not math.isinf(matrix_L[starting_node_index][i])):
            previous_node_index_matrix[i] = starting_node_index

    print(cheaper_route_matrix)


    pending_node_indices = []
    for i in range(0, len(all_nodes_list)):
        if(i != starting_node_index):
           pending_node_indices.append(i)

    for i in range(0, all_nodes_lenght-1):
        print(all_nodes_list)
        print(cheaper_route_matrix)
        print(previous_node_index_matrix)

        current_index = None
        for j in pending_node_indices:
            if(not math.isinf(cheaper_route_matrix[j])):
                current_index = j
                pending_node_indices.remove(j)
                break
        
        if(current_index == None):
            break

        for j in pending_node_indices:
            if(cheaper_route_matrix[j]>(cheaper_route_matrix[current_index] + matrix_L[current_index][j])):
                cheaper_route_matrix[j]= cheaper_route_matrix[current_index] + matrix_L[current_index][j]
                previous_node_index_matrix[j] = current_index

        

    


        
        
         


show_graph(graph=town_graph)  
get_dijkstra_paths(graph=town_graph,starting_node=list(town_graph.nodes)[2])
