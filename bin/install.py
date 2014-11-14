#!/usr/bin.python
import sys 
import MySQLdb
import re
import os
sys.path.append("../public_html/Models")
from UserModel  import *

def getpasswd():
	confirm=""
	toapass=" "
	valid=False
	while (confirm!=toapass or valid==False):
		toapass=raw_input("Enter a password \n")
		confirm=raw_input("Please confirm password\n")
		if confirm!=toapass:
			print("ERROR:passwords dont match, please try again\n")
		#elif re.match('.(?=.{8,})(?=.[a-zA-Z])(?=.[!@#\$%*&]).*$',toapass)==None  :
		elif re.match('.(?=.{8,})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#\$%@&\?\* "]).*$',toapass)==None  :
			print "Password not valid, must contain at least 8 characters and at least one number, one letter and one unique character"
		else:
			valid=True
	return toapass 

def createcrontab(flowspath, binpath) :
	fd = open("../etc/crontab", "w")
	binpath+='/bin'
	fd.write("""*/5 * * * * %s/flowdbu.sh %s %s\n""" % (binpath, flowspath, binpath))	
	fd.write("""0 22 * * * /usr/bin/python %s/flowsgrapherdaily_pool.py""" % (binpath))
	fd.write("""0 22 * * * /usr/bin/python %s/flowsdbcleaner.py \n"""%(binpath) )	
	fd.close()

def confirmInput(msg):
	value = ""
	cont = ""
	while 1:
		value = raw_input(msg)
		cont = raw_input("Your selection was %s ok?(y/n)" % value)
		if cont == "y" or cont == "Y":
			return value
		
		
		
def createconfigfile(password):

	print "Now enter the following information to create the configuration file\n" 
    	graphpath=confirmInput("Enter the complete graphs path for TOA, suggested: /home/<username>/public_html/graphs (directory must exist, create after instalation if necessary): ")

	flowpath=confirmInput("Enter path where the Flow files will be located (directory must exist, create after instalation if necessary): ")

	logspath=confirmInput("Enter the  complete path for TOA logs to be saved(directory must exist, create after instalation if necessary): ")
	
	crontime=confirmInput("Enter the new crontime (in unix time) for TOA's script executions (suggested 300): ")
	oldesttime=confirmInput("Enter for how many years will Toa keep data in the database before deleting it, min 1 year  max 5 years (only int): ")
	oldesttime=int(float(oldesttime)) #round down just incase

	toapath=confirmInput("Enter the path where the toa directory is located (include the toa directory in the path): ")

	configfile="""
<!-- Warning do not leave spaces in between tags and the data, it will count as part of the data string -->
<config>
        <database>

            <name>%s</name>

            <auth>

                <user>%s</user>

                <passwd>%s</passwd>

            </auth>

        </database>




        <logs><path>%s</path></logs>

        <flows><path>%s</path></flows>

        <graphs><path>%s</path></graphs>

        <crontime><time>%s</time></crontime>

	<oldesttime><time>%i</time></oldesttime>

	<toapath><path>%s</path></toapath> 
    </config>
	""" %(DB_NAME,DB_USER,DB_PASS,logspath,flowpath,graphpath,crontime,oldesttime,toapath)



	file=open('../etc/config.xml','w')
	file.write(configfile)
	file.close()
	return flowpath,graphpath,crontime,toapath


################### MAIN ################

print """This installer will guide you through the installation of TOA"""
print """Please follow the instructions carefully"""
print 

DB_USER=confirmInput("Enter MySQL User to be use with Toa: ")
DB_PASS=confirmInput("Enter the password: ")
DB_NAME=confirmInput("Enter the database to be used\n")
DB_HOST='localhost'

print "Testing connection to database using toadb..."
try:
	db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, host=DB_HOST,db=DB_NAME)

	c = db.cursor()
	print "Succesfully Connected"
except MySQLdb.Error, e:

    print "Error %d: %s" % (e.args[0],e.args[1])
    if e.args[0]==1045:
	print "Make sure you provided the correct password,database and user credentials"
	print "Exiting installation with errors"
    exit(1)

print "Loading Database Schema..."
if os.path.exists('../db/flowsschema.sql'):
	#os.system('mysql -u toadb -p%s -h %s Toa < db/flowsschema.sql'%(toapass,DB_HOST))
	try:
		file=open('../db/flowsschema.sql','r')
		lines=(file.read()).split(";")
		for query in lines:
			c.execute(query)
	except MySQLdb.Error,e:
    		print "Error %d: %s" % (e.args[0],e.args[1])
		print "ERROR: database could not be loaded from 'db/flowsschema.sql', exiting ..."
		c.close()
		exit(1)

	print "Database loaded"
else:
	print "Error: Database dump 'flowsschema.sql' not found, please place it in this directory"
	exit(1)


print "Success"
print "Creating the configuration file"
flowpath,graphpath,crontime, toapath=createconfigfile(DB_PASS)

print "..Done, a file named config.xml was created in the ../etc directory. If desired the file can also be placed on /etc or ~/etc "

print "Generating crontab commands"
createcrontab(flowpath,toapath)

print "..Done, a file named crontab  was created in the ../etc directory. Please copy its contents to the crontab (remember to update crontab if the path it uses change) "

print ("""Creating admin for the web interface.""")
print "Insert password for admin 'toa'"

userpass=getpasswd()
phone=raw_input("Enter phone number(only digits)\n")
while re.match("[0-9]{7,20}$",phone)==None :
	print "ERROR: not a valid phone number (use only digits)"
	phone=raw_input("Enter phone number(only digits)\n")

email=raw_input("Enter email to be used with admin account. Emails are used as usernames in Toa.\n")
while re.match("([a-zA-Z0-9]|\.|_|-|\+|$)+@[a-zA-Z0-9]+(\.[a-zA-Z]+)+$",email)==None:
	print "Error: not a valid email adress"
	email=raw_input("Enter email\n")


user=UserModel()

print DB_USER, DB_PASS

if user.connect(DB_NAME,DB_USER, DB_PASS,flowpath,graphpath,crontime):
	

	user.Create('toa',phone,userpass,email,1)


else:
	print "ERROR: Database Connection Error\n"
	print "Make sure the user 'toa' doesn't exist already"
	print "Exiting installation with errors"
	c.close()
	exit(1)

print("Done, you are now able to log in as admin using the toa user")


c.close()
