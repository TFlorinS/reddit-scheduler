import sqlite3, time, os
from datetime import datetime
from dotenv import load_dotenv
import praw

load_dotenv()

def reddit_login(account):
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        username=os.getenv(f'{account}_USERNAME'),
        password=os.getenv(f'{account}_PASSWORD'),
        user_agent=os.getenv('REDDIT_USER_AGENT')
    )
    return reddit

def post_image(reddit, subreddit_name, title, image_path):
    reddit.subreddit(subreddit_name).submit_image(title, image_path=image_path)

while True:
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    conn = sqlite3.connect('posts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE scheduled_time=? AND posted=0", (now,))
    posts_to_post = c.fetchall()

    for post in posts_to_post:
        reddit = reddit_login(post[1])
        post_image(reddit, post[2], post[3], post[4])
        c.execute("UPDATE posts SET posted=1 WHERE id=?", (post[0],))
        conn.commit()
        print(f"Posted: {post[3]} at {now}")

    conn.close()
    time.sleep(60)  # check every minute