import sys
import subprocess

def get_command(arg1, arg2):
    print("Get command executed with args:", arg1, arg2)

def set_light_state(light_state):
    try:
        if light_state == 1:
            print("Turning on the light...")
            subprocess.run(['python3', '/var/lib/homebridge/irrp.py', '-p', '-g17', '-f', 'codes', 'light:on'], check=True)
        elif light_state == 0:
            print("Turning off the light...")
            subprocess.run(['python3', '/var/lib/homebridge/irrp.py', '-p', '-g17', '-f', 'codes', 'light:off'], check=True)
        else:
            raise ValueError("Invalid light state. Use 0 to turn off or 1 to turn on.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while trying to change the light state: {e}")
        raise

def main():
    if len(sys.argv) < 5:
        print("Usage: script.py [Get|Set] <arg1> <arg2> <0|1>")
        sys.exit(1)

    command = sys.argv[1]
    arg1 = sys.argv[2]
    arg2 = sys.argv[3]

    try:
        light_state = int(sys.argv[4])
    except ValueError:
        print("Invalid light state. Use 0 to turn off or 1 to turn on.")
        sys.exit(1)

    if command == 'Get':
        get_command(arg1, arg2)
    elif command == 'Set':
        set_light_state(light_state)
    else:
        print("Invalid command. Use 'Get' or 'Set'.")
        sys.exit(1)

if __name__ == "__main__":
    main()
