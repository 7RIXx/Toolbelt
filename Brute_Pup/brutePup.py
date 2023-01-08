#!/bin/python3

### START HEADERS ###

'''

I was in the process of building a tool called onionHunter.py that bruteforced strings of given parameters, passed them as .onion links, attempted to connect to them and if successful went to the homepage and GoWitnessed the content there. Having some trouble I was searching forums and came across some content that made me aware of the ethical/legal risks inherent in building such a tool.

I decided to scrap the project but wanted to save some of the modules I wrote so I just compiled them into this script that points the strings at clearnet instead and called it uselessBrute.py.

Then I started really getting in the zone with features and it reached a certain point-of-scale that it wasn't so useless/pointless anymore and actually had some potential to be a real toolbelt tool for pentesting! Needing a new name I approached my wife and explained what I had done, she sat there trying very hard to look interested as I explained the pythonic complexities of my program and the naming dilemma I now faced. Her suggestion was brutePup because she thinks puppies are cute.. So here we are; while it may only be a pup, at least it's a brute -- Welcome to brutePup.py! 

'''

'''
POTENTIAL EVOLUTIONS LIST

1) Add a fuzzing option

2) Add a progress bar

3) Add a pause/resume feature (like Feroxbuster) or maybe just a brutePup.state file

4) For output file globals use some type of string formatting to allow greater flexibility in combinations and granular control

5) Add optionality to pipe into TOR

'''

### END HEADERS ###


### START IMPORTS ###

from string import ascii_lowercase as little_letters
from string import ascii_uppercase as big_letters
from string import punctuation as symbols
from string import digits as numbers
import requests, threading, argparse, os, errno, multiprocessing
from time import sleep
from ratelimiter import RateLimiter
import itertools
from datetime import datetime

### END IMPORTS ###


### START GLOBAL ENVIRONMENT ###

pretty_banner = '''

                                                                                                                            
88                                                        88888888ba                                                        
88                                      ,d                88      "8b                                                       
88                                      88                88      ,8P                                                       
88,dPPYba,   8b,dPPYba,  88       88  MM88MMM  ,adPPYba,  88aaaaaa8P'  88       88  8b,dPPYba,                              
88P'    "8a  88P'   "Y8  88       88    88    a8P_____88  88""""""'    88       88  88P'    "8a                             
88       d8  88          88       88    88    8PP"""""""  88           88       88  88       d8                             
88b,   ,a8"  88          "8a,   ,a88    88,   "8b,   ,aa  88           "8a,   ,a88  88b,   ,a8"                             
8Y"Ybbd8"'   88           `"YbbdP'Y8    "Y888  `"Ybbd8"'  88            `"YbbdP'Y8  88`YbbdP"'                              
88                           888888888888  88888888ba   88  8b        d8            88  ad88888ba                           
88                                   ,8P'  88      "8b  88   Y8,    ,8P             88 d8"     "8b                          
88                                  d8"    88      ,8P  88    `8b  d8'                 Y8,                                  
88,dPPYba,   8b       d8          ,8P'     88aaaaaa8P'  88      Y88P      8b,     ,d8  `Y8aaaaa,     ,adPPYba,   ,adPPYba,  
88P'    "8a  `8b     d8'         d8"       88""""88'    88      d88b       `Y8, ,8P'     `"""""8b,  a8P_____88  a8"     ""  
88       d8   `8b   d8'        ,8P'        88    `8b    ""    ,8P  Y8,       )888(             `8b  8PP"""""""  8b          
88b,   ,a8"    `8b,d8'        d8"          88     `8b   aa   d8'    `8b    ,d8" "8b,   Y8a     a8P  "8b,   ,aa  "8a,   ,aa  
8Y"Ybbd8"'       Y88'        8P'           88      `8b  88  8P        Y8  8P'     `Y8   "Y88888P"    `"Ybbd8"'   `"Ybbd8"'  
                 d8'                                                                                                        
                d8'  

   	
   			with a very special thanks to Varga and SensePost!




'''



