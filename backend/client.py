import socketio
import os

sio = socketio.Client()

@sio.event
def connect():
    print('Connected to server')

@sio.event
def disconnect():
    print('Disconnected from server')

@sio.on('command')
def on_command(data):
    action = data.get('action')
    if action == 'shutdown':
        print('Received shutdown command')
        os.system("shutdown /s /t 5")
    elif action == 'open':
        app_name = data.get('app_name')
        print(f'Received open command for {app_name}')
        app_path = f'"C:\\Program Files (x86)\\Steam\\steamapps\\common\\wallpaper_engine\\wallpaper64.exe" "{app_name}"'
        os.system(f'start {app_path}')
    else:
        print("Unknown command")

def main():
    try:
        sio.connect('https://your-render-url.onrender.com')  # Заміни на свій
        sio.wait()
    except Exception as e:
        print("Connection error:", e)

if __name__ == '__main__':
    main()
