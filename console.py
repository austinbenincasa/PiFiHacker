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
        cmd = raw_input(colored.green("PiFiHacker:~$ "))
        if cmd:
            readline.write_history_file(cmd_history)
            output = instance.proccess_command(cmd)
            if output is not None:
                print(output)
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
