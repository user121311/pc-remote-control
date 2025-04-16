# server.py
from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "PC Control Server is running."

@app.route('/shutdown', methods=['POST'])
def shutdown():
    os.system("shutdown /s /t 5")
    return jsonify({"status": "Shutting down..."})


@app.route('/open', methods=['POST'])
def open_app():
    app_path = request.json.get("app")
    try:
        subprocess.Popen(app_path)  # app_path має бути повним шляхом до .exe
        return jsonify({"status": f"Opened {app_path}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
