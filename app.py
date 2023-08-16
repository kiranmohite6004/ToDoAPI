from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# database configuration
DB_NAME = 'todo.sqlite3'


# helper function to create a table if it doesn't exist
def create_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    status TEXT NOT NULL)''')
    conn.commit()
    conn.close()


# create table when an application starts, ideally it will create only at the first instance
create_table()


# GET ====> Route to display all Tasks and message if none exists
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


# POST ====> Route to add a new task
@app.route('/tasks', methods=['GET', 'POST'])
def add_tasks():

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form.get('title')
        description = request.form.get('description')
        status = request.form.get('status')
        c.execute("INSERT INTO tasks (name, description, status) VALUES (?, ?, ?)", (name, description, status))
        conn.commit()
        conn.close()
        return render_template("index.html", message="Task added successfully")

    else:

        c.execute("select * from tasks")
        data = c.fetchall()
        tasks = []
        for row in data:
            task = {'id': row[0], 'name': row[1], 'description': row[2], 'status': row[3]}
            tasks.append(task)
        conn.close()
        return render_template("index.html", tasks=tasks)


# PUT ====> Route to update an existing Task
@app.route('/task/<int:task_id>', methods=['GET', 'PUT'])
def update_task(task_id):
    print("inside update_task")
    print(request.form.get('name'))
    status = "DONE"
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
    conn.commit()
    conn.close()
    return jsonify({"messages": "Task updated successfully"})


# DELETE ====> Route to delete a Task
@app.route('/task/<int:task_id>', methods=['GET', 'DELETE'])
def delete_task(task_id):
    print("inside delete_task")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id, ))
    conn.commit()
    conn.close()
    return jsonify({"messages": "Task deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
