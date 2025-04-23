from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import threading
import os
import time
from flask_cors import CORS
from datetime import datetime, timezone, timedelta

datetime.now(timezone.utc)


app = Flask(__name__)
socketio = SocketIO(app)
CORS(app)

commands_queue = []
client_status = {}

# Клієнт вважається неактивним після N секунд без пінгу
PING_TIMEOUT_SECONDS = 30


@app.route('/')
def index():
    return "PC Control Server is running."


@app.route('/get_commands', methods=['GET'])
def get_commands():
    if commands_queue:
        commands = commands_queue.copy()
        commands_queue.clear()
        return jsonify({'commands': commands})
    else:
        return jsonify({'commands': []}), 200


@app.route('/ping', methods=['POST'])
def ping():
    data = request.json
    client_id = data.get('client_id')

    if not client_id:
        return jsonify({'error': 'Missing client_id'}), 400

    client_status[client_id] = datetime.now(timezone.utc)
    print(f"✅ Ping received from {client_id} at {client_status[client_id]}")

    return jsonify({'status': 'pong'}), 200


@app.route('/active_clients', methods=['GET'])
def get_active_clients():
    now = datetime.now(timezone.utc)
    active_clients = []

    for client_id, last_ping in list(client_status.items()):
        if (now - last_ping).total_seconds() <= PING_TIMEOUT_SECONDS:
            active_clients.append({
                'client_id': client_id,
                'last_ping': last_ping.isoformat()
            })
        else:
            print(f"🕓 Client {client_id} timed out (last ping at {last_ping})")
            del client_status[client_id]

    return jsonify({'active_clients': active_clients})



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


@socketio.on('client_message')
def handle_client_message(data):
    print(f"Received message from client: {data.get('message')}")


@socketio.on('connect')
def handle_connect():
    sid = request.sid
    print(f"Client connected: {sid}")


@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected.")


def run():
    socketio.run(app, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    run()
