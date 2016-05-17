import sqlite3
DATABASE = 'tasks.db'
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
conn = sqlite3.connect(DATABASE)
#conn.row_factory = dict_factory

def query_db(query):
    c=conn.cursor()
    c.execute(query)
    print c.fetchall()


c= conn.cursor()
for row in c.execute("SELECT * FROM tasks"):
    print row