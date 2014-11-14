#!/usr/bin/python

import time
import MySQLdb
from Config import Config
import os 

config=Config()
DB_NAME=config.getDBName();
DB_HOST='localhost'
DB_USER=config.getUser();
DB_PASS=config.getPassword();
INCREMENT=config.getCronTime()
LOGSPATH=config.getLogsPath()

db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
c = db.cursor()


#check if logs path exists, if not create it

if not os.path.exists(LOGSPATH):
	os.makedirs(LOGSPATH)
 
logs=open(LOGSPATH+'/cleanup_log','a+')

#maxtime=31536000
year=31536000  #year in seconds
maxtime=int(config.getOldesttime())*year


now = int(time.time())

databasenow=now-now%INCREMENT
databasenow-=600 #oldest time in database


oldesttime= databasenow - maxtime


sql=" select time_unix from rrd_n order by time_unix desc limit 1" # do not use max, because if the clock changes the last one isnt necessarily the max 

c.execute(sql)

lasttime=c.fetchone()[0]

if lasttime >= (databasenow-600) and lasttime<=now :


	sql="delete from rrd_n where time_unix <= %s"%(oldesttime)

	c.execute(sql)
else:
	logs.write(" ERROR: Didn't delete from rrd_n tables because of time mismatch. System time is %s, database time is %s\n"%(now,lasttime))

#########################################################
sql=" select time_unix from rrd_port order by time_unix desc limit 1" # do not use max, because if the clock changes the last one isnt necessarily the max 

c.execute(sql)

lasttime=c.fetchone()[0]

if lasttime >= (databasenow-600) and lasttime<=now :

	sql="delete from rrd_port where time_unix <= %s"%(oldesttime)

	c.execute(sql)
else:
	logs.write(" ERROR: Didn't delete from rrd_port tables because of time mismatch. System time is %s, database time is %s\n"%(now,lasttime))


#########################################################
sql=" select time_unix from rrd_to_net order by time_unix desc limit 1" # do not use max, because if the clock changes the last one isnt necessarily the max 

c.execute(sql)

lasttime=c.fetchone()[0]

if lasttime >= (databasenow-600) and lasttime<=now :

	sql="delete from rrd_to_net where time_unix <= %s"%(oldesttime)

	c.execute(sql)
else:
	logs.write(" ERROR: Didn't delete from rrd_to_net tables because of time mismatch. System time is %s, database time is %s\n"%(now,lasttime))


logs.close()
