import subprocess

def run_commands():
    commands = [
        'flask db init',
        'flask db migrate -m "initial migrations"',
        'flask db upgrade'
    ]

    for command in commands:
        try:
            print(f"Executing command: {command}")
            subprocess.run(command, shell=True, check=True)
            print("Command executed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {command}")
            print(e)
            return

if __name__ == "__main__":
    run_commands()
