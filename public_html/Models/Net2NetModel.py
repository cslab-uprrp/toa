##### Imports #####

import struct
import socket
import re         
import MySQLdb    
import sys
from Config import Config

##### Imports #####

class Net2NetModel:

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


	################################### Net2Net Methods #########################################

	
	def GetGraphInfo(self, id, nn_id):
        
		self.cursor.execute("""select n_id, label from NETWORK, NET2NET where (NETWORK.n_id=fn_id or NETWORK.n_id=tn_id) and NET2NET.nn_id=%s and NET2NET.fn_id=%s""" % (nn_id, id))
        	
		return self.cursor.fetchall()

	def GetFromandTo(self,id):
    #this function gets a net2net id and returns the from and to network ids of that connection in an array
        	self.cursor.execute("select fn_id, tn_id from NET2NET where nn_id=%s"%id)
        	return self.cursor.fetchall()

	def Get(self, id):
        	
		self.cursor.execute("""select nn_id, label, tn_id from NETWORK, NET2NET where fn_id=%s and tn_id=n_id""" % id)
        	
		return self.cursor.fetchall()

	def GetAll(self, nid):
        	
		self.cursor.execute("""select nn_id, tn_id, label from NET2NET, NETWORK where fn_id='%s' and n_id=tn_id """ % nid)
        	
		return self.cursor.fetchall()

	def Add(self, id, device):
	        
	    try:
	                
	        return self.cursor.execute("""insert into NET2NET (fn_id, tn_id) values (%s, %s); insert into NET2NET (fn_id, tn_id) values(%s, %s)""" % (id, device, device, id))
	    
	    except MySQLdb.IntegrityError, e:
	               
	        print e
	                
	        return None
	        
	    except:
                	
			print "Unknown Error Please contact administrator"


	def Remove(self, nnid):

		fn_id,tn_id=self.GetFromandTo(nnid)[0]

		try:
	               
			self.cursor.execute("""delete from NET2NET where tn_id=%s and fn_id=%s""" % (tn_id,fn_id))
			self.cursor.execute("""delete from NET2NET where fn_id=%s and tn_id=%s""" % (tn_id,fn_id))
	        
		except:
	                
			print "Unknown Error Please contact administrator"
