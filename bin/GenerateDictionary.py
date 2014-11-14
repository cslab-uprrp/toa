import MySQLdb

def GetLabelByNumber(c, id, type):
	if type == "as":  
		c.execute("""select label from NETWORK where asn=%s""" % id) 
 	elif type=="int":	
		c.execute("""select label from NETWORK where interface=%s""" % id)
	else:
		return id

	return c.fetchone()[0]

def GetNetId(c, id, type):
	if type == "as":  
		c.execute("""select n_id from NETWORK where asn=%s""" % id) 
 	elif type=="int":	
		c.execute("""select n_id from NETWORK where interface=%s""" % id)
	else:
		#	print ("""select n_id from NETWORK where label=%s""" % id)
		c.execute("""select n_id from NETWORK where label='%s'""" % id) 


	return c.fetchone()[0]

def GetPortId(c, nid, port):
	c.execute("""select p_id from PORT where n_id=%s and port=%s""" % (nid, port)) 

	return c.fetchone()[0]

def getnn_id(From,To,c):
	sql="Select nn_id from NET2NET where fn_id=%s and tn_id=%s"%(From,To)
	c.execute(sql)
	nn_id=c.fetchone()[0]
	return nn_id

class GenerateDictionary:

	def GenDictionary(self, c):

		c.execute("""select label, tom, interface, asn, n_id from NETWORK""")
		network = {}

		# DO A BINARY DUMP IN CASE THE MYSQL IS DOWN TO RECUPERATE
		networks = c.fetchall()
		#print networks
		network["int"] = {}
		network["as"] = {}
		network["net"] = {}
	

		# In other MySQLs use net[1].data.keys()[0]
		for net in networks:
			net_type = net[1]
			#print net[1]
			if net_type == "as":
				id = "as"
				label = net[3]
		
			elif net_type == "interface":
				id = "int"
				label = net[2]

			elif net_type == "network": 
				id = "net"
				label = net[0]			
				
			else:
				return {}


			#print id, label
			#network[id] = {label:{}}
			network[id][label] = {"i": [0,0,0], "o": [0,0,0]}
		
			# IF ID is NET then we have to generate the network blocks
			if id == "net":
				network[id][label]["address"] = []
				c.execute("""select ip_from, ip_to from NET_BLOCK where n_id=%s ORDER BY ip_from""" % net[4])
				blocks= c.fetchall()
				if blocks:
				 	for block in blocks:
						network[id][label]["address"].append(block)
				

			c.execute("""select port from PORT where n_id=%s""" % net[4])
			ports = c.fetchall()
			network[id][label]["port"] = {}
			if ports:
			 	for port in ports:
					network[id][label]["port"][port[0]] = {"i": [0,0,0], "o": [0,0,0]}

			
			c.execute("""select label, tom, interface, asn from NETWORK, NET2NET where fn_id=%s and tn_id=n_id""" % net[4])
			network[id][label]["to"] = {} 
			network[id][label]["to"]["as"] = {}
			network[id][label]["to"]["int"] = {}
			network[id][label]["to"]["net"] = {}
			for to in c.fetchall():
				to_net_type = to[1]
				if to_net_type == "as":
					nid = "as"
					nlabel = to[3]
			
				elif to_net_type == "interface":
					nid = "int"
					nlabel = to[2]
	
				elif to_net_type == "network": 
					nid = "net"
					nlabel = to[0]
                                        #print nlabel,nid
                                        #print 'DICT'
                                        #print id, label,'to',nid,nlabel
				network[id][label]["to"][nid][nlabel] = {"i": [0,0,0], "o": [0,0,0]}

		return network

		
