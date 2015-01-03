#!/usr/bin/python

import cgi, os
import cgitb; cgitb.enable()
import string
# from time import gmtime,strftime
import flowtools
from cube import *
sys.path.append('../../../bin/')
from Config import Config
config=Config()
FLOWS_LOCATION=config.getFlowsPath()
import time as mytime
sys.path.append('../../Models/')
from SessionModel import SessionModel

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
        now = mytime.time()#generate the TimeStamp

        sm = SessionModel()

        if sm.connect():

            timestamp = sm.Validate(uid, sid, remote, now)
            if not timestamp:

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
		print parse_ip(Flow_Set,srcIp,dstIp,src_prefix,dst_prefix,thold,thold_value)
	
	sys.exit() 

print """
<!doctype html>
<html lang="en">
	<head>
		<link rel="shortcut icon" href="../style/img/favicon.ico"/>
		<title> Network Monitoring Tool</title>
		<!-- <script src="../build/Three.js" > </script>  -->
		
		<script src="../js/three.min.js"></script>
		<link rel="stylesheet" href="http://code.jquery.com/ui/1.9.0/themes/base/jquery-ui.css">
		<script src="../style/jQuery/jquery-1.8.2.js"></script>
		<script src="../style/jQuery/jquery-ui.js"></script>
		<link href = "../style/css/bootstrap/css/bootstrap.min.css" rel = "stylesheet">
		<link rel="stylesheet"type="text/css"href="../style/css/confstyle.css"/>
		<script src="../style/jQuery/jquery-ui-timepicker-0.3.1/jquery.ui.timepicker.js"></script>
		<link href = "../style/jQuery/jquery-ui-timepicker-0.3.1/jquery.ui.timepicker.css" rel = "stylesheet">
		<script src="ctrpan.js" defer></script>

	</head>

	<body>
	
	<div id='axis_legend'>
		<table>
			<tr>
				<td id= 'x_Axis'></td>
				<td>X Axis</td>
			</tr>
			<tr>
				<td id = 'y_Axis'></td>
                <td>Y Axis</td>
            </tr>
			<tr>
                <td id = 'z_Axis'></td>
                <td>Z Axis</td>
            </tr>
		</table>
	</div>

	<div id='settings'>
		<div id = "sett_title">Settings</div>
		<div id ='updwn'><button id = 'chlBtn' class = 'btn dflt_cstm_btn'>HIDE MENU</button></div>
		<div id ='main_content'>
		<input id = 'flow_date' type = 'hidden' value = '%s'>
		<input id = 'uid' type = 'hidden' value = '%s'>
		<input id = 'sid' type = 'hidden' value = '%s'>
		<input id = 'remote' type = 'hidden' value = '%s'>

		<div>
	        	<h4> File Upload </h4>
				<div align="left" <p>Flow Date:</p> <input type="text" name = "fecha" placeholder='Click to set date' id="datepicker" size = "17" maxlength = "10" value="%s"/>
                <p>Time: </p><input type = "text" name = "hora" placeholder = 'Click to set time' id = "timepicker" value="%s"/>
				<h4>Filter Connections</h4>
				<div id = "add_opt">	
					<div id = 's_em' class="alert-error e_alert"></div>
					<div id='src_inp'>
						<div id = 's_ip_inp'>	
							<input class = 'input-medium' id = "srcIp" type="text" maxlength="15"
							placeholder = "Source IP" title = "Field to filter by source IP." >
						</div>
						<select id = "src_pre">
							<option value = "0">/0</option>
							<option value = "8">/8</option>
		                			<option value="16">/16</option>
		                			<option value="24">/24</option>
		                			<option value="32">/32</option>
			        		</select>
					</div>
					<div id = 'd_em' class="alert-error e_alert"></div>
					<div id = 'dst_inp'>
						<div id ='d_ip_inp'>
							<input class = 'input-medium' id = "dstIp" type="text" maxlength="15" 
							placeholder = "Destination IP" title = "Field to filter by destination IP.">
						</div>
						<select id = "dst_pre">
							<option value = "0">/0</option>
							<option value = "8">/8</option>
		                			<option value="16">/16</option>
		                			<option value="24">/24</option>
		                			<option value="32">/32</option>
			        		</select>
					</div>
				</div>
				<h5>Threshold</h5>
	            <div id='th'>
	            <select id='opt'>
	                <option value='octets'>Octets</option>
	                <option value='packets'>Packets</option>
	            </select>
	                <input type='text' id ='threshold_size' placeholder='Size' class='input-small'>
	                <select id='unit'>
	                    <option value='1024'>KB</option>
	                    <option value='1048576'>MB</option>
	                    <option value='1073741824'>GB</option>
	                </select>
	            </div
			</div>
			<button id = 'dsp_btn' class = 'btn dflt_cstm_btn' type="submit" name="button"  marginheight = "0px"
                		onClick = "this.disabled='disabled';dspData(1);this.disabled=false;"; >Display</button>
			<button type = "button" class = 'btn dflt_cstm_btn' id = "second_menu_btn" align = "left" ><b>Axis Colors</b></font></button>
			<div id ='axis_menu'>
				<span>X:</span>
				<select name="X_COLOR" id = "x_color_id" onchange = "renderCube();renderCube();document.getElementById('x_Axis').style.backgroundColor='#'+this.options[this.selectedIndex].value.substring(2,this.options[this.selectedIndex].length)">
                            		<option value= "0x0" selected>BLACK</option>      
                                	<option value= "0xFF0033">RED</option> 
                                	<option value= "0x00FF00">GREEN</option>
                                	<option value="0x0000FF">BLUE</option>
					<option value="0x996600">BROWN</option>
                                	<option value="0X660000">WINE</option>
                                	<option value="0xFFFF00">YELLOW</option>
					<option value="0xFF9900">ORANGE</option>
                        	</select><br>
				<span>Y:</span>
				<select name="Y_COLOR" id = "y_color_id" onchange = "renderCube();renderCube();document.getElementById('y_Axis').style.backgroundColor='#'+this.options[this.selectedIndex].value.substring(2,this.options[this.selectedIndex].length)">
                                	<option value= "0x0" selected>BLACK</option>      
                                	<option value= "0xFF0033">RED</option> 
                                	<option value= "0x00FF00">GREEN</option>
                                	<option value="0x0000FF">BLUE</option>
                                	<option value="0x996600">BROWN</option>
                                	<option value="0X660000">WINE</option>
                                	<option value="0xFFFF00">YELLOW</option>
                                	<option value="0xFF9900">ORANGE</option>
                        	</select><br>
				<span>Z:</span>
				<select name="Z_COLOR" id = "z_color_id" onchange = "renderCube();document.getElementById('z_Axis').style.backgroundColor='#'+this.options[this.selectedIndex].value.substring(2,this.options[this.selectedIndex].length)">
                        		<option value= "0x0" selected>BLACK</option>      
                                	<option value= "0xFF0033">RED</option> 
                        		<option value= "0x00FF00">GREEN</option>
                                	<option value="0x0000FF">BLUE</option>
                                	<option value="0x996600">BROWN</option>
                                	<option value="0X660000">WINE</option>
                                	<option value="0xFFFF00">YELLOW</option>
                                	<option value="0xFF9900">ORANGE</option>	    	
				</select>	
			</div>	
		</div>
	</div>
</div>
	<div id ='aut_cmpl'></div>
</body>
</html>
""" % (fromtoa, uid, sid, remote, fecha, hora)
