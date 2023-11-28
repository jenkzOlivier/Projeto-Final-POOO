import sqlite3
from flask import Flask, render_template, request, jsonify
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class TodoApp:
    def __init__(self):
        self.app = Flask(__name__)
        
        # Conectar ao banco de dados SQLite
        self.conn = sqlite3.connect('todos.db')
        self.cursor = self.conn.cursor()
        
        # Criar tabela se não existir
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                done INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

        # Rotas
        self.app.route('/')(self.index)
        self.app.route('/api/todos', methods=['GET'])(self.get_todos)
        self.app.route('/api/todos', methods=['POST'])(self.save_todo)
        self.app.route('/api/todos/<int:todo_id>', methods=['PUT'])(self.update_todo)
        self.app.route('/api/todos/<int:todo_id>', methods=['DELETE'])(self.delete_todo)

    def run(self):
        if __name__ == '__main__':
            self.app.run(debug=True)

    def index(self):
        return render_template('index.html')

    def get_todos(self):
        self.cursor.execute('SELECT * FROM todos')
        todos = self.cursor.fetchall()
        return jsonify(todos)

    def save_todo(self):
        data = request.get_json()
        text = data['text']
        done = data.get('done', 0)

        # Salvar no banco de dados
        self.cursor.execute('INSERT INTO todos (text, done) VALUES (?, ?)', (text, done))
        self.conn.commit()

        return jsonify({'status': 'success'})

    def update_todo(self, todo_id):
        data = request.get_json()
        text = data['text']

        # Atualizar no banco de dados
        self.cursor.execute('UPDATE todos SET text = ? WHERE id = ?', (text, todo_id))
        self.conn.commit()

        return jsonify({'status': 'success'})

    def delete_todo(self, todo_id):
        # Deletar do banco de dados
        self.cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
        self.conn.commit()

        return jsonify({'status': 'success'})

if __name__ == '__main__':
    todo_app = TodoApp()
    todo_app.run()
