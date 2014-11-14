#!/usr/bin/python
from net_tools import *
import sys,time
from datetime import datetime
import socket

# from Config import Config

traffic_data = "" # this list will contain all the data within a flow. Unix time, src ip, dst ip, ports, etc.

def connThold(thold,thold_value,octets,packets):
    
    thold_value = thold_value.split('|')

    if len(thold_value[0])==0: thold_value[0]='10'
    size = int(thold_value[0])
    unit_size = int(thold_value[1])
    #print 'size: %s, byte_size: %s'%(size,unit_size)
    if thold == 'packets':
        if packets > size: return 1
    else:
        if size == '': return 0
        if octets > size*unit_size: return 1
    return 0

#********************************************************************************
# The function parse_ip, parse all the ip wanted by the user.			*
# Pre: The function recieves two strings with the src IP and dst IP. It could   *
# be null.									*
# Post: The function returns a string holding all the matched Ip.	        *
#********************************************************************************

def parse_ip(Flow_Set,srcIp,dstIp,src_prefix,dst_prefix,thold,thold_value):
	global traffic_data # this variable holds all the traffic data in a single string to return it to the client side.
	tmp_list=[]
	src_prefix=(int(src_prefix)/8,0)[int(src_prefix)==0]
	dst_prefix=(int(dst_prefix)/8,0)[int(dst_prefix)==0]
	new_srcIP = getIpOctets(srcIp,src_prefix)
	new_dstIP = getIpOctets(dstIp,dst_prefix)
	max_flow =5000
	i=0
	# If the src and dst Ip are empty, by default, we return all the information inside the flow.
	if (srcIp == "null" and dstIp == "null") or (src_prefix==0 and dst_prefix==0):
		
		for flow in Flow_Set:
			tmp_list.append("%s %s %s %s %s\n" % ( flow.unix_secs, str( int(socket.inet_aton(flow.srcaddr).encode('hex'),16) ) ,
			str( int(socket.inet_aton(flow.dstaddr).encode('hex'),16) ), flow.dstport, connThold(thold,thold_value,flow.dOctets,flow.dPkts) ))
			if i==max_flow: break
			i+=1
	# If the user asks for an IP address, we search the IP in the flow. 	
	# This is the case where the user filled src and dst ip fields.
	elif srcIp != 'null' and dstIp != 'null':
		for flow in Flow_Set:
			if new_srcIP == getIpOctets(flow.srcaddr,src_prefix):
				tmp_list.append("%s %s %s %s %s\n" % ( flow.unix_secs, str( int(socket.inet_aton(flow.srcaddr).encode('hex'),16) ) ,
				str( int(socket.inet_aton(flow.dstaddr).encode('hex'),16) ),flow.dstport,connThold(thold,thold_value,flow.dOctets,flow.dPkts) ))
				# f.write("%s\n"%flow.srcaddr)
			if new_dstIP == getIpOctets(flow.dstaddr,dst_prefix):
				tmp_list.append("%s %s %s %s %s\n" % ( flow.unix_secs, str( int(socket.inet_aton(flow.srcaddr).encode('hex'),16) ) ,
				str( int(socket.inet_aton(flow.dstaddr).encode('hex'),16) ),flow.dstport,connThold(thold,thold_value,flow.dOctets,flow.dPkts) ))
			if i==max_flow: break
			i+=1

	# This case, src but not dst.
	elif srcIp != 'null' and dstIp == 'null':
		for flow in Flow_Set:
			#print thold_value,type(thold_value)
			if new_srcIP == getIpOctets(flow.srcaddr,src_prefix):
				tmp_list.append("%s %s %s %s %s\n" % ( flow.unix_secs, str( int(socket.inet_aton(flow.srcaddr).encode('hex'),16) ) ,
				str( int(socket.inet_aton(flow.dstaddr).encode('hex'),16) ),flow.dstport,connThold(thold,thold_value,flow.dOctets,flow.dPkts) ))
			if i==max_flow: break
			i+=1
	# This case, dst but not src.
	else:
		for flow in Flow_Set:
			if new_dstIP == getIpOctets(flow.dstaddr,dst_prefix):
				tmp_list.append("%s %s %s %s %s\n" % ( flow.unix_secs, str( int(socket.inet_aton(flow.srcaddr).encode('hex'),16) ) ,
				str( int(socket.inet_aton(flow.dstaddr).encode('hex'),16) ),flow.dstport,connThold(thold,thold_value,flow.dOctets,flow.dPkts) ))
			if i==max_flow: break
			i+=1

	tmp_list.sort() # We sort all the data
	return "".join(tmp_list)
	# for i in tmp_list: 
	# 	traffic_data += i # The content of the flow is returned to the client side.
	# return traffic_data

def currentDayPath(hour):
	PATH="/CassandraVol/flows/"
	INCREMENT=300
	now=datetime.now()
	unixtime=time.mktime(now.timetuple())
	unixtime=(unixtime-(unixtime%INCREMENT))-INCREMENT
	filetime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(unixtime))

	filetime=filetime.split(' ')
	year_month_day=filetime[0]
	hour=("".join(hour.split(':')))
	year=year_month_day[0:4]
	#[5:7]=month ; [8:]= day ; year
	# date = year_month_day[5:7] + "/" + year_month_day[8:] + "/" + year
	year_month=year_month_day[0:7]
	PATH=PATH+'/'+year+'/'+year_month+'/'+year_month_day+'/ft-v05.'+year_month_day+'.'+hour+'-0400'
	return PATH

if __name__ == "__main__":
	print currentDayPath("13:55:00")
	for i in range(1,5):
		print getIpOctets('null',i) +'--\n'
