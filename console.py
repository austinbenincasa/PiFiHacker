from clint.textui import colored, puts
from command import command
from tab_completer import tab_completer
import readline


def main():
    instance = command()
    cmd_list = instance.command_list()

    t = tab_completer()
    t.createListCompleter(cmd_list)

    readline.parse_and_bind("tab: complete")

    while True:
        readline.set_completer(t.listCompleter)
        cmd = raw_input(colored.green("PiHacker:~$ "))
        if cmd:
            output = instance.proccess_command(cmd)
            if output is not None:
                print(output)
        else:
            readline.set_completer(t.listCompleter)
            cmd = raw_input(colored.green("PiHacker:~$ "))

if __name__ == '__main__':
    puts(colored.red("Welcome to PiHacker!"))
    puts()
    main()
