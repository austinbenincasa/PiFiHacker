from normalize_output import normalize_output
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


class map_network():

    def __init__(self):
        self.req_var = False
        self.opt_var = True
        self.opt_variables = ["-i","-n"]

    def help(self):
        hlp = (
            "\nDescription:\n"
            "############\n"
            "\nThis command can be used to show all alive host currently "
            "connected to a specified network. Can also be used to show "
            "which ports are open on a specified ip address\n"
            "\nUsage:\n"
            "############\n"
            "\n'map-network -n <network range>'\n"
            "\n'ex. map-network -n 192.168.1.*'\n"
            "\n'map-network -i <ip address>'\n"
            "\n'ex. map-network -i 192.168.1.1'\n"
        )
        return hlp

    def is_up(self,ip):
        """ Tests if host is up """
        icmp = IP(dst=ip)/ICMP()
        resp = sr1(icmp, timeout=10, verbose = False)
        if resp == None:
            return False
        else:
            return True

    def map_network(self, var):
        norm_class = normalize_output()
        if "-n" in var:
            if len(var) > 1:
                output = []
                output.append("1")
                output.append("Error: To many flags. Can only accept one.")
                return output
            try:
                ans, unans = srp(
                    Ether(dst="ff:ff:ff:ff:ff:ff") /
                    ARP(pdst=var["-n"]), timeout=2, verbose=False)
                hosts = []
                for snd, rcv in ans:
                    result = rcv.sprintf(r"%ARP.psrc% %Ether.src%").split()
                    hosts.append(result)
                if len(hosts) == 0:
                    output = []
                    output.append("1")
                    output.append("No hosts found on network, check network range")
                    return output
                return norm_class.normalize_network_map(hosts)

            except Exception:
                output = []
                output.append("1")
                output.append(e)
                return output

        if "-i" in var:
            scan = {}
            if len(var) > 1:
                output = []
                output.append("1")
                output.append("Error: To many flags. Can only accept one.")
                return output
            try:
                if self.is_up(var["-i"]):
                    closed_ports = 0
                    open_ports = []
                    conf.verb = 0 # Disable verbose in sr(), sr1() methods
                    start_time = time.time()
                    ports = [21,22,23,25,42,43,53,67,79,80,102,110,115,119,123,135,137,
                            143,161,179,379,389,443,445,465,636,993,995,1025,1080,1090,
                            1433,1434,1521,1677]
                    print("Scan has started...")
                    scan[var["-i"]] = []
                    for port in ports:
                        src_port = RandShort() # Getting a random port as source port
                        p = IP(dst=var["-i"])/TCP(sport=src_port, dport=port, flags='S') # Forging SYN packet
                        resp = sr1(p, timeout=2) # Sending packet
                        if resp.getlayer(TCP) == "<type 'NoneType'>":
                            pass
                        elif resp.haslayer(TCP):
                            if resp.getlayer(TCP).flags == 0x12:
                                send_rst = sr(IP(dst=var["-i"])/TCP(sport=src_port, dport=port, flags='AR'), timeout=1)
                                open_ports.append(port)
                    duration = time.time()-start_time
                    if len(open_ports) == 0:
                        scan[var["-i"]] = ["None"]
                    else:
                        scan[var["-i"]] = open_ports
                    
                    norm_class = normalize_output()
                    return norm_class.normalize_network_scan(scan)
                    print "%s Scan Completed in %fs" % (var["-i"], duration)
                else:
                    print "Host %s is down" % var["-i"]
                            
            except Exception, e:
                output = []
                output.append("1")
                output.append(e)
                print output
