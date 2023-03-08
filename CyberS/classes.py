#!/bin/env python3

import global_defs as gd
import socket
import helper
import json
import flatdict

'''

Class structures for CyberS


'''

# create a probe class with attributes: target_port, target_host, output_location


class Probe():

	def __init__(self, host, port, verbosity, priority, tcp_scan):
		self.host = str(host)		
		self.port = int(port)
		self.verbose = int(verbosity)
		self.priority = bool(priority)
		self.tcp_scan = bool(tcp_scan)
		

		
	def check_pulse(self) -> int:
	# checks if connection succeeds, returns boolean
	# each probe checks one port of one host and returns boolean
		if self.tcp_scan:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(gd.timeout_delay)
			try:
				s.connect((self.host,self.port))
			
				if self.verbose >= 1:
					print(f'TCP-Port {self.port} on host {self.host} is responsive\n')
			
				s.close()
				
				return 1 
			
			except:
				if self.verbose >= 2:
					print(f'TCP-Port {self.port} on host {self.host} has refused us\n')			
				
				return 0
	
		else:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.settimeout(timeout_delay)
			try:
				s.connect((self.host,self.port))
				
				if self.verbose >= 1:
					print(f'UDP-Port {self.port} on host {self.host} is responsive\n')
			
				s.close()
			
				return 1
			
			except:
				if self.verbose >= 2:
					print(f'UDP-Port {self.port} on host {self.host} has refused us\n')			
		
				return 0
				
				
	def check_banner(self,host,port):
	# takes a string item '127.0.0.1:80', splits it, checks it for banner
		
		#banner_host = input_string.split(':')[0]
		#banner_port = input_string.split(':')[0]
		
		#if gd.debug:
		#	print(f'BanHost: {banner_host}\nBanPort: {banner_port}')
		
		if self.tcp_scan:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(gd.timeout_delay)
			try:
				s.connect((host,port))
				s.send(b'Harrow?')
				data = s.recv(gd.datar)
			
				if self.verbose >= 1:
					print(f'TCP-Port {self.port} on host {self.host} is responding: \n\n {data}\n\n')
			
				s.close()
				
				if len(data) == 0:
					data = b'Unknown'
				
				return data 
			
			except:
				pass
	
		else:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.settimeout(timeout_delay)
			try:
				s.connect((host,port))
				s.send(b'Harrow?')
				data = s.recv(datar)
				
				if self.verbose >= 1:
					print(f'UDP-Port {self.port} on host {self.host} is responding: \n\n {data}\n\n')
			
				s.close()
			
				if len(data) == 0:
					data = b'Unknown'
				
				return data
			
			except:
				pass
				
	
