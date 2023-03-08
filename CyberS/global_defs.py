#!/bin/env python3

### GLOBALS ###

pretty_banner = '''

              _                 _____                           
             | |               /  ___|                          
  ___  _   _ | |__    ___  _ __\ `--.                           
 / __|| | | || '_ \  / _ \| '__|`--. \                          
| (__ | |_| || |_) ||  __/| |  /\__/ /                          
 \___| \__, ||_.__/  \___||_|  \____/                           
 _      __/ |   ____________  _ __   __       _____             
| |    |___/   |___  /| ___ \| |\ \ / /      /  ___|            
| |__   _   _     / / | |_/ /| | \ V / __  __\ `--.   ___   ___ 
| '_ \ | | | |   / /  |    / | | /   \ \ \/ / `--. \ / _ \ / __|
| |_) || |_| | ./ /   | |\ \ |_|/ /^\ \ >  < /\__/ /|  __/| (__ 
|_.__/  \__, | \_/    \_| \_|(_)\/   \//_/\_\\____/  \___| \___|
         __/ |                                                  
        |___/                                                   


'''

help = '''

	#####################################################################################
	#####################################################################################

	Probe Usage: ./cyberS.py -h 10.10.10.10 -p 1-65535
	
	Probe Options:	
					
		-p, --ports :: List of ports
		
		-h, --hosts :: List of hosts
		
		-ss, --service :: Service Scan
		
		-dr, --data-receipt :: Bytes to receive when service scanning (Default: 50)
		
		-v, --verbose :: Verbose output (-vv for extra verbose output)
		
		--port-priority :: Check port(s) while alternating hosts
		
		-d, --delay :: Seconds to wait for port response (Default: 20)
		
		-udp :: Test UDP ports
		
		-q, --quick :: Skip pretty_banner
		
		--credits :: Roll some boring stuff across the screen
		
		--debug :: Various outputs that might help while troubleshooting for development
		
	#####################################################################################
	#####################################################################################	
		
		Map operates on an object which is created as a result of probing. A file is
		generated during probing that can then be used to quickly lookup the data as
		the test progresses. You must run a probing sequence that returns at least one
		result for Map to be of any use.
		
	Map Usage: ./cyberS.py -map -h 10.11.12.13 --show-ports
	
	Map Options:
	
		-h :: Lookup by host
		
		-p :: Lookup by port
		
		--show-ports :: Shows "'Host:P80,P443,P9050','Host2:P22,P53'" 
				
				(can be delimited by -h)
		
		--show-hosts :: Shows active hosts
		
				(can be delimited by -p)
				
		--show-data :: Shows service info
		
				(can be delimited by -p and -h)
				
		--clear :: Dumps all data in the Map object



	#####################################################################################
	#####################################################################################
'''



verbosity = 0
tcp_scan = True
service_scan = False
datar = 50
port_priority = False
port_list = []
host_list = []
living_list = []
timeout_delay = 20
quick = False
debug = False
mapping = False
map_show_ports, map_show_hosts, map_show_data, map_clear_data = False, False, False, False
mapping_list = {}












