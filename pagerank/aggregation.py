
import matplotlib.pyplot as plt
import numpy as np

INPUT = "/home/beatrice/Desktop/WIR/data/aggregation.txt"

def aggregate_results(in_file):
    #attacker and defender aggregated scores in A-pageranks
    att_a_pagerank = 0
    def_a_pagerank = 0

    #attacker and defender aggregated scores in D-pageranks
    att_d_pagerank = 0
    def_d_pagerank = 0

    #total number of attackers and defenders in all networks
    n_attackers = 0
    n_defenders = 0
    with open(in_file, 'r') as in_file:
        for line in in_file:
            pageranks = line.split("\t")
            a_pagerank = pageranks[0]
            d_pagerank = pageranks[1]
            numbers = pageranks[2].split(",")

            a_values = a_pagerank.split(",")
            d_values = d_pagerank.split(",")

            att_a_pagerank += float(a_values[0])
            def_a_pagerank += float(a_values[1])

            att_d_pagerank += float(d_values[0])
            def_d_pagerank += float(d_values[1])

            n_attackers += int(numbers[0])
            n_defenders += int(numbers[1])

    attackers_scores = [att_a_pagerank/n_attackers, att_d_pagerank/n_attackers]
    defenders_scores = [def_a_pagerank/n_defenders, def_d_pagerank/n_defenders]
    print(str(attackers_scores))
    print(str(defenders_scores))

    plotbars(attackers_scores, defenders_scores)
    
def plotbars(attackers, defenders):
    # data to plot
    n_groups = 2
    
    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8
    
    rects1 = plt.bar(index, attackers, bar_width, 
                    color='#960018',
                    label='Attackers')
    
    rects2 = plt.bar(index + bar_width, defenders, bar_width,
                    color='#111e6c',
                    label='Defenders')
    
    #plt.xlabel('PageRanks')
    plt.ylabel('Scores')
    plt.title('Scores in PageRanks')
    plt.xticks(index + bar_width/2, ('A-PageRank', 'D-PageRank'))
    plt.legend()
    
    plt.tight_layout()
    plt.show() 

aggregate_results(INPUT)
            


