# RedditConflicts

This repository covers three main subprojects regarding Reddit communities, their similarity and interactions.
This is part of a project for a class of Web Information Retrieval and the main inspiration for these works is
this paper [link to paper] from Leskovec et al. from Stanford University.

## Get Started

This project is composed of three different tasks:
- [Attackers and Defenders PageRank](#personalized-pagerank-on-cross-community-conflicts)
- [Subreddit Recommendation System](#subreddit-recommendation-system)
- [Cross-linking posts sentiment analysis](#sentiment-analysis-of-reddit-posts-leading-to-conflicts)

## Personalized PageRank on Cross-Community Conflicts

We reproduced some results of the paper answering the question on how users taking parts in conflicts interact
to each other. The researchers from Stanford proposed the Attackers and Defenders PageRanks.

This score is based on the graph of users replies to comments of members of their community or of the enemy 
community.

## Subreddit Recommendation System

We expanded the work of the original authors about similarities between communities to build a system that
suggests the user subreddits related to the ones he has been most active in its recent past.
We carried out our experiments using data of users in the interval of a month and we considered the 
top 5000 subreddits.

## Sentiment Analysis of Reddit Posts Leading to Conflicts

A post with a link to some content on a different subreddit may contain words that instigate a conflict on
that target subreddit. We analysed the sentiment of the text of such posts and of its top comments trying to
classify post with bad intents to neutral posts just sharing contents across communities.

We got on such task an F1 score of 90%

The code for this par of the project can be found in [this repository](https://github.com/spallas/reddit_sentiments).
