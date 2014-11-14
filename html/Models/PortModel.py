##### Imports #####

import struct
import socket
import re         
import MySQLdb   
import sys
from Config import Config    

##### Imports #####

class PortModel:

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


	################################### Ports Methods #########################################

    def Get(self, id):
        	
        self.cursor.execute("""select p_id, port from PORT where n_id='%s'""" % id)
        	
        return self.cursor.fetchall()

    def GetPortNetwork(self,id):
        
	self.cursor.execute("""select n_id from PORT where p_id=%s""" % id)
        	
        return self.cursor.fetchone()
    def GetPortLabel(self,id):
        
	self.cursor.execute("""select port from PORT where p_id=%s""" % id)
        	
        return self.cursor.fetchone()

    def GetAll(self, nid):
            
        self.cursor.execute("""select p_id, port from PORT where n_id = '%s' """%nid)
            
        return self.cursor.fetchall()

    def GetGraphInfo(self, id, p_id):
        
        self.cursor.execute("""select label, port from NETWORK, PORT where NETWORK.n_id=%s and PORT.p_id=%s""" % (id, p_id))
        	
        return self.cursor.fetchone()


    def Add(self, id, p):
        
        try:
        	
        	return self.cursor.execute("""insert into PORT (n_id, port) values (%s, %s)""" % (id, p))
        	
        except MySQLdb.IntegrityError, e:
               
            print e
                	
            return None
        	
       	except:	
        	        
        	print "Unknown Error Please contact administrator"

    def Remove(self, id, pid):
        	        
        try:
                		
            self.cursor.execute("""delete from PORT where p_id=%s and n_id=%s""" % (pid, id))
        		
        except:
                	
            print "Unknown Error Please contact administrator"
	
