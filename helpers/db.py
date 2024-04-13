import psycopg2
import os
uri = os.environ.get('DATABASE_URL')


class User:
    def __init__(self,id,instaid,email) -> None:
        self.id = id
        self.instaid = instaid
        self.email = email
        

class Mydb:
    def __init__(self):
        self.conn = psycopg2.connect(uri)
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users(
                ID SERIAL PRIMARY KEY,
                instaid VARCHAR(255),
                email VARCHAR(255)
            );''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS latest(ID int);
        ''')
    def add_user(self, instaid, email):
        self.cur.execute("INSERT INTO users(instaid, email) VALUES(%s, %s)", (instaid, email))
        self.conn.commit()
    def get_user(self,id):
        self.cur.execute("SELECT * FROM users WHERE id=%s",(id,))
        user = self.cur.fetchone()
        if user:
            return User(*user)
        return None
    def get_users(self):
        self.cur.execute("SELECT * FROM users")
        users = self.cur.fetchall()
        if users:
            return [User(*user) for user in users]
        return None
    def delete_user(self,id):
        self.cur.execute("DELETE FROM users WHERE id=%s",(id,))
        self.conn.commit()
    def truncate(self):
        self.cur.execute("TRUNCATE users")
        self.conn.commit()
    def close(self):
        self.cur.close()
        self.conn.close()
    def get_latest(self):
        self.cur.execute("SELECT * from latest")
        return self.cur.fetchone()[0]
    def set_latest(self,id):
        self.cur.execute("TRUNCATE latest")
        self.cur.execute(f"INSERT INTO latest(id) VALUES({id})")
        self.conn.commit()
        
db = Mydb()
db.close()
