import os


class setup():

    def setup(self):
        dhcppath = str(os.path.abspath("dhcpd.conf"))
        hostpath = str(os.path.abspath("hostapd.conf"))

        #os.system("sudo apt-get install hostapd")
        #os.system("sudo apt-get install isc-dhcp-server")


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
            "DAEMON_CONF=" + hostpath + "\n"

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
            "RUN_DAEMON='YES'"
        )
        hostapd_default.write(config)
        hostapd_default.close()

        config = open("config.txt", "w")
        config.write("PiFiHacker has been set up do not remove this file")
        config.close()
