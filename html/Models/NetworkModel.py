##### Imports #####

import struct
import socket
import re         
import MySQLdb
import os
import sys  
from Config import Config
##### Imports #####

class NetworkModel:

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

	def GetLabel(self, id):
	
		self.cursor.execute("""select label from NETWORK where n_id='%s'""" % id)

		return self.cursor.fetchone()[0]

		#print "Hello"

	def GetLabels(self):

		self.cursor.execute("""SELECT label FROM NETWORK""")#Select the label field from the Network Table in the DB

		return self.cursor.fetchall()#fetch all the labels(all the networks)

	def GetNumberOfLabels(self):

		self.cursor.execute("""SELECT label FROM NETWORK""")#Select the label field from the Network Table in the DB

		return self.cursor.rowcount#get the number of labels or networks there are


	def GetIdByLabel(self, label):

		self.cursor.execute("""SELECT n_id FROM NETWORK WHERE label = '%s'"""%label)#select the network id field from the table Network in the DB

		return self.cursor.fetchone()#fetch the value of the id of the current network in the list


	def GetAll(self):
    
		self.cursor.execute("""select n_id, label from NETWORK""")

		return self.cursor.fetchall()

	def GetByUser(self, uid):
        	
		self.cursor.execute("""select USUARIO_NETWORK.n_id, label from USUARIO_NETWORK, NETWORK where USUARIO_NETWORK.uid=%s and USUARIO_NETWORK.n_id = NETWORK.n_ID""" % uid)
        	
		return self.cursor.fetchall()

	def Get(self, ids):
        
		self.cursor.execute("""select label, interface, asn, tom, min_byte_flow, max_byte_flow from NETWORK where n_id = '%s' """ %ids)
        	
		result = self.cursor.fetchone()

		if result:
                	
			return result[0], result[1], result[2], result[3], result[4], result[5]

		return None, None, None, None, None, None

	def GetMinMaxBytes(self, id):
		
		self.cursor.execute("select min_byte_flow, max_byte_flow from NETWORK where n_id = '%s'"%id)

		min_max = self.cursor.fetchall()

		return min_max

	def GetToSelect(self, id):
        
		self.cursor.execute("""select n_id, label from NETWORK where not EXISTS (select * from NET2NET where fn_id=%s and n_id = tn_id) and n_id <> %s""" % (id,id))
        	
		return self.cursor.fetchall()

	def GetNetwork2(self, id):
        
		self.cursor.execute("""select nn_id, label, tn_id from NETWORK, NET2NET where fn_id=%s and tn_id=n_id""" % id)
        	
		return self.cursor.fetchall()

	def Add(self, label, monitoringType, interfaceNumber, asNumber, minBytes, maxBytes):

		try:
	
			self.cursor.execute("""insert into NETWORK (label, tom, interface, asn, max_byte_flow, min_byte_flow) values ('%s', '%s', '%s', '%s', '%s', '%s')""" % (label, monitoringType, interfaceNumber, asNumber, maxBytes, minBytes))
			
			return self.cursor.lastrowid
        	
		except MySQLdb.IntegrityError, e:
        	
			print e
       
		except:
        	        
			print "Unknown Error Please contact administrator"

			return None

	def Save(self, id, label, monitoringType, interfaceNumber, asNumber, minBytes, maxBytes):
        
		try:
        	        
			e = self.cursor.execute("""update NETWORK set label='%s', tom='%s', interface='%s',asn='%s' where n_id='%s'""" % (label, monitoringType, interfaceNumber, asNumber, id))
        		
			p = re.compile('[0-9]')
			
			if(minBytes == None or p.match(str(minBytes)) == None):
				
				minBytes = 0
			
			if(maxBytes == None or p.match(str(maxBytes)) == None):
				
				maxBytes = 0
			
			d = self.cursor.execute("""update NETWORK set min_byte_flow='%s', max_byte_flow='%s' where n_id='%s'"""%(minBytes, maxBytes,id))
			
			return e, d
		
		except MySQLdb.IntegrityError, e:
        	        
			print  e
        	        
			return None
        
		except:
        	        
			print "Unknown Error Please contact administrator"


	def Remove(self, ids):

		try:

			self.cursor.execute("""delete from NETWORK where n_id = '%s' """ %ids)

			self.cursor.execute("""delete from USUARIO_NETWORK where n_id='%s'""" % ids)

			self.cursor.execute("""delete from NET2NET where nn_id='%s' or fn_id='%s'""" % (ids, ids))

			self.cursor.execute("""delete from PORT where n_id='%s'""" % ids)

			self.cursor.execute("""delete from NET_BLOCK where n_id='%s'""" % ids)

			return 1

		except MySQLdb.IntegrityError, e:

			print  e
        	        
			return 0

		except:

			print "Unknown Error Please contact administrator"


