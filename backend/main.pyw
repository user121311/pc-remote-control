from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import threading

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://pc-remote-control.web.app"]}})
socketio = SocketIO(app, cors_allowed_origins="*")  # дозволяє WebSocket

connected_clients = []

@app.route('/')
def index():
    return "PC Control Server is running."

@app.route('/shutdown', methods=['POST'])
def shutdown():
    if connected_clients:
        socketio.emit('command', {'action': 'shutdown'})
        return jsonify({"status": "Sent shutdown command to client"})
    else:
        return jsonify({"error": "No clients connected"}), 400

@app.route('/open', methods=['POST'])
def open_app():
    app_name = request.json.get("app_name")
    if connected_clients:
        socketio.emit('command', {'action': 'open', 'app_name': app_name})
        return jsonify({"status": f"Sent open command for {app_name}"})
    else:
        return jsonify({"error": "No clients connected"}), 400

@socketio.on('connect')
def handle_connect():
    connected_clients.append(request.sid)
    print("Client connected:", request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    connected_clients.remove(request.sid)
    print("Client disconnected:", request.sid)

def run():
    socketio.run(app, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    run()
