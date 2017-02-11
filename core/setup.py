import os


class setup():

    def setup(self):

        os.system("sudo apt-get install hostapd")
        os.system("sudo apt-get install dnsmasq")

        config = open("config.txt", "w")
        config.write("PiFiHacker has been set up do not remove this file")
        config.close()
