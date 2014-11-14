#################################################################################################################################
#
# flowgrapher.py
# Generate Traffic Graphics for 24 hours
#
#
#
################################################################################################################################


from GenerateDictionary import *

from grapher_divided_graph import *

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
#sets the number that the time is going to be modulated by
interval_modulation=INCREMENT 
db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
c = db.cursor()
network = GenerateDictionary().GenDictionary(c)
now = int(time.time())
# now is the the current time modulated by Increment. 
now = now - now%INCREMENT  


for inter in network.keys():
	for label in  network[inter].keys():
		# Input / Output
		nlabel = GetLabelByNumber(c, label, inter)
		nid = GetNetId(c, label, inter)

                # Normal graphs for I/O:
		graphInt24h(now, nlabel, nid, GRAPH_PATH)
	 
		# Graphs for Ports
		for port in network[inter][label]["port"]:
	
			pid =  GetPortId(c, nid, port)

			graphPort24h(now,nlabel, port, pid, GRAPH_PATH)
	#	continue
		# Graphs Point to Point Interfaces 
		for to_inter_type in network[inter][label]["to"]:
			for to_inter in  network[inter][label]["to"][to_inter_type]:
				to_label = GetLabelByNumber(c, to_inter, to_inter_type)
				to_id=GetNetId(c, to_inter, to_inter_type)
				nn_id=getnn_id(nid,to_id,c)

				graphP2P24h(now,nlabel, nn_id, to_label, GRAPH_PATH)

#Close connection
c.close()
