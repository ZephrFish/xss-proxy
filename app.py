#!usr/bin/env python
from flask import Flask, jsonify, abort, make_response, g, request
from flask.ext.cors import CORS
import sqlite3

DATABASE = 'tasks.db'

app = Flask(__name__)
CORS(app)
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
def connect_to_database():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = dict_factory
    return conn

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    get_db().commit()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/api/tasks/<int:client_id>', methods=['GET'])
def get_task(client_id):
    tasks = query_db('SELECT * FROM tasks WHERE client_id=? and progress=0',str(client_id))

    if len(tasks) == 0:
        abort(404)
    for task in tasks:
        query_db('update tasks set progress=1 where id=?',str(task['id']))
    return jsonify({'tasks': tasks})

@app.route('/api/tasks/confirm', methods=['POST'])
def confirm_task():
    if not request.json or not 'tasks' in request.json:
        abort(400)
    for task in request.json['tasks']:
        query_db('update tasks set progress=2 where id=?',str(task['id']))
    return jsonify({'result': True}), 201

@app.route('/api/tasks/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    if not request.json or not "response" in request.json:
        abort(400)
    headers = request.json['response'][0]['headers']
    body = request.json['response'][0]['body']
    query_db('update tasks set progress=3, headers=?, body=? where id=?',(str(headers),str(body),str(task_id)))
    return jsonify({'result': True}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)

"""
todo:

make bot finish tasks
    update task to "complete" (3)
    api endpoint for recieving post data (http response headers, httpresonse body)
make some kinda ui

"""