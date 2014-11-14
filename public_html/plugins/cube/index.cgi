#!/usr/bin/python

import cgi, os
import cgitb; cgitb.enable()
# from time import gmtime,strftime
import flowtools
from cube import * 
sys.path.append('../../../bin/')
from Config import Config
config=Config()
GRAPH_PATH=config.getGraphsPath()
import datetime
sys.path.append('../../Models/')
from SessionModel import SessionModel
# from time import gmtime,strftime


#We get the input parameters received from frontend.
form = cgi.FieldStorage()

PARSE = form.getvalue("PARSE")
fname = form.getvalue("f_name")
srcIp = form.getvalue("srcIp")
dstIp = form.getvalue("dstIp")
date = form.getvalue("date")
time = form.getvalue("time")
src_prefix=form.getvalue("src_pre")
dst_prefix=form.getvalue("dst_pre")
getList = form.getvalue("gl")
fromtoa = form.getvalue("fromtoa")
thold = form.getvalue("thold")
thold_value = form.getvalue("tvalue")

print "Content-Type: text/html"
print

#================================================================================
				#FUCNTIONS DEFINITION				|
#================================================================================

def validate(form):
    if form.has_key('uid') and form.has_key('sid') and form.has_key('remote'):
        uid=form.getvalue('uid')
        sid=form.getvalue('sid')
        remote=form.getvalue('remote')
        now = datetime.datetime.now()#generate the TimeStamp

        tmstp = now.minute#converting the TimeStamp to string   

        sm = SessionModel()


        if sm.connect():

            timestamp = sm.Validate(uid, sid, remote)
            #print "timestamp = ",timestamp
            if((timestamp+5)<=tmstp or timestamp == -1):

                sm.Close(uid, remote)
	
                del sm
                return 0
            else:
                return 1
        else:
            return 0
        return 1
    else:
            return 0



def getPage(page_filename):
	f=open(page_filename)
	p = f.read()
	f.close()
	return p


#================================================================================
#				SERVER RESPONSE					|
#================================================================================
uid=form.getvalue('uid')
sid=form.getvalue('sid')
remote=form.getvalue('remote')

#print "uid = ",uid
#print "sid = ",sid
#print "remote = ",remote
#we check if the form has the key of the variable filename.
if not validate(form): 

	print """
<!DOCTYPE html>
<html>
	<head></head>
	<body>
		<script language=javascript type=text/javascript>												
			window.location.href='../../';
		</script>
	</body>
</html>"""
	exit()

if PARSE != None: PARSE=int(PARSE)
else: PARSE=0

#if the request is from toa and the request is not for parsing, then the request
#is to display the cube and send the name of the file to be requested once the 
# cube is displayed. 
v = Validation()
if fromtoa!=None and PARSE in (0,1):
	#if the request is not for parse, that means that this is the first time the plugin is invoked from
	# toa, so we print the cube page.
	fromtoa = fromtoa.replace("'","")
	length = len(fromtoa)
	
	if PARSE == 0:
		if length == 19 or length == 8:
			print getPage('netcube.html')%(fromtoa,uid,sid,remote)
		else:
			print getPage('netcube.html')%("null","null","null","null")
		
		# elif length == 8:
		# 	complete_path,date = currentDayPath(fromtoa)
		# 	print getPage('netcube.html')%date

	#if the request is to parse the data coming from toa, means that the request came from TOA and it is the
	# first time the cube execute, so we return the data to the user.

	elif PARSE == 1:
		#Default data.
		srcIp=dstIp="null"
		src_prefix=dst_prefix=0
		thold='octets'
		thold_value='1|1024'

		if length == 19:
			y = fromtoa[0:4]
			m = fromtoa[5:7]
			d = fromtoa[8:10]
			hour = fromtoa[11:13]
			minutes=fromtoa[14:16]
			complete_path = FLOWS_LOCATION+"/%s/%s-%s/%s-%s-%s/ft-v05.%s-%s-%s.%s%s00-0400" % (y,y,m,y,m,d,y,m,d,hour,minutes)
			Flow_Set = v.validateFlow(complete_path)
			if Flow_Set == -1: print -1
			#thold='octect'|packet ; thold_value = thold_size|unidad(kb,mb,gb)
			else: print parse_ip(Flow_Set,srcIp,dstIp,src_prefix,dst_prefix,thold,thold_value)
			
		elif length == 8:

			complete_path= currentDayPath(fromtoa)
			Flow_Set = v.validateFlow(complete_path)
			if Flow_Set == -1: print -1
			else: print parse_ip(Flow_Set,srcIp,dstIp,src_prefix,dst_prefix,thold,thold_value)
			
		else:
			print getPage('netcube.html')%("null","null","null","null")

	else:
		print getPage('netcube.html')%("null","null","null","null")

elif PARSE == 1 and date != None and time != None:
	if len(date)==10 and len(time)==5:
		y = date[6:10]
		m = date[0:2]
		d = date[3:5]
		hour = time[0:2]
		minutes= time[3:5]
		complete_path = FLOWS_LOCATION+"/%s/%s-%s/%s-%s-%s/ft-v05.%s-%s-%s.%s%s00-0400" % (y,y,m,y,m,d,y,m,d,hour,minutes)
		Flow_Set = v.validateFlow(complete_path)
		if Flow_Set == -1: print -1
		else: print parse_ip(Flow_Set,srcIp,dstIp,src_prefix,dst_prefix,thold,thold_value)
	

else:
	print getPage('netcube.html')%("null")