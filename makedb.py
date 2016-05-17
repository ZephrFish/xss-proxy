import sqlite3

conn = sqlite3.connect('tasks.db')

c = conn.cursor()

# Create table
c.execute("DROP TABLE tasks")
c.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, client_id INTEGER, uri text, postdata text, progress int, headers text, body text)")

#dummy data

requests = [(1,'/dostuff1.html',None,0,),
(1,'/dostuff2.html?abc=123',None,0,),
(2,'/dostuff1.html','abc=123&foo=bar',0)]

c.executemany("INSERT INTO tasks (client_id,uri,postdata,progress) VALUES (?,?,?,?)", requests)



for row in c.execute('SELECT * FROM tasks'):
	print row
conn.commit()
c.close()
conn.close()