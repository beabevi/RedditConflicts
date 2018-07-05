import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter

INPUT = "/home/beatrice/Desktop/WIR/data/all_graphs2.txt"

def compute_rankings(in_file):
    with open(in_file, 'r') as in_file:
        for line in in_file:
            parts = line.split('\t')

            info = parts[0]
            edges = parts[1].strip("[").strip("]").split(', ')
            attackers = parts[2].strip("[").strip("]").replace("'", "").split(", ")
            defenders = parts[3].strip("[").strip("]").replace("'", "").split(", ")

            G = nx.DiGraph()

            for edge in edges:
                nodes = edge.split(" ")
                former = nodes[0].strip("'")
                latter = nodes[1].strip("'")
                
                G.add_edge(former, latter)

            values = [0.6 if node in attackers else 0.2 for node in G.nodes()]    
            nx.draw_networkx(G, node_color=values, cmap=plt.get_cmap('jet'), node_size = 50, with_labels=False)
            plt.show() 

            #up to now i pass only one graph, it must be changed to compute an aggregated value for page rank
            #given multiple graphs
            a_personalization = {}
            d_personalization = {}
            #print(attackers)
            for node in G.nodes():  
                a_personalization[node] =  1 if node in attackers else 0
                #d_personalization[node] = 1 if node in defenders else 0
            a_pr = nx.pagerank(G, alpha=0.85, personalization=a_personalization)
            sorted_pr = sorted(a_pr.items(), key=itemgetter(1), reverse = True)
            for i in sorted_pr:
                print(i) 

compute_rankings(INPUT)


