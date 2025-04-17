import os
import logging
import requests
import time

logging.basicConfig(level=logging.DEBUG)

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
        response = requests.get('https://pc-remote-control.onrender.com/get_commands')

        if response.status_code == 200:
            commands = response.json()  # Це буде список рядків

            if commands:  # Перевірка, чи список не порожній
                for command in commands:
                    print(f"Received Command: {command}")
                    # Тут ви можете викликати відповідну функцію
                    # напр., if command == 'open': open_app()
            else:
                print("No new commands")
        else:
            print(f"Failed to fetch commands. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching commands: {str(e)}")

def start_polling():
    while True:
        get_commands_from_server()  # Перевіряємо нові команди кожні 5 секунд
        time.sleep(5)

def main():
    try:
        print("Starting command polling...")
        start_polling()  # Стартуємо polling для перевірки команд
    except Exception as e:
        print("Exception during polling:", e)

if __name__ == '__main__':
    main()
