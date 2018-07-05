import praw
import datetime


BURST_PATH = "/home/beatrice/Desktop/WIR/data/label_info.tsv"

#set your own info
reddit = praw.Reddit(client_id='my client id',
                     client_secret='my client secret',
                     user_agent='my user agent',
                     username='my username',
                     password='my password')

#print(reddit.user.me())

def get_bursts(file_name):
    bursts = []
    with open(file_name, 'r') as burst_file:
        for line in burst_file:
            ids, label = line.strip('\n').split('\t')
            if label == "burst":
                ids = ids.strip('(')
                ids = ids.strip(')')
                ids = ids.replace("'", '')
                bursts.append(ids)
    return bursts

def get_comments_bursts(out):
    bursts = get_bursts(BURST_PATH)
    print(len(bursts))

    with open(out, 'w') as out_file:
        
        for ids in bursts:
            posts = ids.split(', ')
            target_post = posts[1]
            source_post = posts[0]

            try:
                submission = reddit.submission(id=target_post)
                target_subreddit = str(submission.subreddit)
                time = datetime.datetime.fromtimestamp(submission.created)
                
                submission.comments.replace_more(limit=None)

                comments= []
                for comment in submission.comments.list():
                    author = comment.author
                    parent = comment.parent().author
                    if parent == None or author == None:
                        continue
                    author = author.name
                    parent = parent.name
                    comments.append(author + " " +  parent)

                submission = reddit.submission(id=source_post)
            
                source_subreddit = str(submission.subreddit)
                print("#")
                out_file.write(ids + ', ' + source_subreddit + ", " + target_subreddit + ", " + str(time) + '\t' + str(comments) + '\n')
            except Exception:
                print("hello")

            



get_comments_bursts("/home/beatrice/Desktop/WIR/data/all_comments.txt")