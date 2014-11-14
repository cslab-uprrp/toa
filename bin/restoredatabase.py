#! usr/bin/python
import sys
import os
import re
import time
from optparse import OptionParser
from Config import Config
import MySQLdb
# Regular expressions to check if the correct directories are being opened
year_exp=re.compile( '(1|2)[0-9][0-9][0-9]')
yearmonth_exp=re.compile( '(1|2)[0-9][0-9][0-9]-(0[1-9]|1[0-2])')
yearmonthday_exp=re.compile( '(1|2)[0-9][0-9][0-9]-(0[1-9]|1[0-2])-(([0-2][0-9])|3[0-1])')
flowfile_exp=re.compile('ft-v05.*')


def getunixtimefromflow(flowfile):

	splitfile=flowfile.split('.')
	seconds=splitfile[2].split("-")[0]
	year=splitfile[1].split("-")[0]
	month=splitfile[1].split("-")[1]
	day=splitfile[1].split("-")[2]
	unixtime="%s-%s-%s %s:%s:00"%(year,month,day,seconds[0]+seconds[1], seconds[2]+seconds[3])
	unixtime=time.strptime(unixtime,"%Y-%m-%d %H:%M:%S")
        unixtime=time.mktime(unixtime)

	
	return unixtime

def checkifexists(unixtime):

    config=Config()

    DB_NAME=config.getDBName()
    DB_HOST='localhost'
    DB_USER=config.getUser()
    DB_PASS=config.getPassword()


    db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
    c = db.cursor()
    c.execute('Select * from rrd_n where time_unix=%s'%(unixtime))
    result=c.fetchone()
    if result:
            return 1;
    return 0;


def getcontinue_unixtime():


# In case io error because file got removed
	try :
		file=open("flowdatabase_continue.log","r")
		lastfile=file.readline()
		if lastfile!="":
			unixtime=getunixtimefromflow(lastfile)
		else:
			unixtime=0;
		file.close()

	except (IOError,IndexError):
		unixtime=0
	return unixtime



def daily_insert(options,PATH):

  if (options.continues==True):
	unixtime=getcontinue_unixtime()
#open log file to record the last flow inserted into the database so we are able to continue later if the script stops
        try:
            file=open("flowdatabase_continue.log","r+")
        except(IOError):
            file=open("flowdatabase_continue.log","w")
            print ("Log file didnt exist. Creating flowdatabase_continue.log file now\n")

  else:
	unixtime=0 #so it doesnt affect the condition in the loop

  flow_files=sorted(os.listdir(PATH))

  for flow in flow_files:
		if (flowfile_exp.match(flow)!=None and getunixtimefromflow(flow)>unixtime):
                        execute=0
                        if (options.indatabase==True):
                             execute=checkifexists(getunixtimefromflow(flow))

#			print flow
			if continues==True and execute==0:
				file.seek(0)
				file.write(flow)
                        if execute==0:
		    	  try:

				os.system("python ../bin/flows-db-update.py %s "%(PATH+"/"+flow))
			  except (IOError):
				print ("ERROR : Error occured  in flows-db_update\n")
 								
 
  if (continues==True):
	file.close()






def monthly_insert(options,PATH):


  if (options.continues==True):
	unixtime=getcontinue_unixtime()
#open log file to record the last flow inserted into the database so we are able to continue later if the script stops
        try:
            file=open("flowdatabase_continue.log","r+")
        except(IOError):
            file=open("flowdatabase_continue.log","w")
            print ("Log file didnt exist. Creating flowdatabase_continue.log file now\n")
  else:
	unixtime=0 #so it doesnt affect the condition in the loop

  day_flows=sorted(os.listdir(PATH))

  for  day in day_flows:
		if (yearmonthday_exp.match(day)!=None):
			flow_files=sorted(os.listdir(PATH+"/"+day))
			for flow in flow_files:
				if (flowfile_exp.match(flow)!=None and getunixtimefromflow(flow)>unixtime):
                                        execute=0
                                        if (options.indatabase==True):
                                                execute=checkifexists(getunixtimefromflow(flow))


				#	print flow
					if continues==True and execute==0:
						file.seek(0)
						file.write(flow)

                                        if execute==0:
                                            try:
                                                        print PATH+"/"+day+"/"+flow+"\n"

					        	os.system("python ../bin/flows-db-update.py %s "%(PATH +"/"+day+"/"+flow))
					    except (IOError):
					        	print ("ERROR : Error occured  in flows-db_update\n")
 								
 
  if (continues==True):
	file.close()




