#!/bin/env python3

from netaddr import IPNetwork
import global_defs as gd
from time import sleep
import os

'''

Helper functions for numeric parsing of dash ranges in port selection feature


'''


def get_range(num_range):
# takes a 'port range' string and spreads it out ;; used inside iter_ports
	the_object = str(num_range)
	counter = 0
	the_list = []
	
	for x in range(len(the_object)):
		if the_object[x] == '-':
			counter = x
			break
	
	start_range = int(''.join(the_object[:x]))
	stop_range = int(''.join(the_object[x+1:]))
	
	for num in range(start_range,stop_range + 1):
		the_list.append(num)
		
	return the_list
	

def iter_ports(input_string):
# accepts single string, breaks into list items, parses them, returns a list with all desired ports
	#separate list items
	tmp_list, port_list = list(input_string.split(',')), []
	#iterate all items, spreading ranges where applicable
	for selection in range(len(tmp_list)):
		if '-' in list(tmp_list[selection]):
			for item in get_range(tmp_list[selection]):
				port_list.append(item)
		else:
			port_list.append(int(tmp_list[selection])) 
			
	return port_list
	
	
	
'''

Helper functions for numeric parsing of CIDR ranges in host selection feature

'''

def get_cidr(cidr_range):
# takes a CIDR range, splits it into individual IPs and returns that list
# used inside of func iter_hosts
	the_object = str(cidr_range)
	the_list = []
	for ip in IPNetwork(the_object):
		ip = str(ip)
		ip = ip.split('\'')
		for item in ip:
			item = str(''.join(item))
			the_list.append(item)

	return the_list


def iter_hosts(input_string):
# accepts single string, breaks into list items to parse and return a list with all desired hosts
	#separate list items
	tmp_list, host_list = list(input_string.split(',')), []
	#iterate all items, spreading CIDRs where applicable
	for selection in range(len(tmp_list)):
		if '/' in list(tmp_list[selection]):
			for item in get_cidr(tmp_list[selection]):
				host_list.append(item)
		else:
			host_list.append(str(tmp_list[selection]))
			
	return host_list
	
'''

Helper function for Mapper class to help break apart the input list, remove duplicates, and return a condensed object

'''
# This return will allow the looking up of 'Host:ALL_PORTS'
def split_port(input_list):
	# figure out how many of each host there are
	tmp_hosts = []
	tmp_hosts_ports = []
	hosts_ports = {}

	for item in input_list:
		h,p,d = item.split(':')
		
		if h not in tmp_hosts:
			tmp_hosts.append(h)
	
	# figure out which ports were responsive for each host
	for host in tmp_hosts:
		tmp_p = []
		for item in input_list:
			h,p,d = item.split(':')
			
			if h == host and p not in tmp_p:
				tmp_p.append(p)
				
		# convert to int, sort numerically, return to str
		tmp_p = [int(x) for x in tmp_p]
		tmp_p.sort()
		tmp_p = [str(x) for x in tmp_p]
		
		# creating a list now which will have format: ['host1:port1,port2', 'host2:port3,port6,port9']		
		tmp = str(host + ':' + ','.join(tmp_p))
		
		if tmp not in tmp_hosts_ports:
			tmp_hosts_ports.append(tmp)
			
	# turn it into a dictionary
	for item in tmp_hosts_ports:
		h,pl = item.split(':')
		hosts_ports[h] = pl
		
	return hosts_ports

'''

Helper function to attach data element to the Mapper object and return a nested dict for final usage

'''


def iter_dat(lwd):
# lwd is list with data
	
	ret_dic = {}
	

	for listing in lwd:
		h,p,d = listing.split(':')
		
		# if key doesn't exist create it, if it does exist add to it
		if h in ret_dic.keys():
			
			ret_dic[h][p] = d
		else:
			ret_dic[h] = {p:d}
	
	if gd.debug:
		print(f'\n\nLWD is: {lwd}\n\nRetDic is {ret_dic}\n\n')
	
	return ret_dic


'''

Helper function for credits

'''

def prn(string):

	# tool for printing strings letter by letter, while contained within some given margins for aesthetic purposes
	# margins solved via multi-line string formatting, this will follow the format the text is set in
	text = string
	my_list = []
	for letter in text:
		
		my_list.append(letter)
		show_list = ''.join(my_list)
		sleep(0.04)  #DEFAULT 0.04
		os.system('clear')
		print(show_list)



