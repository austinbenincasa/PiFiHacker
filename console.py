from clint.textui import colored, puts
from command import command
import readline

cmd_history = "cmd_history"


def main():
    instance = command()
    # setting up command history 
    try:
        readline.read_history_file(cmd_history)
    except Exception:
        open("cmd_history", "a")
        readline.read_init_file(cmd_history)

    while True:
        cmd = raw_input(colored.green("PiHacker:~$ "))
        if cmd:
            output = instance.proccess_command(cmd)
            if output is not None:
                readline.write_history_file(cmd_history)
                print(output)
        else:
            cmd = raw_input(colored.green("PiHacker:~$ "))

if __name__ == '__main__':
    puts(colored.red("Welcome to PiHacker!"))
    puts()
    main()
