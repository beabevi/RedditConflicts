import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter

INPUT = "/home/beatrice/Desktop/WIR/data/all_graphs3.txt"
OUTPUT = "/home/beatrice/Desktop/WIR/data/aggregation.txt"

path = "/home/beatrice/Desktop/net_img/"

def compute_rankings(in_file, out_file):
    name = 0
    with open(in_file, 'r') as in_file, open(out_file, 'w') as out_file:
        for line in in_file:
            parts = line.strip("\n").split('\t')

            info = parts[0]
            edges = parts[1].strip("[").strip("]").split(', ')

            if (parts[1] == "[]" or parts[2] == "[]" or parts[3] == "[]"):
                continue

            attackers = parts[2].strip("[").strip("]").replace("'", "").split(", ")
            defenders = parts[3].strip("[").strip("]").replace("'", "").split(", ")

            fig = plt.figure(figsize=(6, 6))

            G = nx.DiGraph()

            for edge in edges:
                nodes = edge.split(" ")
                former = nodes[0].strip("'")
                latter = nodes[1].strip("'")
                
                G.add_edge(former, latter)

            values = [0.6 if node in attackers else 0.2 for node in G.nodes()]    
            nx.draw_networkx(G, node_color=values, cmap=plt.get_cmap('jet'), node_size = 50, with_labels=False)
            fig.savefig(path + str(name) + ".png", dpi=180, bbox_inches = 'tight', pad_inches = 0)
            name += 1
            #plt.show() 

            a_personalization = {}
            d_personalization = {}
            
            for node in G.nodes():  
                a_personalization[node] =  1 if node in attackers else 0
                d_personalization[node] = 1 if node in defenders else 0

            if all(a_personalization[v] == 0 for v in a_personalization):
                continue
            if all(d_personalization[v] == 0 for v in d_personalization):
                continue

            #attacker page rank    
            a_pr = nx.pagerank(G, alpha=0.75, personalization=a_personalization)
            sorted_a_pr = sorted(a_pr.items(), key=itemgetter(1), reverse = True)
            a_score1 = 0
            d_score1 = 0
            for i in sorted_a_pr:
                if i[0] in attackers:
                    a_score1 += i[1]
                else:
                    d_score1 += i[1]

            print(a_score1, d_score1)

            #defender page rank
            d_pr = nx.pagerank(G, alpha=0.75, personalization=d_personalization)
            sorted_d_pr = sorted(d_pr.items(), key=itemgetter(1), reverse = True)
            a_score2 = 0
            d_score2 = 0
            for i in sorted_d_pr:
                if i[0] in attackers:
                    a_score2 += i[1]
                else:
                    d_score2 += i[1]
            
            print(a_score2, d_score2)

            out_file.write(str(a_score1) +  "," + str(d_score1) + "\t")
            out_file.write(str(a_score2) + "," + str(d_score2) + "\t" )
            out_file.write(str(len(attackers)) + "," + str(len(defenders)) + "\n")

compute_rankings(INPUT, OUTPUT)


