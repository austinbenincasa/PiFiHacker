from normalize_output import normalize_output
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


class show_netstats():

    def __init__(self):
        self.req_var = True
        self.opt_var = True
        self.req_variables = ["-i"]
        self.opt_variables = ["-c"]
        self.ap_list = []

    def help(self):
        hlp = (
            "\nDescription:\n"
            "############\n"
            "\nCommand will show network usage for potential"
            " network deceptions."
            "Command can take a optional '-c' flag to set how many packets to "
            "listen for. Default value is 1000 packets\n"
            "\nUsage:\n"
            "############\n"
            "\n'show-netstats -i <interface>'\n"
            "'show-netstats -i <interface> -c <count>'\n"
        )
        return hlp

    # calc networks usage for each avalable
    def show_netstats(self, var):
        norm_class = normalize_output()
        if "-i" in var:
            # put device in monitor mode
            try:
                os.system("sudo ifconfig " + var["-i"] + " down")
                os.system("iwconfig " + var["-i"] + " mode monitor")
                os.system("sudo ifconfig " + var["-i"] + " up")
            except Exception, e:
                return e
            try:
                pkts = 1000
                if "-c" in var:
                    pkts = int(var.get("-c"))
                print("Gathering networks statistics...")
                sniff(iface=var["-i"], prn=self.PacketHandler, count=pkts)
                return norm_class.normalize_netstats_table(self.ap_list)
            except Exception, e:
                return "Error: Could not analyze networks" and e
        else:
            return "Error: Need to specifiy interface to analyze"

    def PacketHandler(self, pkt):
        present = False
        if pkt.haslayer(Dot11):
            if pkt.type == 0 and pkt.subtype == 8:
                info = {}
                for ap in self.ap_list:
                    if pkt.info == ap["name"]:
                        present = True
                        ap["packets"] = ap.get("packets") + 1
                if not present:
                        info["name"] = pkt.info
                        info["ssid"] = pkt.addr2
                        info["packets"] = 1
                        self.ap_list.append(info)
