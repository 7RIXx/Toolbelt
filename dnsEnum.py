#!/bin/python3

## A quick enumerator to scan for subdomains ; BASED ON A SCRIPT BY RILEY KIDD

## TO DO LIST: Incorporate a check for valid domain name, maybe send a quick GET when checking the user input


# If you have harvested a DNS Cache from some machine, such that it is formatted as:
#
#	127.0.0.1	somesubdir.foofoo.com
#	
# then you can use this bash syntax to pull down a list with the raw subdirectories in it:
#
#	for i in seq harvestedListFile; do cat ${i} | cut -d ‘ ’ -f 5 | cut -d ‘.’ -f 1 > rawSubsFile & done;




# Read each line from the file and prepend the items as subdirectories to GET requests in either HTTP or HTTPS format


# Import required modules

import requests
from time import sleep


# Make Heath proud

prettyBanner = '''
      _              _____                                      
   __| | _ __   ___ | ____| _ __   _   _  _ __ ___              
  / _` || '_ \ / __||  _|  | '_ \ | | | || '_ ` _ \             
 | (_| || | | |\__ \| |___ | | | || |_| || | | | | |            
  \__,_||_| |_||___/|_____||_| |_| \__,_||_| |_| |_|            
  _              _____  ____   _ __  __       ____              
 | |__   _   _  |___  ||  _ \ | |\ \/ /__  __/ ___|   ___   ___ 
 | '_ \ | | | |    / / | |_) || | \  / \ \/ /\___ \  / _ \ / __|
 | |_) || |_| |   / /  |  _ < |_| /  \  >  <  ___) ||  __/| (__ 
 |_.__/  \__, |  /_/   |_| \_\(_)/_/\_\/_/\_\|____/  \___| \___|
         |___/  
         
         Special Thanks to Riley Kidd and TCM Security
'''

print('\n\n' + prettyBanner + '\n\n')
sleep(4)


# Declare globals and configure the environment

fileSet = False
while not fileSet:
    try:
        f = open(input('Please point to the file containing your raw subdirectories: \n >>> '), 'r')
    except KeyboardInterrupt:
        print('Session manually terminated')
        exit()
    except FileNotFoundError:
        print('\n File not found, try again.. \n')
        continue
    else:
        fileSet = True
print('\n')

g = open(input('Which filename would you like to append your results to: \n >>> '), 'a')
print('\n')

d = input('Please indicate the domain you seek to conquor (Eg. google.com): \n >>> ')

accept = ['http', 'https']
h = 'foo'

while h.lower() not in accept:
    try:
        h = input('\n Would you like to attack HTTP or HTTPS? \n >>> ')
        print('\n')
    except KeyboardInterrupt:
        print('Session manually terminated')
        exit()
        
if h.lower() == 'http':
    h = 'http://'
elif h.lower() == 'https':
    h = 'https://'

mylist = f.readlines()

zz = 0


# Make it fun

print('\n Understood, marshalling an attack force...')
sleep(2)
print('\n Forces marshalled, commencing raiding sequence... \n\n')
sleep(1)


# Main logic loop -- send GET to an address, if status is 200 say so and write to a file, if not just say so

while zz < len(mylist):

    try:
        
        r = requests.get(h + str(mylist[zz].strip()) + '.' + d)
        
        code = r.status_code
        if code == 200:
            print('Successful hit on: ' + h + str(mylist[zz].strip()) + '.' + d)
            g.write(h + str(mylist[zz].strip()) + '.' + d + '\n')
            zz += 1
                
    except KeyboardInterrupt:
        print('Session manually terminated')
        exit()
        
    except:
        print('Subdomain ' + str(mylist[zz].strip()) + ' dropped..')
        zz += 1
        continue


# Maintain the narrative

print('\n\n Raid successful, please see \'' + str(g.name) + '\' file to obtain your spoils.\n')


# Clean Up

f.close()
g.close()
