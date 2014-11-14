#!/usr/bin/python

import cgi, os
import cgitb; cgitb.enable()
from time import gmtime,strftime
import flowtools
import socket
import sys

form = cgi.FieldStorage()

PARSE = form.getvalue("PARSE")
fname = form.getvalue("f_name")
srcIp = form.getvalue("srcIp")
dstIp = form.getvalue("dstIp")
src_prefix=form.getvalue("src_pre")
dst_prefix=form.getvalue("dst_pre")
rmv_file = form.getvalue("rmv")
getList = form.getvalue("gl")
file_number = 1
thold = form.getvalue("thold")
thold_value = form.getvalue("tvalue")

print "Content-Type: text/html"
print

#================================================================================
				#FUCNTIONS DEFINITION				|
#================================================================================

#********************************************************************************
# The function get_form() prints the html content to let the user upload a file *
# again to the server.								*
# Pre: function does not recieves any parameter.				*
# Post: The function returns the web page with the upload form.			*
#********************************************************************************

def get_form(file_number,append):
	print """
<html>
        <head>
                <link href="/~jgrullon/bootstrap/css/bootstrap.min.css" rel="stylesheet">
                <link rel="stylesheet" type="text/css" href="confstyle.css">
        </head>
        <body onload="""
	if append == 0: print "'warn_disp(0);'>"
	elif append == 1: print "'warn_disp(1);'>"
	else: print "'appendToParent();'>"
	print """
                <form action="fup.cgi" method="post" id= "myform" name = "form" enctype="multipart/form-data"
                onsubmit = "return (document.form.hidden_id.value.length? true : false);" target = "_self" >
                        <input type="file" id = "fname" style="display: none" onChange="Handlechange();" name="filename" />
                        <input type="text" class = 'large-inp' id="new_box" readonly=true/>
                        <input type = "hidden" id = "hidden_id" value = "%s"/>
			<input type = "hidden" name = "file_number" value = "%s"/>
                        <input class = 'btn btn-mini' type="button" value="Select Flow" marginwidth = "0px" marginheight = "0px" onclick= "document.getElementById('fname').click();"/>
                        <input class = 'btn btn-mini' id='formSubBtn' type="submit" value="Upload Flow"
                                onclick = "document.form.hidden_id.value = document.form.fname.value;"/>
                </form>
                <script>	
					var pw = window.parent;
					function lst_rqst(fname){
						setAcInput(((pw.getData('fup.cgi?gl=1&f_name='+fname)).split("div")),'append');
					}
					function setAcInput(data,action){
						pw.srcfnList=(action=='append'?data[0].split(","):"");
						pw.dstfnList=(action=='append'?data[1].split(","):"");
						pw.$("#srcIp").autocomplete("option",{ source: pw.srcfnList });
						pw.$("#dstIp").autocomplete("option",{ source: pw.dstfnList });
					}
					function rmvParentElement(btn_element){
						btn_element.parentNode.parentNode.removeChild(btn_element.parentNode);
						if(btn_element.parentElement.children[0].checked)setAcInput("",'remove');	
					}
               		function appendToParent(){
						pw.document.getElementById("fn_list").style.display = "block";
						pw.document.getElementById("fn-ulist").innerHTML +="<li class = 'fn_el' onclick = 'if (this.children[0].checked) return false ;this.children[0].checked=true;"+'document.getElementById("frm").contentWindow.lst_rqst(this.children[2].value);'+"'><input type = 'radio' name = 'fn_lst_inp'><span>%s</span><input type = 'hidden' value = '%s'><button type = 'button' name = 'c_b_r' class = 'close' onclick = 'getData("+'"fup.cgi?rmv=1&f_name="+this.parentNode.children[2].value);this.parentNode.onclick = function(evt){evt.preventdefault;};document.getElementById("frm").contentWindow.rmvParentElement(this);'+"'>&times</button></li>" ;
						pw.document.getElementById('fn-ulist').lastChild.click();
					}
	
					function warn_disp(errorID) {
						(errorID==0?pw.document.getElementById("b_alert").style.display = "block":pw.document.getElementById("bf_alert").style.display = "block")
					}
                       
					function Handlechange(){
                              	// if the user selected a file, we remove the path and display only the name of the file.
                                document.getElementById("new_box").value  = document.form.fname.value.length?(document.form.fname.value).substring(12) : "";
					}
                </script>
        </body>
</html>
"""%(full_fname,file_number,(full_fname[21:53],full_fname[21::])[len(full_fname)<=33],full_fname[0:20])

