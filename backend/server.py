from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import threading
import os
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Список команд, які чекають виконання
commands_queue = []

@app.route('/')
def index():
    return "PC Control Server is running."

# API для отримання нових команд

@app.route('/get_commands', methods=['GET'])
def get_commands():
    if commands_queue:
        # Копіюємо команди та очищаємо чергу
        commands = commands_queue.copy()
        commands_queue.clear()
        return jsonify({'commands': commands})  # Повертаємо словник
    else:
        return jsonify({'commands': []}), 200  # Порожній список у словнику


# API для додавання нових команд
@app.route('/send_command', methods=['POST'])
def send_command():
    data = request.json
    if data:
        command = data.get('command')
        if command:
            commands_queue.append(command)
            return jsonify({"status": "Command added successfully!"}), 200
        return jsonify({"error": "No command provided"}), 400
    return jsonify({"error": "Invalid data"}), 400

# Обробка підключень від клієнтів
@socketio.on('client_message')
def handle_client_message(data):
    print(f"Received message from client: {data.get('message')}")

# Обробка підключень
@socketio.on('connect')
def handle_connect():
    sid = request.sid
    print(f"Client connected: {sid}")

# Обробка відключень
@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected.")

def run():
    socketio.run(app, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    run()
