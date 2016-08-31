import netifaces
from normalize_output import normalize_output


class show_netifaces():

    def __init__(self):
        self.req_var = False
        self.opt_var = False

    def help(self):
        hlp = (
            "\nDescription:\n"
            "############\n"
            "\nDefault command will show all avaliable netork interfaces.\n"
            "\nUsage:\n"
            "############\n"
            "\n'show-netifaces'\n")
        return hlp

    def show_netifaces(self, var):

        norm_class = normalize_output()
        return norm_class.normalize_list(netifaces.interfaces())
