#!/bin/env python3

import os, socket, sys, argparse, json
from time import sleep
import helper, classes
import global_defs as gd
from time import sleep
import footers


'''

A network mapping tool


'''


# build argument parser
parser = argparse.ArgumentParser(add_help=False)

parser.add_argument('-p', '--ports', type=str)
parser.add_argument('-h', '--hosts', type=str)
parser.add_argument('-ss', '--service', action='store_true')
parser.add_argument('-dr', '--data-receipt', type=int)
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-vv', action='store_true')
parser.add_argument('--port-priority', action='store_true')
parser.add_argument('-d', '--delay', type=int)
parser.add_argument('-udp', action='store_true')
parser.add_argument('--help', action='store_true')
parser.add_argument('--debug', action='store_true')
parser.add_argument('-map', action='store_true')
parser.add_argument('--show-ports', action='store_true')
parser.add_argument('--show-hosts', action='store_true')
parser.add_argument('--show-data', action='store_true')
parser.add_argument('--clear', action='store_true')
parser.add_argument('-q','--quick', action='store_true')
parser.add_argument('--credits', action='store_true')

# parse passed argumentation
args = parser.parse_args()

if args.credits:
	print('\n')
	print(gd.pretty_banner)
	print('\n')
	sleep(2)
	helper.prn(footers.project_notes)
	sleep(2)
	print('\n')
	helper.prn(footers.citations)
	print('\n')
	sleep(2)
	helper.prn(gd.pretty_banner)
	exit()


if args.help:
	print(gd.help)
	exit()
if args.ports is not None:
	gd.port_list = helper.iter_ports(args.ports)	
	
	if gd.debug:
		print(f'\nargs.port is {args.ports}\n')
		print(f'\nport list is: {gd.port_list}\n')
		
if args.hosts is not None:
	gd.host_list = helper.iter_hosts(args.hosts)
	
	if gd.debug:
		print(f'\nargs.hosts is: {args.hosts}\n')
		print(f'\nHost list is: {gd.host_list}\n')
		
if args.service:
	gd.service_scan = True
if args.data_receipt is not None:
	gd.datar = args.data_receipt
if args.verbose:
	gd.verbosity = 1
if args.vv:
	gd.verbosity = 2
if args.port_priority:
	gd.port_priority = True
if args.delay is not None:
	gd.timeout_delay = args.delay
if args.udp:
	gd.tcp_scan = False
if args.debug:
	gd.debug = True
if args.quick:
	gd.quick = True

if args.map:
	gd.mapping = True
if args.show_ports:
	gd.map_show_ports = True
	gd.mapping_list['sp'] = gd.map_show_ports
if args.show_hosts:
	gd.map_show_hosts = True
	gd.mapping_list['sh'] = gd.map_show_hosts
if args.show_data:
	gd.map_show_data = True
	gd.mapping_list['sd'] = gd.map_show_data
if args.clear:
	gd.map_clear_data = True
	gd.mapping_list['cd'] = gd.map_clear_data
# only handle one map function at a time
if len(gd.mapping_list) > 1:
	print(f'\n\n One option at a time please \n\n')
	sleep(2)
	print(gd.help)
	exit()





### MAIN EXECUTION SEQUENCE ###

print('\n')
if not gd.quick:
	print(gd.pretty_banner)
	sleep(2)
	print('\n\n')

# if using probe function
if not gd.mapping:
# check all hosts, going port to port 
	try:
		if not gd.port_priority:
			for h in gd.host_list:
					for p in gd.port_list:
						# probe each instance, if alive send to a list
						probe = classes.Probe(h, p, gd.verbosity, gd.port_priority, gd.tcp_scan)
						life = probe.check_pulse()
						if life:
							# if service scan then do it
							if gd.service_scan:
								d = probe.check_banner(h,p)	
								d = d.decode()
							
								gd.living_list.append(str(h) + ':' + str(p) + ':' + str(d))
						
							# if not service scan then fill 'data' column with 'None'
							else:
								gd.living_list.append(str(h) + ':' + str(p) + ':' + 'None')
		
			# Output all to mapper class
			de = classes.mapper()
			de.input_data(gd.living_list)
			de.output_data()
			

				
											
		# check all ports, going host to host
		else:
			for p in gd.port_list:
				for h in gd.host_list:
					# probe each instance, if alive send to a list
					probe = classes.Probe(h, p, gd.verbosity, gd.port_priority, gd.tcp_scan)
					life = probe.check_pulse()
					if life:
						# if service scan then do it
						if gd.service_scan:
							d = probe.check_banner(h,p)
							d = d.decode()
						
							gd.living_list.append(str(h) + ' : ' + str(p) + ':' + str(d))	
					
						# if not service scan then fill 'data' column with 'None'
						else:
							gd.living_list.append(str(h) + ':' + str(p) + ':' + 'None')
						
			# Output all to mapper class
			de = classes.mapper()
			de.input_data(gd.living_list)
			de.output_data()
			

		

	except KeyboardInterrupt:
		exit()


# if using map function
elif gd.mapping:
	try:
		# load the objects back into workable memory
		mp = open('.mapperp','r+')
		md = open('.mapperd','r+')		
		mapo = json.load(mp)
		mada = json.load(md)
		mp.close()
		md.close()
		
		# form the workable object
		de = classes.mapper()
		de.remap(mapo,mada)
			
		if gd.map_show_ports:
			if args.hosts is not None:
				de.show_ports(helper.iter_hosts(args.hosts))
			else:
				de.show_ports()
			
		if gd.map_show_hosts:
			if args.ports is not None:
				de.show_hosts(helper.iter_ports(args.ports))
			
			else:
				de.show_hosts()
			
		if gd.map_show_data:
			if args.hosts is not None and args.ports is None:
				de.show_data(delimiter=helper.iter_hosts(args.hosts))
				
			elif args.hosts is None and args.ports is not None:
				de.show_data(retimiled=helper.iter_ports(args.ports))
				
			elif args.hosts is not None and args.ports is not None:
				de.show_data(delimiter=helper.iter_hosts(args.hosts),retimiled=helper.iter_ports(args.ports))
				
			else:
				de.show_data()			
		
		
	except KeyboardInterrupt:
		exit()

		



