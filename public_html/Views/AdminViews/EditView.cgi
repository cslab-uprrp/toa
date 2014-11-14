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
from GraphModel import GraphModel
from UserModel import UserModel
from ViewModel import ViewModel
sys.path.append("../../Controllers")
from FormController import *

########## Imports #######################

############### Init #######################

print "Content-Type: text/html"

print 

form = cgi.FieldStorage()#getting the values of the form in case of a validation error

uid = form.getvalue("uid")

uid = str(uid).strip("(),L")

uid = int(uid)

sid = form.getvalue("sid")

remote = form.getvalue("remote")

vid = form.getvalue("vid")

vid = str(vid).strip("(),L")

vid = int(vid)

now = datetime.datetime.now()#generate the TimeStamp

tmstp = now.minute#converting the TimeStamp to string   

SessionModel = SessionModel()

GraphModel = GraphModel()

ViewModel = ViewModel()

UserModel = UserModel()

if SessionModel.connect() and UserModel.connect() and GraphModel.connect() and UserModel.connect():

    timestamp = SessionModel.Validate(uid, sid, remote)

    ##################### Init ##########################################

    if((timestamp+5)<=tmstp or timestamp == -1):

        SessionModel.Close(uid, remote)

        del GraphModel

        del UserModel

        del SessionModel

        del ViewModel

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

    graphs = GraphModel.GetAll() 

    view_graphs = GraphModel.GetViewGraph("g_id", "v_id", vid)

    vg = ""

    for v in view_graphs:

        vg += str(v)+","

    view_name = ViewModel.Get("view_name", "vid", vid)

    EditViewForm(uid, sid, remote, graphs, view_name, vg, len(view_graphs))

    print "</ul><br></div></center></div></body>"


else:

    print "Database Connection Error. Configuration File Not Found."

del GraphModel

del UserModel

del SessionModel

del ViewModel
