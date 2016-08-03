from normalize_output import normalize_output
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


class map_network():

    def __init__(self):
        self.req_var = True
        self.opt_var = False
        self.req_variables = ["-n"]

    def help(self):
        hlp = (
            "\nDescription:\n"
            "############\n"
            "\nThis command can be used to show all alive host currently "
            "connected to a specified network.\n"
            "\nUsage:\n"
            "############\n"
            "\n'map-network -n <network>'\n"
            "\n'map-network -n 192.168.1.*'\n"
        )
        return hlp

    def map_network(self, var):
        norm_class = normalize_output()
        if "-n" in var:
            try:
                ans, unans = srp(
                    Ether(dst="ff:ff:ff:ff:ff:ff") /
                    ARP(pdst=var["-n"]), timeout=2, verbose=False)
                hosts = []
                for snd, rcv in ans:
                    result = rcv.sprintf(r"%ARP.psrc% %Ether.src%").split()
                    hosts.append(result)
                if len(hosts) == 0:
                    output = []
                    output.append("1")
                    output.append("No hosts found on network, check network range")
                    return output
                return norm_class.normalize_network_map(hosts)

            except Exception:
                output = []
                output.append("1")
                output.append(e)
                return output