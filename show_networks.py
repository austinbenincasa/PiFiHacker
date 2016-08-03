from wifi import Cell
import os
from normalize_output import normalize_output


class show_networks():

    def __init__(self):
        self.req_var = True
        self.opt_var = False
        self.req_variables = ["-i"]

    def help(self):
        hlp = (
            "\nDescription:\n"
            "############\n"
            "\nCommand will show all near by wifi networks\n"
            "\nUsage:\n"
            "############\n"
            "\n'show-networks -i <interface>'\n"
        )

        return hlp

    def show_networks(self, var):

        if "-i" in var:
            # make sure wifi is in managed mode
            try:
                os.system("sudo ifconfig " + var["-i"] + " down")
                os.system("iwconfig " + var["-i"] + " mode managed")
                os.system("sudo ifconfig " + var["-i"] + " up")
            except Exception:
                output = []
                output.append("1")
                output.append("Error: could not change interface settings")
                return error
            networks_info = []
            try:
                wifi_list = Cell.all(var["-i"])
                for wifi in wifi_list:
                    network_info = {}
                    network_info["name"] = wifi.ssid
                    network_info["address"] = wifi.address
                    network_info["channel"] = wifi.channel
                    if wifi.encrypted == 1:
                        network_info["encrypted"] = "Yes"
                        network_info["type"] = wifi.encryption_type
                    else:
                        network_info["encrypted"] = "No"
                        network_info["type"] = "N/A"
                    network_info["signal"] = wifi.signal

                    networks_info.append(network_info)
                norm_class = normalize_output()
                return norm_class.normalize_wifi_table(networks_info)

            except Exception:
                output = []
                output.append("1")
                output.append("Cannot show networks on interface "
                "'" + var["-i"] + "'")
                return output

        else:
            output = []
            output.append("1")
            output.append("Error: Need to specifiy iface to listen on")
            return output