#********************************************************************************
# The function getIpOctets split an Ip address into network class. For instance,*
# if ip = "136.234.112.3" and the number of octets is 2, the function will      *
# return "136.234".                                                             *
# Pre: the function recieves the whole Ip address and the number of octects to  *
# return.                                                                       *
# Post: The function returns a string containing the new ip address.            *
#********************************************************************************

def getIpOctets(ip,octet_numbers):
	#if block_numbers==0:return ip_address
	ip = ip.split('.') # we get a list with all the octects
	newIp = "" # this variable holds the new ip.
	ip_index = 0 # counter to put only doc between numbers. We do not want, "136.234."
	for i in ip[0:octet_numbers]: # we only take the octects selected by the user.
		#following line doesn't work in version 2.4.3 of python.
		#newIp+=i+("." if count != n-1 else "") # we add a point after each octect execpt the last.
     	#instead we use:
		newIp+=i+("",".")[ip_index!=octet_numbers-1]
		ip_index+=1
	return newIp

def connThold(thold,thold_value,octets,packets):
	thold_value = thold_value.split('|')
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

def parse_ip(src_prefix,dst_prefix):
	
	tmp_list = [] # this list will contain all the data within a flow. Unix time, src ip, dst ip, ports, etc.
	traffic_data = "" # this variable holds all the traffic data in a single string to return it to the client side.
	f = open('ip.txt','w')
	flow_path = os.getcwd()+'/flows_repository/'+fname[0:20]	
	
	# We check that the file to be opened exists.
	if os.path.exists("%s"%flow_path):
		try: 
			Flow_Set = flowtools.FlowSet("%s"%flow_path)
		except:
			print "-1"
			return
		i = 0
		src_prefix=(int(src_prefix)/8,0)[int(src_prefix)==0]
		dst_prefix=(int(dst_prefix)/8,0)[int(dst_prefix)==0]
		# If the src and dst Ip are empty, by default, we return all the information inside the flow.
		if (srcIp == "null" and dstIp == "null") or (src_prefix==0 and dst_prefix==0):
			tmp =0
			for flow in Flow_Set:
				tmp_list.append("%s %s %s %s %s\n" % ( flow.unix_secs, str( int(socket.inet_aton(flow.srcaddr).encode('hex'),16) ) ,
				str( int(socket.inet_aton(flow.dstaddr).encode('hex'),16) ), flow.dstport, connThold(thold,thold_value,flow.dOctets,flow.dPkts) ))
				f.write("%s\n"%flow.srcaddr)
		
		# If the user asks for an IP address, we search the IP in the flow. 	
		# This is the case where the user filled src and dst ip fields.
		elif srcIp != 'null' and dstIp != 'null':
			for flow in Flow_Set:
				if getIpOctets(srcIp,src_prefix) == getIpOctets(flow.srcaddr,src_prefix):
					tmp_list.append("%s %s %s %s %s\n" % ( flow.unix_secs, str( int(socket.inet_aton(flow.srcaddr).encode('hex'),16) ) ,
					str( int(socket.inet_aton(flow.dstaddr).encode('hex'),16) ),flow.dstport,flow.dOctets,flow.dPkts))
					f.write("%s\n"%flow.srcaddr)
				if getIpOctets(dstIp,dst_prefix) == getIpOctets(flow.dstaddr,dst_prefix):
					tmp_list.append("%s %s %s %s %s\n" % ( flow.unix_secs, str( int(socket.inet_aton(flow.srcaddr).encode('hex'),16) ) ,
					str( int(socket.inet_aton(flow.dstaddr).encode('hex'),16) ),flow.dstport,flow.dOctets,flow.dPkts))
		
		# This case, src but not dst.
		elif srcIp != 'null' and dstIp == 'null':
			for flow in Flow_Set:
				if getIpOctets(srcIp,src_prefix) == getIpOctets(flow.srcaddr,src_prefix):
					tmp_list.append("%s %s %s %s %s\n" % ( flow.unix_secs, str( int(socket.inet_aton(flow.srcaddr).encode('hex'),16) ) ,
					str( int(socket.inet_aton(flow.dstaddr).encode('hex'),16) ),flow.dstport,flow.dOctets,flow.dPkts))
					f.write("%s\n"%flow.srcaddr)
		# This case, dst but not src.
		else:
			for flow in Flow_Set:
				if getIpOctets(dstIp,dst_prefix) == getIpOctets(flow.dstaddr,dst_prefix):
					tmp_list.append("%s %s %s %s %s\n" % ( flow.unix_secs, str( int(socket.inet_aton(flow.srcaddr).encode('hex'),16) ) ,
					str( int(socket.inet_aton(flow.dstaddr).encode('hex'),16) ),flow.dstport,flow.dOctets))
					f.write("%s\n"%flow.dstaddr)
		#	print getIpOctets(flow.dstaddr,dst_prefix) 	
	
		tmp_list.sort() # We sort all the data
		for i in tmp_list: 
			traffic_data += i # The content of the flow is returned to the client side.
		print traffic_data														