help = '''

Default Usage: ./brutePup.py

Extended Usage: ./brutePup.py -s [-t | -mn | -mx | -d | -o | -cs | -l | -sn | -v] 
			      
			      -s -dr [-sn | -v]
			      
			      --redirection
			      
			      -h

	-t, --threads :: Run multi-threaded requests (Default: 100)
	                |
	                |__/\_  Recommended range: 1-250 (as tested on Intel i7x8)
	
	-s, --sitelist :: Pass a wordlist instead of bruteforcing sites
	                |
	                |__/\_  Accepts classic wordlist, entries separated by newline
	                
	                	Entries should be domain name only, do not include SSL/TLD
	                	
	                		Eg. "google"
	                		
	-sn, --snap :: Screenshot sites
	
	-ssl, --secure :: SSL engaged, boolean-plus (Default: 1)
	                |
	                |__/\_  Key :: Value
	                
	                         0  ::  http
	                         1  ::  https
	                 |        
	                 |__/\_ To pass alternative prefixes enter as a string:
	                 
	                 	eg. 'ftp'                
	                 
	-mn, --minChar :: Minimum length of bruteforced string (Default: 1)

	-mx, --maxChar :: Maximum length of bruteforced string (Default: 2)

	-d, --timeout :: Seconds to wait for each request response (Default: 1)

	-o, --output :: Output log folder (Default: ./data)
	
	-tld, --toplevel :: Top Level Domain to use (Default: .com)
	
	-cs, --charset :: Character set for bruteforcing (Default: Lower Only)
	                |
	                |__/\_  Key :: Value
	                
	                         0  ::  Lowercase
	                         1  ::  Uppercase
	                         2  ::  Numbers
	                         3  ::  Symbols
	                 |        
	                 |__/\_ To Pass multiple charsets enter as such:
	                 
	                 		-cs 012 :: Lower + Upper + Numbers
	                 		
	                 		-cs 302 :: Symbols + Lower + Numbers
	                 |        
	                 |__/\_ To pass a custom charset, please enter a string,
	                 	 as such:
	                 
	                 		-cs '%$^&*dhfKJG3478'	                 		

	-e, --errorfile :: Error Logging File (Default: ./data/sites.errors)
	
	--redirection :: Redirect bruteforce into file for processing with sitelist feature (-s)
	                |
	                |__/\_  PLEASE BE CAREFUL WITH THIS -- this can generate an
	                		
	                obscenely large file on your computer, be aware of the total
	                
	                potential MB/GB/TB/PB you are requesting based on your parameters 
	
	-dr, --dirbust :: Pass a wordlist to directory bust with
	                |
	                |__/\_  Accepts classic wordlist, entries separated by newline
	                
	                	Requires site(s) list to be passed in -s
	                	
	-v, --verbose :: Watch your screen fill up with all the $1cK requests you're making!

	-h, --help :: Show this display

'''


set_min = 1
set_max = 2

timeoutdelay = 1
threadlimit = 100
error_queue = []
error_report = {}

char_set = list(little_letters)
tmp_list = []
set_list = []
live_tar = []
sitelist = []
dirlist = []
dirbustinglist = []
snap = False
ssl_prefix = 'https://'
tld = '.com'

redirection = False

log_folder = './data'
log_file = log_folder + '/' + 'sites' + '.live'
log_errors = './data/sites.errors'
screen_folder = log_folder + '/' + 'screenshots'
subdirs_file = log_folder + '/' + 'subdirs.live'
brute_direction = log_folder + '/' + 'sitelist.unchecked'
targetting_file = log_folder + '/' + 'sites' + '.targetting'

# build argument parser
parser = argparse.ArgumentParser(add_help=False)

parser.add_argument('-t', '--threads', type=int)
parser.add_argument('-s', '--sitelist', type=str)
parser.add_argument('-sn', '--snap', action='store_true')
parser.add_argument('-ssl', '--secure', type=str)
parser.add_argument('-mn', '--minChar', type=int)
parser.add_argument('-mx', '--maxChar', type=int)
parser.add_argument('-d', '--timeout', type=float)
parser.add_argument('-o', '--output', type=str)
parser.add_argument('-tld', '--toplevel', type=str)
parser.add_argument('-cs', '--charset', type=str)
parser.add_argument('-e', '--errorfile', type=str)
parser.add_argument('--redirection', action='store_true')
parser.add_argument('-dr', '--dirbust', type=str)
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-h', '--help', action='store_true')

