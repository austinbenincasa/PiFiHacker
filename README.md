# PiFiHacker

Is a python 2.7 CLI program developed to penetrate wifi networks. PiFiHacker stands up a Evil Twin used to decieve a unsuspecting victim. The tool is currently only been tested on Ubuntu 16.04 using python 2.7. May work on other linux distros but is not compatiable with Windows.

### Example Commands:
- show-netifaces
- show-networks
- show-netstats
- netspoof

### Required Python libraries:
- Clint
- Wifi
- Netifaces
- Scapy 

### Ubuntu Dependencies:
- Hastapd
- Dnsmasq

### Required Hardware:
- 2 Wifi cards capable of packet injection and AP mode
- Software tested with 2 Alfa AWUSO36NH Cards

### Hints:
If your wifi cards are showing up as long names add:
- ```SUBSYSTEM=="net", ACTION=="add", ATTR{address}=="card mac address", NAME="some name"```
to the file /etc/udev/rules.d/10-network.rules than reboot the system 
