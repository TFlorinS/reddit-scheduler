from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('posts.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account TEXT,
            subreddit TEXT,
            title TEXT,
            image_path TEXT,
            scheduled_time TEXT,
            posted INTEGER DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            subreddit TEXT,
            title TEXT,
            image_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Run this always so Heroku initializes the DB
init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('posts.db')
    c = conn.cursor()
    c.execute('SELECT * FROM posts ORDER BY scheduled_time DESC')
    posts = c.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    conn = sqlite3.connect('posts.db')
    c = conn.cursor()

    # Get saved templates from the database
    c.execute('SELECT * FROM templates')
    templates = c.fetchall()
    conn.close()

    if request.method == 'POST':
        account = request.form['account']
        subreddit = request.form['subreddit']
        title = request.form['title']
        image_path = request.form['image_path']
        scheduled_time = request.form['scheduled_time']
        
        # Check if a template was selected
        template_id = request.form.get('template_id')

        conn = sqlite3.connect('posts.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO posts (account, subreddit, title, image_path, scheduled_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (account, subreddit, title, image_path, scheduled_time))
        conn.commit()
        conn.close()
        return redirect('/')

    return render_template('schedule.html', templates=templates)

if __name__ == '__main__':
    app.run(debug=True)