# parse passed argumentation
args = parser.parse_args()

if args.threads is not None:
	threadlimit = args.threads

if args.snap:
	snap = True
if args.secure is not None:
	if args.secure == '0':
		ssl_prefix = 'http' + '://'
	elif args.secure == '1':
		ssl_prefix == 'https' + '://'
	else:
		ssl_prefix == str(args.secure) + '://'
if args.minChar is not None:
	set_min = args.minChar
if args.maxChar is not None:
	set_max = args.maxChar
if args.timeout is not None:
	timeoutdelay = args.timeout
if args.output is not None:
	log_folder = args.output
if args.toplevel is not None:
	tmp = list(args.toplevel)
	# up to six in case someone does want to pass .onion
	if tmp[0] != '.' or len(tmp) > 6:
		print(help)
		exit()
	else:
		tld = str(args.toplevel)
if args.sitelist is not None:
	try:
		wl = open(args.sitelist,'r')
		for site in wl:
			sitelist.append(ssl_prefix + site.strip('\n') + tld)
		wl.seek(0)
		wl.close()
	except:
		pass
if args.charset is not None:
	# catch argument and sort the numbers ascending
	pass_flag = args.charset
	catch_flag = []
	for x in pass_flag:
		catch_flag.append(x)
	catch_flag.sort()
	catch_flag = ''.join(catch_flag)
	
	
	# designate charset based on passed argument
	if catch_flag == '0':
		char_set = list(little_letters)
	elif catch_flag == '1':
		char_set = list(big_letters)
	elif catch_flag == '2':
		char_set = list(numbers)
	elif catch_flag == '3':
		char_set = list(symbols)
		
	elif catch_flag == '01':
		char_set = list(little_letters + big_letters)
	elif catch_flag == '02':
		char_set = list(little_letters + numbers)
	elif catch_flag == '03':
		char_set = list(little_letters + symbols)
	elif catch_flag == '12':
		char_set = list(big_letters + numbers)
	elif catch_flag == '13':
		char_set = list(big_letter + symbols)
	elif catch_flag == '23':
		char_set = list(numbers + symbols)
		
	elif catch_flag == '012':
		char_set = list(little_letters + big_letters + numbers)
	elif catch_flag == '013':
		char_set = list(little_letters + big_letters + symbols)
	elif catch_flag == '023':
		char_set = list(little_letters + numbers + symbols)
	elif catch_flag == '123':
		char_set = list(big_letters + numbers + symbols)
		
	elif catch_flag == '0123':
		char_set = list(little_letters + big_letters + symbols + numbers)
	else:
		char_set = list(args.charset)
		
if args.errorfile is not None:
	log_errors = str(args.errorfile)
if args.redirection:
	redirection = True
if args.dirbust is not None:
	try:
		dl = open(args.dirbust,'r')
		for dirs in dl:
			dirlist.append('/'+str(dirs.strip('\n')))
		dl.seek(0)
		dl.close()
	except:
		pass	
if args.help is True:
	print(help)
	exit()
	

### END GLOBAL ENVIRONMENT ###


### START EXECUTION ENVIRONMENT ###	
	
# create folder and files to hold things
try:
	os.mkdir(log_folder)

except OSError as er:
	if er.errno == errno.EEXIST:
		print(f'''\n\n 
		
	Output directory \"{log_folder}\" already exists and will be used;
	screenshots of the same site will be overwritten. 
	
	If the files \"{log_file}\" and \"{log_errors}\" also exist, they
	will be appended to.	
		
		\n\n''')
		
		sleep(3)
		

try:
	le = open(log_errors,'a')
except OSError as er:
	if er.errno == errno.EEXIST:
		le = open(log_errors,'x')
		

try:
	lf = open(log_file,'a')
except OSError as er:
	if er.errno == errno.EEXIST:
		lf = open(log_file,'x')
		
try:
	lt = open(targetting_file,'a')