def yearly_insert(options,PATH):

  if (options.continues==True):
	unixtime=getcontinue_unixtime()
#open log file to record the last flow inserted into the database so we are able to continue later if the script stops
        try:
            file=open("flowdatabase_continue.log","r+") #if it already exists it needs to be r+ because w will overwrite it completely 
        except(IOError):
            file=open("flowdatabase_continue.log","w")
            print ("Log file didnt exist. Creating flowdatabase_continue.log file now\n")

  else:
	unixtime=0 #so it doesnt affect the condition in the loop

  month_flows=sorted(os.listdir(PATH))

  for month in month_flows:
#			print month
			if (yearmonth_exp.match(month)!=None):
				day_flows=sorted(os.listdir(PATH+"/"+month))
				for  day in day_flows:
					if (yearmonthday_exp.match(day)!=None):
						flow_files=sorted(os.listdir(PATH+"/"+month+"/"+day))
						for flow in flow_files:
							if (flowfile_exp.match(flow)!=None and getunixtimefromflow(flow)>unixtime):

                                                                execute=0;
                                                                if (options.indatabase==True):
                                                                    execute=checkifexists(getunixtimefromflow(flow))
								#print flow
								if continues==True and execute==0:
									file.seek(0)
								    	file.write(flow)

                                                                if execute==0:
                                                                  try:

								    os.system("python ../bin/flows-db-update.py %s "%(PATH+"/"+month+"/"+day+"/"+flow))
								  except (IOError):
									print ("ERROR : Error occured  in flows-db_update\n")
 								
 
  if (continues==True):
	file.close()

def normalpathinsert(options,PATH):
        #The user adds only one file, the same can be accomplished by running flows-db-update directly 
  
  s=PATH.split('/')
  flow=s[len(s)-1]
  if (options.continues==True):
	unixtime=getcontinue_unixtime()
#open log file to record the last flow inserted into the database so we are able to continue later if the script stops
        try:
            file=open("flowdatabase_continue.log","r+") #if it already exists it needs to be r+ because w will overwrite it completely 
        except(IOError):
            file=open("flowdatabase_continue.log","w")
            print ("Log file didnt exist. Creating flowdatabase_continue.log file now\n")

  else:
	unixtime=0 #so it doesnt affect the condition in the loop
  execute=0;
  if (options.indatabase==True):
            execute=checkifexists(getunixtimefromflow(flow))
  if continues==True and execute==0:
	    file.seek(0)
	    file.write(flow)
  if execute==0:
    try:

	os.system("python ../bin/flows-db-update.py %s "%(PATH))
    except (IOError):
	print ("ERROR : Error occured  in flows-db_update\n")
 								
  if (continues==True):
	file.close()
###################Main ####################




###############command line options:


parser = OptionParser()
#check if in database
parser.add_option("-i", "--indatabase", action="store_true", dest="indatabase",help="If there exists an entry in the database for the time corresponding to the current flow file it skips it")
#Continue
parser.add_option("-c", "--continues", action="store_true", dest="continues",help="Creates and writes in a log file the last flow entered in the database so that the it can continue from there if the script  is stopped. If the log file already exists, the scripts reads the last flow file entered, and only writes into the database flow files after that. To reset just delete log file")

#year
parser.add_option("-y", "--year", metavar="YEAR", dest="year",help="Only inserts flow files belonging to the year the user specifies in the path. Use by specifying -y followed by path path")

#month
parser.add_option("-m", "--month", metavar="MONTH", dest="month",help="Only inserts flow files belonging to the year and month the user specifies in the path. Use by specifying -m followed by path")

#daily
parser.add_option("-d", "--day", metavar="DAY", dest="day",help="Only inserts flow files belonging to the day  month and year the user specifies in the path. Specify by using -d followed by path")

###get the parameters###
(options, args) = parser.parse_args()

continues=options.continues



if (options.year):
	PATH= options.year
	yearly_insert(options,PATH)
elif options.month:
	PATH= options.month
	monthly_insert(options,PATH)
	
elif options.day:
	PATH=options.day
	daily_insert(options,PATH)
else:
	PATH=os.sys.argv[len(os.sys.argv)-1]
	normalpathinsert(options,PATH)








	


