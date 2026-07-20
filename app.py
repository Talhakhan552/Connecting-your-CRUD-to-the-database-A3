from flask import Flask, request, jsonify
import sqlite3
app = Flask(__name__)

# In-memory task list (will become a database in Assignment 2)
tasks = []
next_id = 1

# =============================================================================
# CRUD ENDPOINTS - these stay almost identical when we move to SQLite
# =============================================================================

# GET /tasks - Read all tasks
DATABASE = 'tasks.db'


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN DEFAULT 0
        )
    ''')

    cursor.execute('SELECT COUNT(*) FROM tasks')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO tasks (title, done) VALUES (?, ?)', ('Learn Flask', 0))
        cursor.execute('INSERT INTO tasks (title, done) VALUES (?, ?)', ('Build a CRUD API', 0))
        cursor.execute('INSERT INTO tasks (title, done) VALUES (?, ?)', ('Move to SQLite', 0))

    conn.commit()
    conn.close()



@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, done FROM tasks')
    rows = cursor.fetchall()
    conn.close()

    tasks = [{'id': row[0], 'title': row[1], 'done': bool(row[2])} for row in rows]
    return jsonify(tasks), 200

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, done FROM tasks WHERE id = ?', (task_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Task not found"}), 404

    task = {'id': row[0], 'title': row[1], 'done': bool(row[2])}
    return jsonify(task), 200

# POST /tasks - Create new task
@app.route('/tasks', methods=['POST'])
def create_task():
    global next_id
    
    data = request.get_json()
    
    # Validation: title must be present and non-empty
    if not data or not data.get('title') or not data['title'].strip():
        return jsonify({"error": "Title is required"}), 400
    
    new_task = {
        'id': next_id,
        'title': data['title'].strip(),
        'done': False
    }
    
    tasks.append(new_task)
    next_id += 1
    
    return jsonify(new_task), 201


# PUT /tasks/<int:task_id> - Update task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    
    data = request.get_json()
    
    # Validation: title must be present and non-empty
    if not data or not data.get('title') or not data['title'].strip():
        return jsonify({"error": "Title is required"}), 400
    
    task['title'] = data['title'].strip()
    task['done'] = data.get('done', task['done'])
    
    return jsonify(task), 200


# DELETE /tasks/<int:task_id> - Delete task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    
    tasks = [t for t in tasks if t['id'] != task_id]
    
    return '', 204




if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=3000)