class mapper():
# accepts host/port/data and generates a nested dictionary
# host is primary branch, then nested into the host is an open port as key + data as value
# will save data to a file, then can use the file to perform basic lookup operations on
	def __init__(self):
		self.map_dict_ports = {}
		self.map_dict_data = {}
		
		self.p_filter = []
		self.h_filter = []
		
		
	def input_data(self,input_list):
	# initial load in for creation of file while probing	
		self.map_dict_ports = helper.split_port(gd.living_list)
		
		self.map_dict_data = helper.iter_dat(gd.living_list)
		
	def remap(self,port_dic,data_dic):
	# alternative load in for parsing of data while mapping
	# also takes port and host filter, though only one would be used at a time	
		self.map_dict_ports = port_dic
		self.map_dict_data = data_dic
		
		
	def output_data(self):
	#!# IMPLEMENT A CHECKER SO WE CAN CHECK INCOMING SCANS AGAINST EXTANT DATA
	
		op = open('.mapperp','a+')
		op.write(json.dumps(self.map_dict_ports))
		op.close()	
					
		od = open('.mapperd', 'a+')
		od.write(json.dumps(self.map_dict_data))
		od.close()
		
		
		
	def show_ports(self,delimiter=0):
		
		# only shows the port-list where the host is found in user provided list
		if delimiter != 0:
			self.h_filter = delimiter
			
			if gd.debug:
				print(f'''
				
				H_Filter is: {self.h_filter}
				
				''')			
			
			
			print('\n')
			for host,ports in self.map_dict_ports.items():
				if host in self.h_filter:
					print(host + ' : ' + ports)
					print('\n')
					
		# just print the whole dictionary with line breaks
		else:
			print('\n')
			for host,ports in self.map_dict_ports.items():
				print(host + ' : ' + ports)
				print('\n')
		
		
	def show_hosts(self,delimiter=0):
	
		# only shows the host if that host has open port available in user provided list
		if delimiter != 0:
			self.p_filter = set(delimiter)
			
			if gd.debug:
				print(f'P_Filter is: {self.p_filter}')
			
			print('\n')
			for host,ports in self.map_dict_ports.items():
				tmp = [] 
				for entry in ports.split(','):
					tmp.append(int(entry))
				tmp = set(tmp)
				
				
				if gd.debug:
					print(f'TMP is: {tmp}')
				

				if self.p_filter.intersection(tmp):
					print(host)
					print('\n')
					
		# just print the whole dictionary with line breaks
		else:
			print('\n')
			for host in self.map_dict_ports:
				print(host)
				print('\n')
		
				
	def show_data(self,delimiter=0, retimiled=0):
		
		# if host filter only (delimiter)
		if delimiter != 0 and retimiled == 0:
			self.h_filter = set(delimiter)
			print('\n')
			for item in self.map_dict_data.keys():
				if item in self.h_filter:
					for meti in self.map_dict_data[item].items():
						print(f'''
						
	{item}
	
		{meti}
						
						''')
						print('\n')
			
			
			
		# if port filter only (retimiled)
		elif delimiter == 0 and retimiled != 0:
			self.p_filter = set(retimiled)
			print('\n')
			for item in self.map_dict_data.keys():
				# check if host even has ports to filter on
				if item in self.map_dict_ports:
					# prepare the comparison
					tmp = set(self.map_dict_ports[item].split(','))
					tmp = {int(x) for x in tmp}
					
					if gd.debug:
						print(tmp)
						print('\n')
					# filter on user input and display
					for meti in tmp.intersection(self.p_filter):
						print(f'''
	
	{item} :: {meti}				
				
			{self.map_dict_data[item][str(meti)]}                                                     
								                                                           
						                                                        					
						''')
					
			
			
			
			
		# if both filters
		elif delimiter != 0 and retimiled != 0:
			self.h_filter = set(delimiter)
			self.p_filter = set(retimiled)
			print('\n')
			for item in self.map_dict_data.keys():
				# filter for host
				if item not in self.h_filter:
					continue
				else:
					# check if host even has ports to filter on
					if item in self.map_dict_ports:
						# double check existence of host:port combo and display if extant
						for host in self.h_filter:
							for port in self.p_filter:
								if self.map_dict_data[host][str(port)]:
									print(f'''
									
	{host} :: {port}				
				
			{self.map_dict_data[host][str(port)]}									
									
									
									''')
					
			
			
			
			
			
			
			
			
			
			
		# if neither filter
		else:
			print('\n')
			fd = flatdict.FlatDict(self.map_dict_data,delimiter=' :: ')
			for item in fd.items():
				print(item)
				print('\n')


	def clear():
	
		mp = open('.mapperp','w')
		md = open('.mapperd','w')
		mp.close()
		md.close()






















	
#debug
'''
probe1 = Probe(631,'127.0.0.1',2,False,True)
probe2 = Probe(3333,'127.0.0.1',2,False,True)
testx = probe1.pulse_check()
testy = probe2.pulse_check()

print(f'Printing testx should be true: {testx}')
print(f'Printing testy should be false: {testy}')

dicti = {}
dicti['test'] = 'case'
dicti['test2'] = 'case2'
dicti['test2'] = {'case2':'data'}
print(f' dicti is: {dicti}')

print(dicti['test'])			# return case
print(dicti['test2']['case2'])		# return data
print(dicti['test2'])			# return case2:data
'''
# create a receiver class that accepts attributes from the return values of the probe object



# for main call a loop initiating a multi-threaded loop that sends probes to each target and passes the results into a receiver object; that object is stored and can then have transforms done to it -- each scan is a new object, not each probe; so the object identifies an entire host, and if many hosts then many objects
