#!/usr/bin/python

import cgi, os
import cgitb; cgitb.enable()
import string
# from time import gmtime,strftime
import flowtools
from graph import *
sys.path.append('../../../bin/')
from Config import Config
config=Config()
FLOWS_LOCATION=config.getFlowsPath()
import datetime
sys.path.append('../../Models/')
from SessionModel import SessionModel
# from time import gmtime,strftime

#We get the input parameters received from frontend.
form = cgi.FieldStorage()

PARSE = form.getvalue("PARSE")
srcIp = form.getvalue("srcIp")
dstIp = form.getvalue("dstIp")
date = form.getvalue("date")
time = form.getvalue("time")
src_prefix=form.getvalue("src_pre")
dst_prefix=form.getvalue("dst_pre")
fromtoa = form.getvalue("fromtoa")

uid=form.getvalue('uid')
sid=form.getvalue('sid')
remote=form.getvalue('remote')

if PARSE != None: PARSE=int(PARSE)
else: PARSE=0

print "Content-Type: text/html"
print

#================================================================================
                                #FUCNTIONS DEFINITION                           |
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


fecha = ""
hora = ""


if not fromtoa and not date and not time or not validate(form):
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
	sys.exit()

if fromtoa:
	if not fromtoa[0].isdigit():
		fromtoa = fromtoa[1:-1]

	fecha, hora = fromtoa.split()
	y, m, d = fecha.split("-")
	fecha = string.join(fecha.split("-"), "/")
	hour, minutes = hora.split(":")[0:2]
	hora= string.join([hour, minutes], ":")
else:
	fecha = date
	hora = time
	y, m, d = date.split('/')
	hour, minutes = time.split(":")[0:2]

if PARSE:
	v = Validation()
	complete_path = FLOWS_LOCATION+"/%s/%s-%s/%s-%s-%s/ft-v05.%s-%s-%s.%s%s00-0400" % (y,y,m,y,m,d,y,m,d,hour,minutes)
        Flow_Set = v.validateFlow(complete_path)
        if Flow_Set == -1: 
		print -1
        else: 
		setFlowInfo(Flow_Set,srcIp,dstIp,src_prefix,dst_prefix)
                print genJsonFile()
	
	sys.exit() 

print """
<!DOCTYPE HTML>

<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<title>Graph Visualization</title>

<link href = "../style/jQuery/jquery-ui-timepicker-0.3.1/jquery.ui.timepicker.css" 
	rel = "stylesheet">
	<script language="javascript" type="text/javascript" src="../js/jit-yc.js"></script>
	<link rel="stylesheet" href="http://code.jquery.com/ui/1.9.0/themes/base/jquery-ui.css">
	<script src="../style/jQuery/jquery-1.8.2.js"></script>
    <script src="../style/jQuery/jquery-ui.js"></script>
	<link type="text/css" href="../style/css/base.css" rel="stylesheet">
	<link type="text/css" href="../style/css/ForceDirected.css" rel="stylesheet">	
	<script language="javascript" type="text/javascript" src="time_graph.js"></script>
	<script src="../style/jQuery/jquery-ui-timepicker-0.3.1/jquery.ui.timepicker.js"></script>
	<link href = "../style/jQuery/jquery-ui-timepicker-0.3.1/jquery.ui.timepicker.css" 
	rel = "stylesheet">
</head>



<body>

<div id='connlist'>
	<div id="inner-details"></div>
</div>

<div id = "c_p" class ='ui-widget-content'>
	<div id = 'cp_title' class ='titleimg'> <h3>Settings</h3><hr></div>
	<div id = 'updwn'>
		
		<div id ="conn_filt_form">
			<div id = 'date_input'>
				<input id = 'flow_date' type = 'hidden' value = '%s'>
				<input id = 'uid' type = 'hidden' value = '%s'>
                		<input id = 'sid' type = 'hidden' value = '%s'>
                		<input id = 'remote' type = 'hidden' value = '%s'>
				<label for ='datepicker' class = 'nonselect'>Flow Date:</label>
				<input type="text" class = 'inp_box global_radius'name = "fecha" placeholder='Click to set date' 
				id="datepicker" size = "17" maxlength = "10"/ value='%s'>
				<label for ='timepicker' class = 'nonselect'>Time:</label>
				<input type = "text" class = 'inp_box global_radius' name = "hora" placeholder = 'Click to set time' id = "timepicker" value='%s'/>
			</div>
			<label class = 'nonselect'>Connections Filter:</label><br></br>
			<div id = 'fields'>
				<input class = 'inp_box global_radius' id='srcIp' placeholder ='Source IP' type='text' size='15' maxlength='15'>
				<select name="menu1" class = 'global_radius' id = "src_pre">
					<option value = "0">/0</option>
					<option value = "8">/8</option>
					<option value="16">/16</option>
					<option value="24">/24</option>
					<option value="32">/32</option>
				</select>
				<input class = 'inp_box global_radius' id='dstIp' placeholder ='Destination IP' type='text' size='15' maxlength='15'>
	
				<select name="menu1" class = 'global_radius' id = "dst_pre">
					<option value = "0">/0</option>
					<option value = "8">/8</option>
					<option value="16">/16</option>
					<option value="24">/24</option>
					<option value="32">/32</option>
				</select>
			</div>
			<span> Display first </span> 
			<input id = 'conn_num' value = "100" class = 'global_radius' type ='text' size = '1' maxlength ='4'/>
			<span>connections.</span><br><br>
			<input type="button" name="button" id = "display_button" value="Display" marginheight = "0px" 
			onclick ="this.disabled = 'disabled';parseData(1);this.disabled = false;" /><br><br>
		</div>
	</div>
</div><br>
	
<div id = "container">
		<div id="left-container">
			<h2>Force Directed Static Graph</h2> 
			<div id="id-list"></div>
		</div>
		<div id = "center-container"><div id="infovis"></div></div>
		<div id="log"></div>
</div>
</body>
</html>
""" % (fromtoa, uid, sid, remote, fecha, hora)
