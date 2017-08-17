import sqlite3

class DBHelper():
    def connect(self):
        return sqlite3.connect('todo_tasks.db')


    def get_user(self, email):
        conn = self.connect()
        email = (email,)
        data = conn.execute('SELECT hash, salt FROM users WHERE email = ?', email).fetchall()
        user = None
        if data:
            user = {'salt': data[0][1], 'hashed': data[0][0]}
        return user



    def add_user(self, email, salt, hashed):
        data = (email, hashed, salt)
        conn = self.connect()
        conn.execute('INSERT into users(email, hash, salt) VALUES (?, ?, ?)', data)
        conn.commit()
        conn.close()

    def add_task(self, description, email):
        conn = self.connect()
        data = (description,email)
        conn.execute('INSERT into tasks(task_description, task_user) VALUES (?, ?)', data)
        conn.commit()
        conn.close()

    def get_all_tasks(self, email):
        conn = self.connect()
        email = (email,)
        data = conn.execute('SELECT task_description, task_id FROM tasks WHERE task_completed = 0 AND task_user = ? ORDER BY task_id',email).fetchall()
        conn.close()
        tasks = []
        for task in data:
            tasks[0:0] = [{'todo':task[0], 'id':task[1]}]
        return tasks

    def task_count(self, email):
        conn = self.connect()
        email = (email,)
        data = conn.execute('SELECT COUNT(*) FROM tasks WHERE task_completed = 0 AND task_user = ?', email).fetchall()
        conn.close()
        return data[0][0]

    def delete_task(self, description, email):
        conn = self.connect()
        data = (description,email)
        task_id = conn.execute('SELECT task_id FROM tasks WHERE task_description = ? AND task_user = ?',data).fetchall()
        if len(task_id) > 1:
            task_id = task_id[0][0]
            data = (description,task_id,email)
            conn.execute('DELETE from tasks WHERE task_description = ? AND task_id = ? AND task_user = ?', data)
        else:
            conn.execute('DELETE from tasks WHERE task_description = ? AND task_user = ?', data)
        conn.commit()
        conn.close()

    def complete_task(self, description,email):
        conn = self.connect()
        data = (description, email)
        task_id = conn.execute('SELECT task_id FROM tasks WHERE task_description = ? AND task_user = ?',data).fetchall()
        if len(task_id) > 1:
            task_id = task_id[0][0]
            data = (description,task_id,email)
            conn.execute('UPDATE tasks set task_completed = 1 WHERE task_description = ? AND task_id = ? AND task_user = ?',data)
        else:
            conn.execute('UPDATE tasks set task_completed = 1 WHERE task_description = ? AND task_user = ?',data)
        conn.commit()
        conn.close()

    def get_completed_tasks(self,email):
        conn = self.connect()
        email = (email,)
        data = conn.execute('SELECT task_description, task_id FROM tasks WHERE task_completed = 1 AND task_user = ? ORDER BY task_id',email).fetchall()
        conn.close()
        tasks = []
        for task in data:
            tasks[0:0] = [{'todo':task[0], 'id':task[1]}]
        return tasks

    def c_task_count(self, email):
        conn = self.connect()
        email = (email,)
        data = conn.execute('SELECT COUNT(*) FROM tasks WHERE task_completed = 1 AND task_user = ?', email).fetchall()
        conn.close()
        return data[0][0]

        
