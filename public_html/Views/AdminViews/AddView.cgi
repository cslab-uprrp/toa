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
from PortModel import PortModel
from Net2NetModel import Net2NetModel
from ViewModel import ViewModel
from UserModel import UserModel
from GraphModel import GraphModel
sys.path.append("../../Controllers")
from FormController import *

cgitb.enable()

########## Imports #######################

############### Init #######################

print "Content-Type: text/html"

print 

form = cgi.FieldStorage()#getting the values of the form in case of a validation error

uid = form.getvalue("uid")

uid = str(uid).strip("(),L")

#uid = int(uid)

sid = form.getvalue("sid")

remote = form.getvalue("remote")

if form.has_key("errors"):

    errors = form.getvalue("errors")

else:

    errors = '[]'

now = datetime.datetime.now()#generate the TimeStamp

tmstp = now.minute#converting the TimeStamp to string   

SessionModel = SessionModel()

UserModel = UserModel()

NetworkModel = NetworkModel()

PortModel = PortModel()

Net2NetModel = Net2NetModel()

ViewModel = ViewModel()

GraphModel = GraphModel()

if SessionModel.connect() and UserModel.connect() and Net2NetModel.connect() and ViewModel.connect() and PortModel.connect() and NetworkModel.connect() and GraphModel.connect():

    timestamp = SessionModel.Validate(uid, sid, remote)

    ##################### Init ##########################################

    if((timestamp+5)<=tmstp or timestamp == -1):

        SessionModel.Close(uid, remote)

        del UserModel

        del SessionModel

        del NetworkModel

        del PortModel

        del GraphModel

        del Net2NetModel

        del ViewModel

        print """<script language=\"JavaScript\">{location.href=\"../../index.cgi\";self.focus();}</script>"""

    SessionModel.UpdateTimeStamp(tmstp, uid, remote)

    print "<!DOCTYPE html><html>"

    print "<head>"

    print "<title>ToaNMS</title>"

    print """<link rel="stylesheet" href="../../Style/bootstrap/css/style.css"/>"""

    print """<link rel="stylesheet" href="../../Style/bootstrap/css/datepicker.css"/>"""

    print """<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>"""

    print "<script src='http://www.google.com/jsapi'></script>"

    print """<script src="../../Style/bootstrap/js/bootstrap.min.js"></script>"""

    print """<script src="../../Style/bootstrap/js/helpers.js"></script>"""

    print """<script src='http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.9/jquery-ui.js' type='text/javascript'></script>"""

    print """<script type='text/javascript' src='../../Style/bootstrap/js/jquery.ui.datetimepicker.min.js'></script>"""

    print """<script src="../../Controllers/GraphController.js"></script>"""

    print """<script src="../../Controllers/MenuController.js"></script>"""

    print """<script src="../../Controllers/PluginController.js"></script>"""

    print """<script src="../../Controllers/Top100Controller.js"></script>"""

    print "<script type='text/javascript'>google.load('visualization', '1', {packages: ['corechart']});</script>"

    print "<script>var elem = document.getElementsByClassName('popover');for(i=0; i<elem.length;i++){elem[i].popover();}</script>"

    print "</head>"

    ######################### headers #########################

    SessionModel.UpdateTimeStamp(tmstp, uid, remote)

    print "<body>"

    ######################### banner  #########################

    print "<div class='row'>"

    print "<div class='col-md-9'>"
            
    print """<h1 class='brand'>Toa Network Monitoring System</h1>"""

    print "</div>"

    print "<div class='col-md-3'>"
        
    print "<div class='row'>"

    print "<div class='col-md-12 box-user'>"

    print "<div class='btn-group'>"

    print "<button class='btn btn-default btn-lg btn-box last' data-toggle='dropdown'>"

    print UserModel.Email(uid)[0]

    print "<span class='caret'></span>"

    print "</button>"

    print "<ul class='dropdown-menu pull-right' role='menu'>"
      
    print "<li><a tabindex='-1' href='#'>Reset Password</a></li>"

    print "<li><a tabindex='-1' href='#'>Add Account</a></li>"

    print "<li><a tabindex='-1' href='../../Controllers/Logout.cgi?uid=%s&sid=%s&remote=%s'>Logout</a></li>"%(uid, sid, remote)

    print "</ul>"

    print "</div>"

    print "</div>"

    print "</div>"

    print "</div>"

    print "</div>"

    ######################### banner  #########################

    ######################### viewer  #########################

    print "<div class='modal fade' id='Viewer'>"
            
    print "<div class='modal-dialog viewer'>"

    #print "<div class='modal-header viewer-header'>"
        
    #print "<h1 class='modal-title'></h1>"
      
    #print "</div>"
                
    print "<div class='modal-content viewer-body'>"
      
    print "<div class='modal-body modal-no-padding' >"

    print "<div class='container-fluid'>"

    #print "<button type='button' class='close viewer-expand' aria-hidden='true'><i class='glyphicon glyphicon-chevron-down'></i></button>"

    print "<button onclick='CleanViewer();' type='button' class='close viewer-close' data-dismiss='modal' aria-hidden='true'><i class='glyphicon glyphicon-remove'></i></button>"

    print "<div class='row' id='viewer-body'>"

    print "</div></div>"

    print "</div>"
    
    print "</div>"
    
    print "</div>"

    print "</div>"

    ######################### add view form  #########################

    ######################### custom query form  #########################

    print "<div class='modal fade' id='CustomQuery'>"
            
    print "<div class='modal-dialog'>"
                
    print "<div class='modal-content'>"
                
    print "<div class='modal-header'>"
        
    print "<button type='button' class='close' data-dismiss='modal' aria-hidden='true'>&times;</button>"
        
    print "<h4 class='modal-title'>Custom Graph Query</h4>"
      
    print "</div>"
      
    print "<div class='modal-body'>"

    print "<div class='row'>"

    print "<div class='col-md-5'>"

    print "<select name='network' class='form-control' id='network' onchange='GetSecondSystemMenu(this[this.selectedIndex].value, 1), ClearThirdSystemMenu()'>"

    devices = NetworkModel.GetAll()

    print "<option value='None'>Select Device</option>"

    for device in devices:

        print "<option value='%s'>%s</option>"%(device[0], device[1])

    print "</select>"

    print "</div></div><br><div class='row'>"

    print "<div class='col-md-10 col-md-offset-1'><div id='custom-query-second'>"

    print "</div></div></div>"

    print "<div class='row'><div class='col-md-10 col-md-offset-1'><div id='custom-query-third'>"

    print "</div></div></div>"

    print "<div id='custom-query-time'>"

    print "</div>"

    print "<div class='row'>"

    print "<div class='col-md-8 col-md-offset-1'><p class='text-danger' id='custom-query-status'></p></div>"

    print "<div class='col-md-2'><button class='btn btn-lg btn-feature-bar' onclick=\"CustomGraphView(%s, '%s', '%s')\">Query</button></div>"%(uid, sid, remote)

    print "</div>"

    print "</div>"
    
    print "</div>"
    
    print "</div>"

    print "</div>"

    ######################### custom query form  #########################

    ######################### Add Graph to View ##########################

    print "<div class='modal fade' id='AddGraphModal'>"

    print "<div class='modal-dialog'>"

    print "<div class='modal-content'>"

    print "<div class='modal-header'>"

    print "<button type='button' class='close' data-dismiss='modal' aria-hidden='true'>&times;</button>"

    print "<h4 class='modal-title'>Add Graph to a View</h4>"

    print "</div>"

    print "<div class='modal-body'>"

    views = ViewModel.GetAll(uid)

    print "<div class='row'>"

    print "<div class='col-md-7 col-md-offset-1'>"

    print "<select class='form-control form-control-lg' id='views'>"

    for v in views:

        print "<option value='%s'>%s</option>"%(v[0], v[1])

    print "</select>"

    print "</div><div class='col-md-3'>"

    print "<button type='button' class='btn btn-default btn-lg btn-feature-bar pull-right' id='GraphAdder'>Add</button><br><br>"

    print "</div></div>"

    print "</div>"

    print "</div>"

    print "</div>"

    print "</div>"

    ######################### Add Graph to View ##########################


    ######################### feature bar #########################

    print "<div class='row feature-bar'>"

    print "<div class='col-md-11 col-md-offset-1'>"

    print "<div class='btn-group feature-bar-group'>"

    print "<a class='btn btn-default btn-lg btn-feature-bar' href='Dashboard.cgi?uid=%s&sid=%s&remote=%s'>Dashboard</a>"%(uid, sid, remote)

    print "<div class='btn-group'>"

    print """<a href='#DeviceMenu' data-toggle='dropdown' class='btn btn-default btn-lg btn-feature-bar'>Device</a>"""        

    print "<ul class='dropdown-menu' role='menu'>"

    devices = NetworkModel.GetAll()

    for device in devices:

	print "<li class='dropdown-submenu'><a href=#Device class='dropdown-hover'>%s</a><ul class='dropdown-menu'><li><a href='#' onclick=\"GraphView('%s', 'all', 'day', 'device', 'default', 'default', 'default', 'default', 1, 'default', '%s', '%s', '%s')\">Interface Graph</a></li>"%(device[1], device[1], uid, sid, remote)

        ports = PortModel.Get(device[0])

        if(len(ports) > 0):

            print "<li class='dropdown-submenu'><a href=#Port class='dropdown-hover'>Port Graph</a><ul class='dropdown-menu'>"

            for port in ports:
		
		print "<li><a href=# onclick=\"GraphView('%s', 'all', 'day', 'port', '%s', 'default', 'default', 'default', 1, 'default', '%s', '%s', '%s')\">%s</a></li>"%(device[1], port[1], uid, sid, remote, port[1])

            print "</ul></li>"

        net2nets = Net2NetModel.Get(device[0])

        if(len(net2nets) > 0):

            print "<li class='dropdown-submenu'><a href=#Net2Net class='dropdown-hover'>Net2Net Graph</a><ul class='dropdown-menu'>"

            for net2net in net2nets:

		print "<li><a href=# onclick=\"GraphView('%s', 'all', 'day', 'net2net', 'default', '%s', 'default', 'default', 1, 'default', '%s', '%s', '%s')\">%s</a>"%(device[1],net2net[1], uid, sid, remote, net2net[1])

            print "</ul></li>"
        
	print "<li class='dropdown-submenu'><a href=#Top100 class='dropdown-hover'>Top100</a>"

        print "<ul class='dropdown-menu' role='menu'>"

	#### Net Top 1000

	print "<li class='dropdown-submenu'><a class='dropdown-hover'>Network</a>"

        print "<ul class='dropdown-menu' role='menu'>"

        print "<li><a onclick=\"GetTop100('net', 'oct', '%s', '%s', '%s', '%s')\">Octects</a></li>"%(device[0], uid, sid, remote)

        print "<li><a onclick=\"GetTop100('net', 'pak', '%s', '%s', '%s', '%s')\">Packets</a></li>"%(device[0], uid, sid, remote)

        print "<li><a onclick=\"GetTop100('net', 'flow', '%s', '%s', '%s', '%s')\">Flows</a></li>"%(device[0], uid, sid, remote)

        print "</li></ul>"

	 ### Port Top 100


        print "<li class='dropdown-submenu'><a class='dropdown-hover'>Port</a>"

        print "<ul class='dropdown-menu' role='menu'>"

        print "<li><a onclick=\"GetTop100('ports', 'oct', '%s','%s','%s','%s')\">Octects</a></li>"%(device[0],uid,sid,remote)

        print "<li><a onclick=\"GetTop100('ports', 'pak', '%s','%s','%s','%s')\">Packets</a></li>"%(device[0],uid,sid,remote)

        print "<li><a onclick=\"GetTop100('ports', 'flow', '%s','%s','%s','%s')\">Flows</a></li>"%(device[0],uid,sid,remote)

        print "</ul></li>"

        print "</ul>"

        print "</li></ul>"

    print "</div>"

    print "<a class='btn btn-default btn-lg btn-feature-bar' href='#' data-toggle='modal' data-target='#CustomQuery'>Custom Query System</a>"

    print "<div class='btn-group'>"

    print "<a class='btn btn-default btn-lg btn-feature-bar last' data-toggle='dropdown'>Viewer</a>"

    print "<ul class='dropdown-menu' role='menu'>"

    views = ViewModel.GetAll(uid)

    for view in views:

 	print "<li><a href=# onclick=\"GraphView('default', 'all', 'day', 'views', 'default', 'default', screen.width/2, screen.height-(screen.height/2), 1, %s)\" data-toggle='modal' data-target='#Viewer'>%s</a></li>"%(view[0], view[1])

    print "</ul></div>"

    print "</div></div>"

    print "</div>"

    ######################### feature bar #########################

    ######################### content  #########################

    print "<div class='container-fluid' id='content'>"

    print "<div class='row'>"

    print "<div class='col-md-12 add-view-form'>"

    graphs = GraphModel.GetAll() 

    AddViewForm(uid, sid, remote, errors)

    print "</div>"

else:

    print "Database Connection Error. Configuration File Not Found."

del UserModel

del SessionModel

del NetworkModel

del PortModel

del GraphModel

del Net2NetModel

del ViewModel
