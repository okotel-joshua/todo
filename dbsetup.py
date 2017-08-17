import sqlite3
conn = sqlite3.connect('todo_tasks.db')

conn.execute('''CREATE TABLE IF NOT EXISTS  users(
user_id INTEGER PRIMARY KEY AUTOINCREMENT,
email TEXT NOT NULL,
hash TEXT NOT NULL,
salt TEXT NOT NULL
);''')

conn.execute('''CREATE TABLE IF NOT EXISTS  tasks(
task_id INTEGER PRIMARY KEY AUTOINCREMENT,
task_description TEXT NOT NULL,
task_user TEXT NOT NULL,
task_completed BOOLEAN DEFAULT(0)
);''')


conn.close()

