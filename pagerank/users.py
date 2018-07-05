import requests
import json
import arrow
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter
import pprint

INPUT = "/home/beatrice/Desktop/WIR/data/all_comments2.txt"
OUTPUT = "/home/beatrice/Desktop/WIR/data/all_graphs2.txt"

comments_by_author = "https://api.pushshift.io/reddit/search/comment/?author="

def construct_graphs(in_file = INPUT, out_file = OUTPUT):
    with open(in_file, 'r') as in_file, open(out_file, 'a') as out_file:
        for burst in in_file:
            burst_info = burst.strip("\n").split("\t")

            info = burst_info[0].split(', ')
            replies = burst_info[1]

            print(replies.strip("[").strip("]"))
            edges, attackers, defenders = construct_graph(info[2], info[3], info[4], replies.strip("[").strip("]"))
            out_file.write(burst_info[0] + '\t' + str(edges) + '\t' + str(attackers) + '\t' + str(defenders) + '\n')



def construct_graph(attacker_sub, defender_sub, time, replies):
    a = arrow.get(time)
    before = a.timestamp
    after = a.shift(months=-1).timestamp
    time_range = "&before=" + str(before) + "&after" + str(after)

    users_dict = {}
    edges = []
    for reply in replies.split(", "):
        r = reply.split(" ")
        former = r[0].strip("'")
        latter = r[1].strip("'")

        if (users_dict.get(former, None) == None):
            is_attacker, is_defender = is_attacker_defender(former, time_range, attacker_sub, defender_sub)

            if is_attacker and not is_defender:
                users_dict[former] = 1
            elif not is_attacker and is_defender:
                users_dict[former] = -1
            else:
                users_dict[former] = 0
        
        if (users_dict.get(latter, None) == None):
            is_attacker, is_defender = is_attacker_defender(latter, time_range, attacker_sub, defender_sub)

            if is_attacker and not is_defender:
                users_dict[latter] = 1
            elif not is_attacker and is_defender:
                users_dict[latter] = -1
            else:
                users_dict[latter] = 0

        if (users_dict[former] != 0 and users_dict[latter] != 0):
            edges.append(former + " " + latter) 

    attackers = []
    defenders = []
    for user in users_dict.keys():
        if users_dict[user] == 1:
            attackers.append(user)
        elif (users_dict[user] == -1):
            defenders.append(user)
    return edges, attackers, defenders 

def is_attacker_defender(user, time_range, attacker_sub, defender_sub):
    try:
        user_subreddits = requests.get(comments_by_author + user + time_range + "&fields=subreddit").json()

        is_defender = False
        is_attacker = False

        for subreddit in user_subreddits["data"]:
            if subreddit["subreddit"] == attacker_sub:
                is_attacker = True
            elif subreddit["subreddit"] == defender_sub:
                is_defender = True

        return is_attacker, is_defender
    except json.decoder.JSONDecodeError:
        return "error"

construct_graphs()