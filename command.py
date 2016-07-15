
from normalize_output import normalize_output
import importlib
import sys

class command():

	def __init__(self):
		pass

	def command_list(self):
		commands = []
		with open('command_list.txt') as f:
			cmd = f.read().splitlines()
		for c in cmd:
			commands.append(c)
		return commands

	def get_command_list(self):
		commands = {}
		with open('command_list.txt') as f:
			cmd = f.read().splitlines()
		for c in cmd:
			cmd = str(c.replace("-","_"))
			commands[c] = cmd
		return commands


	# CLI general help
	# Might load this from a file later?
	def help(self):
		hlp = ("\nUsage:\n"
			"##########\n\n"
			"use 'ls' to list all avaliable commands and 'help <command>' to show command help\n")
		return hlp

	# outputs command help
	def command_help(self,cmd):
		instance = self.class_instance(cmd)
		run = getattr(instance,"help")
		return run()

	# show all avaliable commands on CLI
	def show_commands(self,cmds):
		norm_class = normalize_output()
		commands = []
		for c in cmds:
			commands.append(c)
		return norm_class.normalize_list(commands)

	# parses CLI input and proccess it
	def proccess_command(self,input):

		command_dict = self.get_command_list()
		input_list = input.split(" ")
		pass_var = {}
		var_val = ""

		if input == " " or "":
			return
		if len(input_list) == 1:

			if input_list[0] == "help":
				return self.help()

			elif input_list[0] == "exit":
				return sys.exit()

			elif input_list[0] == "ls":
				return self.show_commands(command_dict)

			else:

				cmd = input_list[0].replace("-","_")
				instance = self.class_instance(cmd)
				if instance == None:
					return "'"+ input_list[0] + "'" + " is a invalid command, use ls to list avaliable commands"
				elif instance.req_var:
						return "'" + input_list[0] + "'" + " requires variables, use 'help <command>' for usage"
				run = getattr(instance,cmd)
				output = run(pass_var)
				return output	

				
		elif len(input_list) >= 1:

			if input_list[0] == "help":
				if input_list[1] in command_dict:
					return self.command_help(command_dict.get(input_list[1]))
				return "'"+ input_list[1] + "'"+" is a invalid command, use ls to list avaliable commands"

			elif input_list[0] in command_dict:

				cmd = input_list[0].replace("-","_")
				instance = self.class_instance(cmd)

				#check if command needs variables
				if instance.req_var:
					req_variables = instance.req_variables
					#can it take opt var too?
					if instance.opt_var:
						opt_variables = instance.opt_variables
						for el in input_list:
							if el != input_list[0]:
								#is a flag 
								if (("-" in el) and (el in req_variables)) or (("-" in el) and (el in opt_variables)):
									var_val = el
								elif var_val != "":
									pass_var[var_val] = el
									var_val = ""
								elif el != "":
									return "'" + el + "'" + " is not a valid flag, use 'help <command>' for usage"
					elif not instance.opt_var:
						req_variables = instance.req_variables
						#get variables
						for el in input_list:
							#ignore command
							if el != input_list[0]:
								#is a flag 
								if (("-" in el) and (el in req_variables)) or (("-" in el) and (el in opt_variables)):
									var_val = el
								elif var_val != "":
									pass_var[var_val] = el
									var_val = ""
								elif el != "":
									return "'" + el + "'" + " is not a valid flag, use 'help <command>' for usage"

					run = getattr(instance,cmd)
					output = run(pass_var)
					return output

				#can command take variables?
				elif instance.opt_var:
					opt_variables = instance.opt_variables
					#get variables
					for el in input_list:
						#ignore command
						if el != input_list[0]:
							#is a flag 
							if("-" in el) and (el in opt_variables):
								var_val = el
							elif var_val != "":
								pass_var[var_val] = el
								var_val = ""
							elif el != "":
								return "'" + el + "'" + " is not a valid flag, use 'help <command>' for usage"

					#from here  command class will handle either empty dict or dict with flags
					run = getattr(instance,cmd)
					output = run(pass_var)
					return output


			else:
				return "'"+ input + "'"+" is a invalid command, use ls to list avaliable commands"


	def class_instance(self,cmd):
		try:
			module = importlib.import_module(cmd)
			instance = getattr(module,cmd)()
			return instance
		except Exception, e:
			return None

	

