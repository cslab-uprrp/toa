##### Imports #####

import struct
import socket
import re         
import MySQLdb
import os
import sys  
from Config import Config
##### Imports #####

class GraphModel:

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

	###################### Model Methods ############################

	def Get(self, property, field, value):
	
		try:
		
			if property:

				self.cursor.execute("""select %s from GRAPH where %s='%s'""" %(property, field, value))

			else:
				self.cursor.execute("""select * from GRAPH where %s=%s""" %(field, value))

			return self.cursor.fetchall()

		except MySQLdb.Error, e:

			return "Error %d: %s"%(e.args[0], e.args[1])


	def GetViewGraph(self, property, field, value):
	
		try:
		
			if property:

				self.cursor.execute("""select %s from VIEW_GRAPH where %s='%s'""" %(property, field, value))

			else:
				self.cursor.execute("""select * from VIEW_GRAPH where %s='%s'""" %(field, value))

			return self.cursor.fetchall()

		except MySQLdb.Error, e:

			return "Error %d: %s"%(e.args[0], e.args[1])


	def GetAll(self):

		try:
		
			self.cursor.execute("""select gid, graph_name FROM GRAPH""")

			return self.cursor.fetchall()#fetch all the labels(all the networks)

		except MySQLdb.Error, e:

			return "Error %d: %s"%(e.args[0], e.args[1])

			

	def Add(self, name, vid):

		try:

			status = self.cursor.execute("""insert into GRAPH (graph_name) values('%s')"""%(name))

			gid = self.cursor.lastrowid

			status = self.cursor.execute("""insert into VIEW_GRAPH (v_id, g_id) values('%s', '%s')"""%(vid, gid))

			return True

		except MySQLdb.Error, e:

			print "Error %d: %s"%(e.args[0], e.args[1])

			return False


	def Remove(self, field, value):

		try:

			self.cursor.execute("""delete from GRAPH where %s=%s""" %(field, value))

			return True

		except MySQLdb.Error, e:

			print "Error %d: %s"%(e.args[0], e.args[1])

			return False
