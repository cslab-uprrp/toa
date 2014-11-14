#################################################################################################################################
#
# flowgrapher.py
# Generate Traffic Graphics for week, month and year
#
#
#
################################################################################################################################


from GenerateDictionary import *

from grapher_divided_graph import *

from multiprocessing import Pool
import sys
import MySQLdb
import os
import time

from Config import Config

 # the config file path is not specified as a command line parameter
if len(sys.argv) < 2:
	config=Config() 
# the path is specified
else:

	config=Config(sys.argv[1])

DB_NAME=config.getDBName();
DB_HOST='localhost'
DB_USER=config.getUser();
DB_PASS=config.getPassword();

INCREMENT=config.getCronTime()
GRAPH_PATH=config.getGraphsPath()
#sets the number that thetime is going to be modulated by
interval_modulation=INCREMENT 
db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
c1 = db.cursor()

network = GenerateDictionary().GenDictionary(c1)
c1.close()
now = int(time.time())
# now is the current time modulated by the increment 
now = now - now%INCREMENT  

#This function graphs the point to point graphs for a network
# It receives: the type of monitoring for that point to point connection(to_inter_to), the network label (to_inter),the network id (nid), the readable name of the network (nlabel)
def n2nworker(to_inter,to_inter_type,nid,nlabel):
            db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
            c = db.cursor()
	    to_label = GetLabelByNumber(c, to_inter, to_inter_type)
	    to_id=GetNetId(c, to_inter, to_inter_type)
	    nn_id=getnn_id(nid,to_id,c)


	    graphP2P1s(now,nlabel, nn_id, to_label, GRAPH_PATH)

	    graphP2P1m(now,nlabel, nn_id, to_label, GRAPH_PATH)

	    graphP2P1a(now,nlabel, nn_id, to_label,  GRAPH_PATH)

            c.close()

#This function graphs the ports for a specific network 
def portworker(port,nid,nlabel):
             db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
             c = db.cursor()
	
	     pid =  GetPortId(c, nid, port)


	     graphPort1s(now,nlabel,port,  pid, GRAPH_PATH)

	     graphPort1m(now,nlabel,port, pid, GRAPH_PATH)
	
	     graphPort1a(now,nlabel,port, pid, GRAPH_PATH)	

             c.close()
#This function is called by each process to graph the graphs of a specific network 
def processgrapher(args):
                label, inter= args
                
                db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
                c = db.cursor()
		# Input / Output
		nlabel = GetLabelByNumber(c, label, inter)
		nid = GetNetId(c, label, inter)

                # Normal graphs for I/O:
		graphInt1s(now, nlabel, nid, GRAPH_PATH)
		graphInt1m(now, nlabel, nid, GRAPH_PATH)
		graphInt1a(now, nlabel, nid, GRAPH_PATH)
		#Close connection
                c.close()
		# Graphs for Ports
		for port in network[inter][label]["port"]:
                        portworker(port,nid,nlabel)

		
		# Graphs Point to Point Interfaces
		for to_inter_type in network[inter][label]["to"]:
			for to_inter in  network[inter][label]["to"][to_inter_type]:
                    		n2nworker(to_inter,to_inter_type,nid,nlabel)


if __name__=='__main__':

    # for each type of monitoring option (AS, network, interface)
    for inter in network.keys():
    		labels=[]
		#for each network under that type
		for label in network[inter].keys():
				#create a list of networks to graphs
				labels.append(label)
		#if there are networks  to graph
        	if len(labels)>0:
			#create a list of tupples to pass as param to the pool of procceses 
			#tupple contains, label and monitoring type (inter)
            		args=((label,inter) for label in labels)
            		pool = Pool()
            		pool.map_async(processgrapher,((label,inter) for label in labels))
            		pool.close()
            		pool.join()