#********************************************************************************
# The function retIpList, returns to the client side, a list containing all the *
# src and dst IP address inside a flow.						*
# Pre: It doesnt receive any parameter.						*
# Post: The function returns a single string with all the Ips 	               	*
#********************************************************************************

def retIpList():
	flow_path=os.getcwd()+'/flows_repository/'+fname[0:20]
	# We check that the file to be opened exists.
	if os.path.exists("%s" %flow_path):
		try: Flow_Set = flowtools.FlowSet("%s"%flow_path)
		except:
			print "-1"
			return

		src=dst='' #holds the variable that will be returned to client
		slist=dlist = [] #this list 
		index=0
		#First, we put all the src and dst ip on a list
		for flow in Flow_Set:
			slist.append("%s"%(flow.srcaddr))
			dlist.append("%s"%(flow.dstaddr))
		#Now we convert both lists in sets to eliminate repeated elements		
		slist=list(set(slist))
		dlist=list(set(dlist))
		#We append all the ip in one string separated by a comma(',') except the last string.
		for sip,dip in map(None,slist,dlist):
			src+="%s"%sip+(",","")[slist[index]==slist[len(slist)-1]]
			dst+="%s"%dip+(",","")[dlist[index]==dlist[len(dlist)-1]]
			index+=1
		#We append src + dst but with a special word(div) to parse it in the client side.
		print src[0:len(src)-1]+"div"+dst[0:len(src)-1]

#================================================================================
#				SERVER RESPONSE					|
#================================================================================
	#we check if the form has the key of the variable filename.
if form.has_key("filename"):
	fileitem = form['filename'] #We get the file upload object.
	full_fname = strftime("%d-%b-%Y-%X",gmtime())+"|"+os.path.basename(fileitem.filename) #newfilename+|+userfilename
	flow_path = os.getcwd()+'/flows_repository/'+full_fname[0:20] #holds the path of the flow.
	open(flow_path,'w').write(fileitem.file.read()) #we save the file..
	#if the file is oppened, we display the form with the filname added to the menu. If not,
	#it means that the file was not a flow file.
	try:
		flowtools.FlowSet("%s"%flow_path)
		get_form(file_number,2) 
	#else, we remove the file and we return a message indicating that the file was not a valid flow.
	except: 
		os.system('rm %s'%flow_path)
		get_form(file_number,1)
#We return the ip list
elif form.has_key('gl'): 
	retIpList()
#remove the requested file.
elif form.has_key('rmv'):
	os.system('rm %s'%os.getcwd()+'/flows_repository/'+fname[0:20])
#all the information to display is returned.
elif PARSE: parse_ip(src_prefix,dst_prefix)
