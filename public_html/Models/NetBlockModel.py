##### Imports #####

import struct
import socket
import re         
import MySQLdb    
import sys
from Config import Config

##### Imports #####

class NetBlockModel:

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


	################################### NetBlock Methods #########################################

	def Get(self, id):
        	
		self.cursor.execute("""select nb_id, ip_from, ip_to from NET_BLOCK where n_id=%s""" % id)
        	
		return self.cursor.fetchall()

	def GetAll(self, nid):
        	
		self.cursor.execute("""select nb_id, ip_from, ip_to from NET_BLOCK where n_id=%s""" % nid)
        	
		return self.cursor.fetchall()

	def Add(self, id, ip_from, ip_to):
	        
		ip_from = struct.unpack("!L", socket.inet_aton(ip_from))[0]
	        
		ip_to = struct.unpack("!L", socket.inet_aton(ip_to)) [0]

		try:
	                
			return self.cursor.execute("""insert into NET_BLOCK (n_id, ip_from, ip_to) values (%s, %s, %s)""" % (id, ip_from, ip_to))

		except MySQLdb.IntegrityError, e:
	                
			print e
	                
			return None
	        
		except:
	            
			print "Unknown Error Please contact administrator"


	def Remove(self, id, bid):
	        
	        #blocks = CheckIDs(form, "blocks")
	                
			try:
	            
				self.cursor.execute("""delete from NET_BLOCK where nb_id=%s and n_id=%s""" % (bid, id))
	        	
			except:
	                
				print "Unknown Error Please contact administrator"
