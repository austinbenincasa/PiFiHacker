from clint.textui import colored, puts
from command import command
from setup import setup
import readline
import os

cmd_history = "cmd_history"


def main():
    # setting up command history
    try:
        readline.read_history_file(cmd_history)
    except Exception:
        open("cmd_history", "a")
        readline.read_init_file(cmd_history)
    if os.path.isfile("config.txt"):
        pass
    else:
        puts(colored.cyan("Setting up PiFiHacker for you..."))
        instance = setup()
        instance.setup()
        puts(colored.cyan("PiFiHacker has been successfully setup"))

    instance = command()
    while True:
        cmd = raw_input(colored.green("PiFiHacker:~$ "))
        if cmd:
            readline.write_history_file(cmd_history)
            output = instance.proccess_command(cmd)
            if output is not None:
                if "1" == output[0]:
                	puts(colored.red(output[1]))
                else:
                	puts(output)
        else:
            cmd = raw_input(colored.green("PiFiHacker:~$ "))

if __name__ == '__main__':
    logo = (
        "\n\n\t########  #### ######## #### ##     ##"
        "\t    ###     ######  ##    ## ######## ########\n"
        "\t##     ##  ##  ##        ##  ##     ##"
        "\t   ## ##   ##    ## ##   ##  ##       ##     ##\n"
        "\t##     ##  ##  ##        ##  ##     ##"
        "\t  ##   ##  ##       ##  ##   ##       ##     ##\n"
        "\t########   ##  ######    ##  #########"
        "\t ##     ## ##       #####    ######   ########\n"
        "\t##         ##  ##        ##  ##     ##"
        "\t ######### ##       ##  ##   ##       ##   ##\n"
        "\t##         ##  ##        ##  ##     ##"
        "\t ##     ## ##    ## ##   ##  ##       ##    ##\n"
        "\t##        #### ##       #### ##     ##"
        "\t ##     ##  ######  ##    ## ######## ##     ##\n\n"
        "\tAustin Benincasa\tVersion: 1.0a" + "\t\t" + u"\u00a9" + "2016"
    )
    puts(colored.yellow(logo))
    puts()
    main()
