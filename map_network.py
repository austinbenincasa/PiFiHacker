from normalize_output import normalize_output
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


class map_network():

    def __init__(self):
        self.req_var = True
        self.opt_var = True
        self.req_variables = ["-n"]
        self.opt_variables = ["-a"]

    def help(self):
        hlp = (
            "\nDescription:\n"
            "############\n"
            "\nThis command can be used to show all alive host currently "
            "connected to a specified network.\n"
            "\nUsage:\n"
            "############\n"
            "\n'map-network -n <network range>'\n"
            "\n'map-network -n 192.168.1.*'\n"
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

        if "-a" in var:
            try:
                if self.is_up(var["-a"]):
                    closed_ports = 0
                    open_ports = []
                    conf.verb = 0 # Disable verbose in sr(), sr1() methods
                    start_time = time.time()
                    ports = range(1, 1024)
                    print "Host %s is up, start scanning" % var["-a"]
                    for port in ports:
                        src_port = RandShort() # Getting a random port as source port
                        p = IP(dst=var["-a"])/TCP(sport=src_port, dport=port, flags='S') # Forging SYN packet
                        resp = sr1(p, timeout=2) # Sending packet
                        if str(type(resp)) == "<type 'NoneType'>":
                            closed_ports += 1
                        elif resp.haslayer(TCP):
                            if resp.getlayer(TCP).flags == 0x12:
                                send_rst = sr(IP(dst=var["-a"])/TCP(sport=src_port, dport=port, flags='AR'), timeout=1)
                                open_ports.append(port)
                            elif resp.getlayer(TCP).flags == 0x14:
                                closed_ports += 1
                    duration = time.time()-start_time
                    print "%s Scan Completed in %fs" % (var["-a"], duration)
                    if len(open_ports) != 0:
                        for pop in open_ports:
                            print "%d open" % pop
                else:
                    print "Host %s is Down" % var["-a"]
                            
            except Exception, e:
                output = []
                output.append("1")
                output.append(e)
                print output