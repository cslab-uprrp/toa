from net_tools import *
import sys
relations = dict()

def addRelation(srcaddr,dstaddr,octets):

	#NOTE: Only for example purposes, the notation n-> m, means that
	# n is the src ip and m is the destination ip.
	#Example: 7->4... then we read 4 
	if relations.get(dstaddr,False) and relations[dstaddr].has_key(srcaddr): 
			relations[dstaddr][srcaddr] += octets

	# We check the relations that already exists
	# Example: 0 -> 3... then you find 0 -> 3 again.
	elif relations.get(srcaddr,False) and relations[srcaddr].has_key(dstaddr):
			relations[srcaddr][dstaddr] += octets
		
	#We add a new entry.
	#Here, we have the following case:
	# We are reading the connection 7 -> 1, but, the line
	# but, the connection 7 -> 5. The early cases already checked that
	# 7 -> 5 or 5 -> 7 does not exists. We add to the dst list of 7's, the
	# destination ip 5.

	elif srcaddr in relations:
		relations[srcaddr][dstaddr] = octets

	# This is the case where: we read 5->8 and then we read, 2 -> 5,
	# we add to the list of the 5 dst's the number 2.

	elif dstaddr in relations:
		relations[dstaddr][srcaddr] = octets

	# The last option is that we are reading a new src ip. So,
	# We only need to add it to the Hash.

	else:
		relations[srcaddr] = {dstaddr:octets}

def setFlowInfo(Flow_Set,srcIp,dstIp,src_prefix,dst_prefix):
	i = 0
	N = 200
	if srcIp != 'null': srcIp = getIpOctets(srcIp,src_prefix)
	if dstIp != 'null': dstIp = getIpOctets(dstIp,dst_prefix)

	# If the src and dest. Ip are empty, by default, we return all the information inside the flow.
	if (srcIp == "null" and dstIp == "null") or (src_prefix==0 and dst_prefix==0):
		for flow in Flow_Set:
			addRelation(flow.srcaddr,flow.dstaddr,flow.dOctets)
			i+=1
			if i == N: break
	# If the user asks for an IP address, we search the IP in the flow.
	# This is the case where the user filled src and dst ip fields.
	elif srcIp != 'null' and dstIp != 'null':
		for flow in Flow_Set:
			if srcIp == getIpOctets(flow.srcaddr,src_prefix):
				addRelation(flow.srcaddr,flow.dstaddr,flow.dOctets)
				#f.write("%s\n"%flow.srcaddr)

			if dstIp == getIpOctets(flow.dstaddr,dst_prefix):
				addRelation(flow.srcaddr,flow.dstaddr,flow.dOctets)
			i+=1
			if i == N: break

	# This case, src but not dst.
	elif srcIp != 'null' and dstIp == 'null':
		for flow in Flow_Set:
			if srcIp == getIpOctets(flow.srcaddr,src_prefix):
				addRelation(flow.srcaddr,flow.dstaddr,flow.dOctets)
			i+=1
			if i == N: break
	# This case, dst but not src. 
	else:
		for flow in Flow_Set:
			if dstIp == getIpOctets(flow.dstaddr,dst_prefix):
				addRelation(flow.srcaddr,flow.dstaddr,flow.dOctets)
			i+=1
			if i == N: break


def getAdjacency(dst,src,color):
	return """{
		"nodeTo": "%s",
		"nodeFrom": "%s",
		"data":{
			"$color":"%s"
		}
	}"""%(dst,src,color)

def getNodeProperty(conn_id,name):
	return """],
			"data": {
				"$color": "ff0000",
				"$type": "circle",
				"$dim": 10
			},
			"id": "%s",
			"name": "%s"
		}"""%(conn_id,name)

def genJsonFile():

	color_list=["#ffffff"]
	index = 0
	json = "["
	last_src = relations.keys()[-1]
	for src in relations:
		#print 'src = %s, last_src = %s'%(src,last_src)
		json+= """{"adjacencies":["""
		last_dst = relations[src].keys()[-1]
		#print '\n\n'
		for dst in relations[src]:
			#print 'dst = %s, last_dst = %s\n\n'%(dst,last_dst)
			json+=getAdjacency(dst,src,color_list[0])
			if dst != last_dst:json+=','

		json+=getNodeProperty(src,src)
		if src != last_src:json+=','
	json+=']'

	return json
	
