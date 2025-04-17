import socketio
import os
import logging
import requests
import time

logging.basicConfig(level=logging.DEBUG)

# Створюємо об'єкт для WebSocket-з'єднання
sio = socketio.Client()

@sio.event
def connect():
    print('✅ Connected to server')

@sio.event
def disconnect():
    print('❌ Disconnected from server')

def execute_command(command):
    action = command.get('action')
    if action == 'shutdown':
        print('📥 Received shutdown command')
        os.system("shutdown /s /t 5")
    elif action == 'open':
        app_name = command.get('app_name')
        print(f'📥 Received open command for {app_name}')
        app_path = f'"C:\\Program Files (x86)\\Steam\\steamapps\\common\\wallpaper_engine\\wallpaper64.exe" "{app_name}"'
        os.system(f'start {app_path}')
    else:
        print("❓ Unknown command")

def get_commands_from_server():
    try:
        response = requests.get('http://localhost:5000/get_commands')
        if response.status_code == 200:
            commands = response.json()
            if commands:
                for command in commands:
                    execute_command(command)
            else:
                print("No new commands.")
        else:
            print("Failed to fetch commands from server.")
    except Exception as e:
        print(f"Error fetching commands: {e}")

def start_polling():
    while True:
        get_commands_from_server()
        time.sleep(5)  # Перевіряємо нові команди кожні 5 секунд

def main():
    try:
        # Підключаємося до серверу через WebSocket (можна для повідомлень)
        sio.connect('https://your-server-url.com')
        start_polling()  # Стартуємо polling для перевірки команд
        sio.wait()  # Чекаємо подій WebSocket
    except Exception as e:
        print("Exception during connect:", e)

if __name__ == '__main__':
    main()
