#!/usr/bin/python

########### Imports #######################

import cgi
import sys 
import os
import cgitb
import datetime
import urllib, hashlib
import sys
sys.path.append("../../Models")
from SessionModel import SessionModel
from NetworkModel import NetworkModel
from UserModel import UserModel

#cgitb.enable()

########## Imports #######################

############### Init #######################

print "Content-Type: text/html\n\n"

print 

form = cgi.FieldStorage()#getting the values of the form in case of a validation error

uid = form.getvalue("uid")

uid = str(uid).strip("(),L")

uid = int(uid)

sid = form.getvalue("sid")

remote = form.getvalue("remote")

now = datetime.datetime.now()#generate the TimeStamp

tmstp = now.minute#converting the TimeStamp to string   

SessionModel = SessionModel()

NetworkModel = NetworkModel()

UserModel = UserModel()

timestamp = SessionModel.Validate(uid, sid, remote)

if form.has_key("iframe_display"):
        
	iframe_display = form.getvalue("iframe_display")

else:

    iframe_display = "p2p"

##################### Init ##########################################

if((timestamp+5)<=tmstp or timestamp == -1):

    SessionModel.Close(uid, remote)

    del NetworkModel

    del UserModel

    del SessionModel

    print """<script language=\"JavaScript\">{location.href=\"../../index.cgi\";self.focus();}</script>"""

SessionModel.UpdateTimeStamp(tmstp, uid, remote)

print """        
	
		<head>

        	<title>TOA Network Monitoring System</title>

            <script src='http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js'></script>

            <link rel='stylesheet' type='text/css' href='../../Style/Style.css'>

        	<script type='text/javascript' src='../../Style/Style.js'></script>

            <script type='text/javascript' src='../../Controllers/MenuController.js'></script>

            <script type='text/javascript' src='../../Controllers/GraphController.js'></script>

            <div class=banner>

            	<p>TOA Network Monitoring System</p>

                <div id='user_box'>

                    <p>"""
print UserModel.GetUsername(uid)[0]

print  """ <br>

                    <a href='Home.cgi?uid=%s&sid=%s&remote=%s'>Home</a>&nbsp;

                    <a href='Dashboard.cgi?uid=%s&sid=%s&remote=%s'>Dashboard</a>&nbsp;

                    <a href='Setting.cgi?uid=%s&sid=%s&remote=%s'>Settings</a>

                    </p>

                </div>
			
			</div>                                                                                                                                                                                                                                                                       
		
		</head>
	
		<body>

            <div class=menu>

            	<div id='top_menu_button' onclick='GetNetworksMenu(1)'>

            		<br><br><br><br><br><br><p>Networks</p>

            	</div>

            	<div id='bottom_menu_button' onclick='GetFirstSystemMenu(1)'>

            		<br><br><br><br><br><p>System</p>

            	</div>

            	<div id='menu_content'>


            	</div>

            	<div id='port_net_menu_container'>

            	</div>

            </div>

            <div class='content' id='content'>"""%(uid, sid, remote, uid, sid, remote, uid, sid, remote)

print """<center><ul><li><a href="ManagePorts.cgi?uid=%s&sid=%s&remote=%s"><div id="mMyAcc"><p>My Account</p></div></a></li><li><a href="ManageNet2Net.cgi?uid=%s&sid=%s&remote=%s"><div id="mAcc"><p>Manage Accounts</p></div></a></li><li><a href="../../Controllers/Logout.cgi?uid=%s&sid=%s&remote=%s"><div id="mLog"><p>Logout</p></div></a></li></ul></center>"""%(uid, sid, remote, uid, sid, remote, uid, sid, remote)

del NetworkModel

del UserModel

del SessionModel

print "</div></body>"