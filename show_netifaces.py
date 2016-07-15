import netifaces 
from normalize_output import normalize_output

class show_netifaces():

	def __init__(self):
		self.req_var = False
		self.opt_var = True
		self.opt_variables = ["-i"]

	def help(self):
		hlp = ("\nDescription:\n"
				"############\n"
				"\nDefault command will show all avaliable netork interfaces, the "
				"command with the -v flag and a valid interface will show that "
				"interfaces details\n"
				"\nUsage:\n"
				"############\n"
				"\n'show-netifaces'\n"
				"'show-netifaces -i <interface>'\n")
		return hlp

	def show_netifaces(self,var):

		norm_class = normalize_output()

		#return specfic info about netiface
		if "-i" in var:
			try:
				addrs = netifaces.ifaddresses(var["-i"])
				return norm_class.normalize_json_list(addrs[netifaces.AF_INET])
			except Exception, e:
				return "'"+var["-i"]+"'"+" is not a valid interface" and e

		#get all netifaces
		else:
			return norm_class.normalize_list(netifaces.interfaces())

