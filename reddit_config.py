import praw
import csv
import os
from datetime import datetime
import re

reddit = praw.Reddit(
    client_id="7MD9yq_tFRiyF_C3S9SfWA",          
    client_secret="TOOrSU6E4HHdWafRuqpV_rtXLKnnkg",      
    user_agent="python:io.lab8.bot:v1.0 (by u/TheLazyBatat)",
)

keywords = ["wybory", "prezydent", "prezydenckie", "kampania", "Trzaskowski", "Nawrocki", "Mentzen", "Braun", "Zandberg", "Hołownia", "Biejat", "Jakubiak", "Seneszyn", "Stanowski", "Woch", "Maciak", "Bartoszewicz", "Tusk", "Kaczyński", "debata", "Koalicja", "PiS",
            "KO", "Konfederacja", "Lewica", "2050"]

subreddits = ["Polska", "PolskaPolityka"]

start = datetime(2025, 1, 1)
output = "full_comments.csv"

if os.path.exists(output):
    os.remove(output)
    print("Plik został usunięty przed rozpoczęciem zapisu.")

with open(output, "w", newline="", encoding="utf-8") as plik:
    writer = csv.DictWriter(plik, fieldnames=["post_id", "post_timestamp", "subreddit", "post_author", "post_title", "post_text", "comment_id", "comment_author", "comment_timestamp", "comment_text", "phase"])
    writer.writeheader()
    
    for subreddit in subreddits:
        sub = reddit.subreddit(subreddit)
        print(f"Lecimy z r/{subreddit}:")
        for post in sub.new(limit=1000):
            post_time = datetime.utcfromtimestamp(post.created_utc)
            if post_time > datetime(2025, 1, 1):
                post_content = (post.title + " " + post.selftext).lower()
                
                if not any(re.search(rf"\b{keyword.lower()}\b", post_content) for keyword in keywords):
                    continue
                
                try:
                    post.comments.replace_more(limit=0)
                    for comment in post.comments.list():
                        comment_time = datetime.utcfromtimestamp(comment.created_utc)
                        
                        if comment_time < datetime(2025, 5 , 18):
                            phase = "pre"
                        elif comment_time <= datetime(2025, 5, 31):
                            phase = "between"
                        else:
                            phase = "post"
                            
                        writer.writerow({
                            "post_id": post.id,
                            "post_timestamp": post_time.isoformat(),
                            "subreddit": subreddit,
                            "post_author": post.author.name if post.author else "[deleted]",
                            "post_title": post.title,
                            "post_text": post.selftext,
                            "comment_id": comment.id,
                            "comment_author": comment.author.name if comment.author else "[deleted]",
                            "comment_timestamp": comment_time.isoformat(),
                            "comment_text": comment.body,
                            "phase": phase
                        })
                except Exception as eror:
                    print("Błąd przy poście o id: ", post.id, {eror})
                    continue
            else:
                continue