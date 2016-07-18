from normalize_output import normalize_output


class wifi_data():

    def __init__(self):
        self.req_var = False
        self.opt_var = True
        self.opt_variables = ["-n", "-p"]

    def help(self):
        hlp = (
            "\nDescription:\n"
            "############\n"
            "\nThis command can be used to save hacked wifi info."
            " Or the command can be used to view hacked wifi info.\n"
            "\nUsage:\n"
            "############\n"
            "\nTo add data:\n"
            "'ap-data -n <network> -p password'\n"
            "\nTo view data:\n"
            "'ap-data'\n"
        )
        return hlp

    def ap_data(self, var):
        norm_class = normalize_output()
        # add new ap data to file
        if "-n" and "-p" in var:
            try:
                with open("hacked_networks.txt", "a") as file:
                    file.write(var["-n"] + " " + var["-p"] + "\n")
                return "Data saved successfully"
            except Exception:
                with open("hacked_networks.txt", "r") as file:
                    file.write(var["-n"] + " " + var["-p"] + "\n")
                return "Data saved successfully"
        # show saved ap data
        else:
            try:
                with open("hacked_networks.txt", "r") as text:
                    norm_class.show_hacked_data(
                        dict(line.strip().split() for line in text))
            except Exception, e:
                return "Error: Hacked network data file not found" and e