except OSError as er:
	if er.errno == errno.EEXIST:
		lf = open(targetting_file,'x')


### END EXECUTION ENVIRONMENT ###

	

### START CRAFT PRIMARY UTILITIES ###


# create rate limiter
rate_limiter = RateLimiter(max_calls=threadlimit, period=1)

# creates the list of targets
def bruteforce():

	return(''.join(candidate)
		for candidate in itertools.chain.from_iterable(itertools.product(char_set, repeat=i)
		for i in range(set_min,set_max + 1)))


# sends crafted GET, utilized inside of ping_site function
def send_request(request_target):
	try:
		# ping site, check for 200 status response, if alive add to list
		r = requests.get(request_target, timeout=timeoutdelay)
		
		if r.status_code == 200:
			live_tar.append(request_target)

			
	# push errors to the error_queue
	except Exception as exc:
		error_queue.append(exc)
	
# sends crafted GET, using send_request function, to check if site is alive
def ping_site(ping_targets):
	open_fire = list(ping_targets)
	threads = []
	
	for x in range(len(open_fire)):
		with rate_limiter:
			tar = open_fire[x]
			if args.verbose:
				print('\nPinging ' + tar + ' ...')
			t = threading.Thread(target=send_request, args=(tar,))

			threads.append(t)
			t.start()

	for t in threads:
		t.join()
				
# custom func to handle the yield return from bruteforce()
def ping_site_brute(ping_target):
	open_fire = str(ping_target)
	threads = []
	
	with rate_limiter:
		tar = open_fire
		if args.verbose:
			print('\nPinging ' + str(tar) + ' ...')
		t = threading.Thread(target=send_request, args=(tar,))

		threads.append(t)
		t.start()

	for t in threads:
		t.join()




# build error logging function
def error_logging(targets):
	dying = targets
	for ailment in dying:
		lf.write(str(ailment) + '\n')

		
# build logging for live responses
def live_logging(targets):
	living = targets
	for site in living:
		lf.write(str(site) + '\n')

# build targetting file for future use
def target_logging(targets):
	targetting = targets
	slice_from = len(ssl_prefix)
	slice_to = len(tld)
	for site in targetting:
		lt.write(str(site[slice_from:-slice_to]) + '\n')
	
	
	
		
# take sites which are confirmed alive and screenshots their landing page
def snapshot(snap_targets):
	reconnoiter = list(snap_targets)
	for shots in range(len(reconnoiter)):
		# custom craft command to pass to system
		cmd = 'gowitness single ' + reconnoiter[shots] + ' -P ' + screen_folder + ' --disable-db'

		

		try:
			os.system(cmd)
		except KeyboardInterrupt:
			print('\n\nUser Interruption\n\n')
		except:
			print('''\n\n
		
	GoWitness Error.
	
	Please ensure that GoWitness is properly installed and within your $PATH
	
	https://github.com/sensepost/gowitness
	
	\n\n''')

		
		
# bust the directories
def dirbusting(site_targets,dir_targets):
	sites = site_targets
	dirs = dir_targets
	for si in sites:
		for di in dirs:
			bustar = si + tld + di
			dirbustinglist.append(bustar)

### END CRAFT PRIMARY UTILITIES ###








### START MAIN EXECUTION SEQUENCE ###

startit = datetime.now()

# if sitelist and directory list were passed then check for all subdirs of all sites
if args.sitelist is not None and args.dirbust is not None:
	try:
		# check the things
		print(pretty_banner)
		sleep(2)
		print('\n\n Busting directories, please be patient.. \n\n')
		sleep(0.5)
		dirbusting(sitelist,dirlist)
		ping_site(dirbustinglist)
		
		# snap the pics
		if snap:
			print('\n\n Snapping shots, please be patient.. \n\n')
			sleep(1)
			snapshot(live_tar)
			

		print(f'\n\n Task complete, data stored in directory {log_folder} \n\n')
		
	except KeyboardInterrupt:
		print('\n\n User interruption \n\n')

		
# if dirlist was passed without sitelist then print help
elif args.dirbust is not None and args.sitelist == None:
	print(help)
	exit()

