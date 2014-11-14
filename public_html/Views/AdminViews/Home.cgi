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
from PortModel import PortModel
from Net2NetModel import Net2NetModel

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

UserModel = UserModel()

timestamp = SessionModel.Validate(uid, sid, remote)

##################### Init ##########################################

if((timestamp+5)<=tmstp or timestamp == -1):

    SessionModel.Close(uid, remote)

    del NetworkModel

    del UserModel

    del SessionModel

    print """<script language=\"JavaScript\">{location.href=\"../../index.cgi\";self.focus();}</script>"""

print "Hello"

SessionModel.UpdateTimeStamp(tmstp, uid, remote)

######################### headers  #########################

print "<!DOCTYPE html><html>"

print "<head>"

print "<title>ToaNMS</title>"

print """<link rel="stylesheet" href="../../Style/bootstrap/css/style.css"/>"""

print """<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>"""

print """<script src="../../Style/bootstrap/js/bootstrap.min.js"></script>"""

print """<script src="../../Controllers/GraphController.js"></script>"""

print "</head>"

######################### headers #########################

print "<body>"

######################### banner  #########################

print """<div class="row-fluid" id="banner">"""

print """<div class="span8 offset1" id="app-name">"""
        
print """<h1>Toa Network Monitoring System</h1>"""

print "</div>"

print """<div class="span3" id="user-box">"""
    
print "<div class='row'>"

print "<div class='span12'><h3><center>"

print UserModel.GetUsername(uid)[0]

print "</center></h3></div>"

print "</div>"

print "<div class='row'>"

print "<div class='span12'><center>"

print "<a class='btn btn-inverse' id='login-button' href='Home.cgi?uid=%s&sid=%s&remote=%s'>Home</a>"%(uid, sid, remote)

print "<a class='btn btn-inverse' id='login-button' href='Dashboard.cgi?uid=%s&sid=%s&remote=%s'>Dashboard</a>"%(uid, sid, remote)

print "<a class='btn btn-inverse' id='login-button' href='Setting.cgi?uid=%s&sid=%s&remote=%s'>Settings</a>"%(uid, sid, remote)

print "</center></div>"

print "</div>"

print "</div>"

print "</div>"

######################### banner  #########################

######################### content  #########################

print "<div class='row' id='FeatureBar'>"

print "<br>"

print "<div class='span11 offset1'>"

print """<div class="btn-group">"""

print """<a href='#DeviceMenu' data-toggle="dropdown" class="btn btn-large btn-inverse dropdown-toggle" id="device-button">Device</a>"""        

print "<ul class='dropdown-menu' role='menu'>"

NetworkModel = NetworkModel()

PortModel = PortModel()

Net2NetModel = Net2NetModel()

devices = NetworkModel.GetAll()

for device in devices:

    print "<li class='dropdown-submenu parent'><a href=#Device class='dropdown-hover'>%s</a><ul class='dropdown-menu' id='TripleOptionMenu'><li><a href='#%sInterfaceGraph' onclick='GetGraphsView(%s)'>Interface Graph</a></li><li><a href='#%sPortGraph' onclick=\"GetGraphsView(%s)\">Port Graph<br><select id='PortSelection' onchange='GetPortGraphsView(this.options[this.selectedIndex].value, %s)'>"%(device[1], device[1], device[0], device[0], device[1], device[0])

    ports = PortModel.Get(device[0])

    print "<option value='None'>Select</option>"

    for port in ports:

        print "<option value='%s'>%s</option>"%(port[1], port[1])

    print "</select></a></li><li><a href='#%sNet2NetGraph'>Net2Net Graph<br><select id='N2NSelection' onchange='GetNet2NetGraphsView(this.options[this.selectedIndex].value, %s)'>"%(device[1], device[0])

    net2nets = Net2NetModel.Get(device[0])

    print "<option value='None'>Select</option>"

    for net2net in net2nets:

        print "<option value='%s'>%s</option>"%(net2net[2], net2net[1])

    print "</select></a></li></ul></li>"

del NetworkModel

del PortModel

del Net2NetModel

del UserModel

del SessionModel

print "</ul>"

print "</div>"

print "</div></div>"

print "<br>"

print "<div class='row-fluid' id='Parent'>"

print "<div class='span12'>"

print """<div class="container" id="content">"""

print """<center><iframe class=infovis src='../../../../graphs/p2p_graph.html' frameborder='0' scrolling='no'></iframe></center>""" 

print "</div>"

print "</div>"

######################### content  #########################

print "</body>"

print "</html>"
