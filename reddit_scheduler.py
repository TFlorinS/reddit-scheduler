import os
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
import praw

load_dotenv()

def reddit_login(account='ACCOUNT1'):
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        username=os.getenv(f'{account}_USERNAME'),
        password=os.getenv(f'{account}_PASSWORD'),
        user_agent=os.getenv('REDDIT_USER_AGENT')
    )
    return reddit

def post_image(reddit, subreddit_name, title, image_path):
    subreddit = reddit.subreddit(subreddit_name)
    subreddit.submit_image(title=title, image_path=image_path)
    print(f"[{datetime.now()}] Posted '{title}' to r/{subreddit_name}")

def schedule_post(account, subreddit, title, image, scheduled_time):
    def job():
        reddit = reddit_login(account)
        post_image(reddit, subreddit, title, image)
    schedule.every().day.at(scheduled_time).do(job)
    print(f"Scheduled '{title}' to r/{subreddit} at {scheduled_time} daily.")

# Example Usage:
schedule_post(
    account='ACCOUNT1',
    subreddit='testsubreddit',
    title='Scheduled Post from Script',
    image='path/to/your/image.jpg',  # Local path to your image
    scheduled_time='15:30'  # 3:30 PM daily
)

# Run scheduler continuously
print("Scheduler is running...")
while True:
    schedule.run_pending()
    time.sleep(30)
