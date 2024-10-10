from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>To-Do List</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                }
                .container {
                    max-width: 600px;
                    margin: auto;
                    background: white;
                    padding: 20px;
                    border-radius: 5px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    text-align: center;
                }
                form {
                    display: flex;
                    justify-content: space-between;
                }
                input[type="text"] {
                    flex: 1;
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                button {
                    padding: 10px;
                    background: #28a745;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                button:hover {
                    background: #218838;
                }
                ul {
                    list-style-type: none;
                    padding: 0;
                }
                li {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin: 10px 0;
                }
                a {
                    color: red;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>To-Do List</h1>
                <form action="/add" method="POST">
                    <input type="text" name="content" placeholder="Add a new task..." required>
                    <button type="submit">Add</button>
                </form>
                <ul>
                    {% for task in tasks %}
                        <li>
                            <form action="/edit/{{ task.id }}" method="POST" style="display: inline;">
                                <input type="text" name="content" value="{{ task.content }}" required>
                                <button type="submit">Edit</button>
                            </form>
                            <a href="/delete/{{ task.id }}">Delete</a>
                        </li>
                    {% endfor %}
                </ul>
            </div>
        </body>
        </html>
    ''', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task_content = request.form.get('content')
    if task_content:
        new_task = Task(content=task_content)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['POST'])
def edit(task_id):
    task = Task.query.get(task_id)
    task.content = request.form.get('content')
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    db.create_all()  # Create database tables
    app.run(debug=True)
