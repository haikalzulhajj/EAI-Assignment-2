from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from datetime import datetime
import functools

app = Flask(__name__)

app.config ['MYSQL_HOST'] = 'localhost'
app.config ['MYSQL_USER'] = 'root'
app.config ['MYSQL_PASSWORD'] = ''
app.config ['MYSQL_DB'] = 'to_do_list'
app.config ['MYSQL_PORT'] = 3308
mysql = MySQL(app)

def token_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kws):
        token = request.headers.get('Authorization')
        if token != 'secretoken12121212':
            return jsonify({'message': 'Unauthorized', 'status_code': 401}), 401
        return f(*args, **kws)
    return decorated_function

@app.route('/')
def root():
    return "Welcome to RESTful API Assignment 2"

@app.route('/task_name', methods=['GET'])
@token_required
def task_name():
    auth = request.authorization
    query_parameters = request.args
    task_id = query_parameters.get('task_id')
    task_detail = query_parameters.get('task_detail')
    
    query = "SELECT * FROM taskname"
    to_filter = []
    
    if task_id:
        query += ' WHERE task_id=%s'
        to_filter.append(task_id)
    elif task_detail:
        query += ' WHERE task_detail=%s'
        to_filter.append(task_detail)
    
    cursor = mysql.connection.cursor()
    cursor.execute(query, to_filter)
    results = cursor.fetchall()
    

    column_names = [i[0] for i in cursor.description]
    data = [dict(zip(column_names, result)) for result in results]
    
    response = {
        'data': data,
        'message': 'Data retrieved successfully' if data else 'No data found',
        'status_code': 'completed',
        'timestamp': datetime.now().isoformat()
    }
    return jsonify(response)

@app.route('/task_add', methods=['POST'])
def add_task():
    task_detail = request.json['task_detail']
    task_id = request.json['task_id']
    task_name = request.json['task_name']
    
    cursor = mysql.connection.cursor()
    sql = "INSERT INTO taskname (task_detail, task_id, task_name) VALUES (%s, %s, %s)"
    val = (task_detail, task_id, task_name)
    
    cursor.execute(sql, val)
    mysql.connection.commit()
    
    response = {
        'message': 'Data added successfully',
        'status_code': "Completed",
        'timestamp': datetime.now().isoformat()
    }
    return jsonify(response)

@app.route('/task_detail', methods=['GET'])
def task_detail():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM taskname WHERE task_id = %s"
        val = (request.args['id'])
        cursor.execute(sql, val)

        column_names = [i[0] for i in cursor.description]

        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))

        return jsonify(data)

        cursor.close()

@app.route('/task_delete', methods= ['DELETE'])
def task_delete():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM taskname WHERE task_id = %s"
        val = (request.args['id'])
        cursor.execute(sql, val)
    
    mysql.connection.commit()

    return jsonify({'message' : 'Data deleted successfully'})
    
    cursor.close()

@app.route('/task_update', methods=['PUT'])
def task_update():
    task_id = request.json['task_id']
    task_detail = request.json['task_detail']
    task_name = request.json['task_name']
    
    cursor = mysql.connection.cursor()
    sql = "UPDATE taskname SET task_detail = %s, task_name = %s WHERE task_id = %s"
    val = (task_detail, task_name, task_id)
    
    cursor.execute(sql, val)
    mysql.connection.commit()
    
    if cursor.rowcount == 0:
        return jsonify({'message': 'No task found with the given ID', 'status_code': 404}), 404

    return jsonify({'message': 'Task updated successfully', 'status_code': 200, 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50, debug=True)