# This Class contains the filter Function for flows

import flowtools
import socket
import struct

class StripFlowData:

	def StripFlowData(self, flow, network):
		in_id = None
		out_id = None

		if flow.input in network["int"].keys():
			in_id = "int"
			in_label = flow.input

		elif flow.src_as in network["as"].keys():
			in_id = "as"
			in_label = flow.src_as
		else:
			in_label = self.CheckByNetwork(flow.srcaddr, network)
			if in_label:
				in_id = "net"

		if flow.output in network["int"].keys():
			out_id = "int"	
			out_label = flow.output	

		elif flow.dst_as in network["as"].keys():
			out_id = "as"
			out_label = flow.dst_as
		else:
			out_label = self.CheckByNetwork(flow.dstaddr, network)
			if out_label:
				out_id = "net"

		if in_id:
                #        print in_id,in_label,flow.dOctets,'IN'
			network[in_id][in_label]["i"][0] += flow.dOctets
		 	network[in_id][in_label]["i"][1] += flow.dPkts
			network[in_id][in_label]["i"][2] += 1
                        
			
			if flow.srcport in network[in_id][in_label]["port"].keys():
                                #print in_id,in_label,flow.srcport,flow.dOctets,'PORT'
				network[in_id][in_label]["port"][flow.srcport]["i"][0] += flow.dOctets
				network[in_id][in_label]["port"][flow.srcport]["i"][1] += flow.dPkts
				network[in_id][in_label]["port"][flow.srcport]["i"][2] += 1

			if out_id and out_label and network[in_id][in_label]["to"][out_id].has_key(out_label):
				network[in_id][in_label]["to"][out_id][out_label]["i"][0] += flow.dOctets
			 	network[in_id][in_label]["to"][out_id][out_label]["i"][1] += flow.dPkts
				network[in_id][in_label]["to"][out_id][out_label]["i"][2] += 1


		if out_id:
                 #       print out_id,out_label,flow.dOctets,'OUT'
			network[out_id][out_label]["o"][0] += flow.dOctets
		 	network[out_id][out_label]["o"][1] += flow.dPkts
			network[out_id][out_label]["o"][2] += 1
	
			if flow.dstport in network[out_id][out_label]["port"].keys():
				network[out_id][out_label]["port"][flow.dstport]["o"][0] += flow.dOctets
				network[out_id][out_label]["port"][flow.dstport]["o"][1] += flow.dPkts
				network[out_id][out_label]["port"][flow.dstport]["o"][2] += 1


	def SearchNetwork(self, key_addr, addresses):
		# Binary Search for network.  Receive an address, convert it to network
		# Binary Check if it is in the list of networks.	
		first = 0
		last = len(addresses) - 1
		key = struct.unpack("!L", socket.inet_aton(key_addr))[0]
		
		while first <= last:
			mid = (first + last) / 2
			if key >= addresses[mid][0] and key <= addresses[mid][1]:
				return 1
			if key > addresses[mid][0]:
				first = mid + 1
			else:
				last = mid -1
			

		return 0
		
	def CheckByNetwork(self, addr, network):
		#For now it only works with /32 /24 /16 and /8
		for net in network["net"]:
			# Plan on sorting all networks and do a binary search
			if self.SearchNetwork(addr, network["net"][net]["address"]):
				return net	
		return None

