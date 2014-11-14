##### Imports #####

import struct
import socket
import re         
import MySQLdb    
import sys
from Config import Config

##### Imports #####

class SessionModel:

	def connect(self, name = None, user = None, passwd = None, flows_path = None, graphs_path = None, crontime = None):

		try:    
                                
			dbinfo = Config()
                
			try:

				conn = MySQLdb.connect(user=dbinfo.getUser(), passwd=dbinfo.getPassword(), db=dbinfo.getDBName(), host="localhost")

				self.cursor = conn.cursor()

				return True

			except MySQLdb.Error, e:
                                
				pass
                                
				sys.exit(0)
                                
				print "Error %d: %s" % (e.args[0],e.args[1])

				return False


		except:

			dbinfo = Config(None, name, user, passwd, flows_path, graphs_path, crontime)

			try:

				conn = MySQLdb.connect(user=dbinfo.getUser(), passwd=dbinfo.getPassword(), db=dbinfo.getDBName(), host="localhost")

				self.cursor = conn.cursor()

				return True

			except MySQLdb.Error, e:

				pass

				print "Error %d: %s" % (e.args[0],e.args[1])

				return False


   	def __del__(self):

   		try:

			self.cursor.close()

		except:

			pass
		

	###################### SessionModel Methods ############################


	def Create(self, id, sid, date, remote):

	    return self.cursor.execute("""insert into SESION (uid,sid,lasttime,remote_addr) values('%s','%s','%s','%s') """%(id,sid,date,remote))#Update the session id of the user in the database field
		
	
	def GetId(self, id, remote):

		self.cursor.execute("SELECT sid FROM SESION WHERE uid = '%s' and remote_addr = '%s'"%(id,remote))#Selecting the Session field of the User Table

		return self.cursor.fetchone()[0]#fetching the session id of the current user


	def GetTimeStamp(self, id, remote):

		self.cursor.execute("SELECT lasttime FROM SESION WHERE uid = '%s' and remote_addr = '%s'"%(id,remote))#selecting the datestamp field of the User Table

		return self.cursor.fetchone()#fetching the value of the Datestamp of the current user

	def Validate(self, uid, sid, remote):

		self.cursor.execute("SELECT lasttime from SESION where uid = '%s' and sid = '%s' and remote_addr = '%s'"%(uid, sid, remote))

		status = self.cursor.fetchone()

		if(status == None):

			return -1

		return int(status[0])

	def UpdateTimeStamp(self, date, id, remote):

		self.cursor.execute("UPDATE SESION SET lasttime = '%s' WHERE uid = '%s' and remote_addr='%s'"%(date,id,remote))


	def Close(self, id, remote):

	        self.cursor.execute("delete from SESION where uid = '%s' and remote_addr = '%s'"%(id,remote))
