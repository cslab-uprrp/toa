# This file is executed by the cron alogn with the flowsgrapher2 script
# The purpose is to parse the flow data from the flow files , create the dictionary and then insert the data in the database
# This is called from the flowdbu.sh script

import flowtools
from StripFlowData import *
from GenerateDictionary import *
import sys
import MySQLdb
import os
import time
from Config import Config

 # the config file path is not specified as a command line parameter
if len(sys.argv) < 3:
	config=Config() 
# the path is specified
else:

	config=Config(sys.argv[2])
	

# This is the main function, it receives file which is the flow file being inserted in the database
def main(file):


	intervalmodulation=config.getCronTime() # the interval to be inserted into the db in unix time. 
        #Split to create timestamp
	temp_var = file.split("/")[-1].split('.')
	date = temp_var[1]
	temp_var = temp_var[2].split('-')
	t_time = temp_var[0]
	time_stamp = date + " " + t_time[0:2] + ":" + t_time[2:4] + ":" + "00"
	date = map(int, date.split('-'))
	utime_stamp = int(time.mktime((date[0], date[1], date[2], int(t_time[0:2]), int(t_time[2:4]), int("00"), 0, 0, 0)))
        utime_stamp = utime_stamp - (utime_stamp%intervalmodulation) #if for some reason the time stamp is not in the specified interval for updating the db , susbtract the necesary seconds the make it fit.  
	
        # Database settings
	#needed to extract database info from the configuration file
	DB_NAME=config.getDBName();
	DB_HOST='localhost'
	DB_USER=config.getUser();
	DB_PASS=config.getPassword();
	db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
	c = db.cursor()
        basepath=config.getFlowsPath()
	path=file
	#This generates the dictionary. It needs the database cursor because settings for the dictionary are in the database
	network = GenerateDictionary().GenDictionary(c) 
	
	sf = StripFlowData() 
	set = flowtools.FlowSet(path)

	#iterates over the flow file
	for flow in set: 
		#uses the stripflowdata to fill the dictionary with the data from the file
		sf.StripFlowData(flow, network) 
	
	
	
	
	#Iterates over the first level of the dictionary  (Monitoring by AS,Net or Interface)
	for inter in network.keys(): 
		#for each network label being monitored 
		for label in  network[inter].keys(): 
			#gets network id and stores it in nlabel
			nlabel = GetNetId(c, label, inter) 
                        # Insert data in database
			c.execute("""INSERT INTO rrd_n(nid, ooctect, ioctect, opacks, ipacks, oflows, iflows, time_unix) VALUES(%s, %s, %s, %s, %s, %s, '%s','%s')""" % (nlabel, network[inter][label]['o'][0], network[inter][label]['i'][0], network[inter][label]['o'][1], network[inter][label]['i'][1], network[inter][label]['o'][2], network[inter][label]['i'][2],utime_stamp))
	
			# Ports 
	
			#iterates over ports being monitored (if any) 
			for port in network[inter][label]["port"]:
				#gets id for the desired port 
				nport = GetPortId(c, nlabel, port)
				c.execute("""INSERT INTO rrd_port(pid, ooctect, ioctect, opacks, ipacks, oflows, iflows, time_unix) VALUES(%s, %s, %s, %s, %s, %s, '%s', '%s')""" % (nport, network[inter][label]['port'][port]['o'][0], network[inter][label]['port'][port]['i'][0], network[inter][label]['port'][port]['o'][1], network[inter][label]['port'][port]['i'][1], network[inter][label]['port'][port]['o'][2], network[inter][label]['port'][port]['i'][2], utime_stamp))
	
			# To Interfaces
			
			#iterates over the monitoring options like AS,NET or interface for each  net2net connection 
			for to_inter in network[inter][label]["to"]:
				#iterates over the destination labels for each net2net connection 
				for to_label in  network[inter][label]["to"][to_inter]:
					#gets id of destination network 
					nto_label = GetNetId(c, to_label, to_inter)
					# gets id for that specific net2net connection 
					nn_id=getnn_id(nlabel,nto_label,c)
					c.execute("""INSERT INTO rrd_to_net(nn_id, ooctect, ioctect, opacks, ipacks, oflows, iflows,time_unix) VALUES(%s, %s, %s, %s, %s, %s, '%s','%s')""" % (nn_id, network[inter][label]['to'][to_inter][to_label]['o'][0], network[inter][label]['to'][to_inter][to_label]['i'][0], network[inter][label]['to'][to_inter][to_label]['o'][1], network[inter][label]['to'][to_inter][to_label]['i'][1], network[inter][label]['to'][to_inter][to_label]['o'][2], network[inter][label]['to'][to_inter][to_label]['i'][2], utime_stamp))
	
	c.close()
	
##################################### MAIN ####################################################
#retrieves the flow file passed as an argument 
file = sys.argv[1]
main(file)
	