# if only sitelist passed then check for those sites			
elif args.sitelist is not None and args.dirbust == None:

	try:		
		# check the things
		print(pretty_banner)
		sleep(2)
		print('\n\n Pinging sitelist, please be patient.. \n\n')
		sleep(0.5)
		ping_site(sitelist)
				
		# snap the pics
		if snap:
			try:
				print('\n\n Snapping shots, please be patient.. \n\n')							
				snapshot(live_tar)
			except KeyboardInterrupt:
				pass
				
		print(f'\n\n Task complete, data stored in directory {log_folder} \n\n')

	except KeyboardInterrupt:
		print('\n\n User interruption \n\n')

# if no sitelist or dirlist passed, but redirection requested
elif args.sitelist == None and args.dirbust == None and args.redirection:
	try:
		# check the things
		print(pretty_banner)
		sleep(2)
		print(f'\n\n Bruteforcing sites into {brute_direction}, please be patient.. \n\n')
		sleep(0.5)
		
		try:
			bd = open(brute_direction,'x')							
		except:
			bd = open(brute_direction,'a')
			
		print('\n\nSaving combinations:\n\n')
		 
		for attempt in bruteforce():
			try:
				if args.verbose:
					print(f'{attempt}\n')
				bd.write(attempt + '\n')
			except KeyboardInterrupt:
				break			
		
		bd.close()
					
		print(f''' 
		
	This message means either that the task is complete, or that you interrupted the process.
	
	Either way, we stuck whatever data you've generated in directory {brute_direction}.
	
	Go ahead and pass this as a sitelist into another run of brutePup!
	
			''')		

	except KeyboardInterrupt:
		print('\n\n User interruption \n\n')


# if neither sitelist nor dirlist was passed, and redirection not, then bruteforce across network					
else:
	try:
		# check the things
		print(pretty_banner)
		sleep(2)
		print('\n\n Checking bruteforced sites, please be patient.. \n\n')
		sleep(0.5)
		
		for att in bruteforce():
			try:
				target = ssl_prefix + att + tld
				ping_site_brute(target)
			except KeyboardInterrupt:
				break	

		# snap the pics
		if snap:
			try:
				print('\n\n Snapping shots, please be patient.. \n\n')							
				snapshot(live_tar)
			except KeyboardInterrupt:
				pass					


		print(f'\n\n Task complete, data stored in directory {log_folder} \n\n')		

	except KeyboardInterrupt:
		print('\n\n User interruption \n\n')

		
### END MAIN EXECUTION SEQUENCE ###


### START LOGGING ###

# record the data
print('\n\n Logging responses, please be patient.. \n\n')		
live_logging(live_tar)
target_logging(live_tar)
print('\n\n Logging errors, please be patient.. \n\n')
error_logging(live_tar)

### END LOGGING ###


### START REPORTING ###
stopit = datetime.now()
print(f'\n\n Total time in execution: {stopit - startit}\n\n')
print(f'Living Targets are: \n\n {live_tar}')

print('\n\nCleaning up, please be patient..\n\n')

### END REPORTING ###

### START CLEAN UP ###

le.close()
lf.close()
lt.close()



### END CLEAN UP ###



### START FOOTERS ###

'''

CITATIONS

1. https://stackoverflow.com/questions/45990454/generating-all-possible-combinations-of-characters-in-a-string

2. https://www.reddit.com/r/TOR/comments/nfyop1/im_trying_to_index_active_onion_sites_needing/

3. https://blog.torproject.org/ethical-tor-research-guidelines/

4. https://github.com/sensepost/gowitness

5. https://stackoverflow.com/questions/4319236/remove-the-newline-character-in-a-list-read-from-a-file

6. https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20

7. https://akshayranganath.github.io/Rate-Limiting-With-Python/

8. https://pypi.org/project/ratelimiter/

9. https://stackoverflow.com/questions/18280612/ioerror-errno-24-too-many-open-files

10. https://stackoverflow.com/questions/11747254/python-brute-force-algorithm

11. https://realpython.com/introduction-to-python-generators/


'''

### END FOOTERS ###
