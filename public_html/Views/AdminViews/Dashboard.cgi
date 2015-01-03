#!/usr/bin/python

########### Imports #######################

import cgi
import sys 
import os
import cgitb
import time
import urllib, hashlib
import sys
sys.path.append("../../Models")
from SessionModel import SessionModel
from NetworkModel import NetworkModel
from PortModel import PortModel
from Net2NetModel import Net2NetModel
from ViewModel import ViewModel
from UserModel import UserModel

cgitb.enable()

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

now = time.time()#generate the TimeStamp

SessionModel = SessionModel()

UserModel = UserModel()

NetworkModel = NetworkModel()

PortModel = PortModel()

Net2NetModel = Net2NetModel()

ViewModel = ViewModel()

def printpage():

	
    SessionModel.UpdateTimeStamp(now, uid, remote)
    #################### Validation ####################################

    ######################### headers  #########################

    print "<!DOCTYPE html><html>"

    print "<head>"

    print "<title>ToaNMS</title>"

    print """<link rel="stylesheet" href="../../Style/bootstrap/css/style.css"/>"""

    print """<link rel="stylesheet" href="../../Style/bootstrap/css/datepicker.css"/>"""

    print """<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>"""

    print "<script src='http://www.google.com/jsapi'></script>"

    print """<script src="../../Style/bootstrap/js/bootstrap.min.js"></script>"""

    print """<script src='http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.9/jquery-ui.js' type='text/javascript'></script>"""

    print """<script type='text/javascript' src='../../Style/bootstrap/js/jquery.ui.datetimepicker.min.js'></script>"""

    print """<script src="../../Controllers/PluginController.js"></script>"""

    print """<script src="../../Controllers/GraphController.js"></script>"""

    print """<script src="../../Controllers/MenuController.js"></script>"""

    print """<script src="../../Controllers/Top100Controller.js"></script>"""

    print "<script type='text/javascript'>google.load('visualization', '1', {packages: ['corechart']});</script>"

    print "<script>var elem = document.getElementsByClassName('popover');for(i=0; i<elem.length;i++){elem[i].popover();}</script>"

    print "</head>"

    ######################### headers #########################


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

    print "<li><a tabindex='-1' href='Account.cgi?uid=%s&sid=%s&remote=%s'>Add Account</a></li>" %(uid, sid, remote) 

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

    ######################### viewer  #################################

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

        print "</ul></li>"

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

    print "<div class='col-md-4 col-md-offset-1 device-col'>"

    labels = NetworkModel.GetLabels()

    count = NetworkModel.GetNumberOfLabels()

    print "<h2 class='device-col-header page-header'>Device List <a class='pull-right device-col-button' href='AddNetwork.cgi?uid=%s&sid=%s&remote=%s'><i class='glyphicon glyphicon-plus'></i></a></h2>"%(uid,sid,remote)

    i = 0# initialize the loop counter to 0

    while(i<count):#while the loop counter is less than the number of labels....do this

        ids = NetworkModel.GetIdByLabel(labels[i][0])

        print "<div class='thumbnail'>"

        print "<h3 class='device-col-entry'>%s"%(labels[i][0])

        print "<a class='pull-right text-danger device-col-remove-button' href='../../Controllers/RemoveNetwork.cgi?uid=%s&sid=%s&remote=%s&nid=%s'><i class='glyphicon glyphicon-trash'></i></a>"""%(uid, sid, remote, ids)

        print "<a class='pull-right text-warning device-col-edit-button' href='EditNetwork.cgi?uid=%s&sid=%s&remote=%s&nid=%s'><i class='glyphicon glyphicon-pencil'></i></a></h3><p><br></p></div>"%(uid, sid, remote, ids)
        
        i += 1 # increment the loop counter

    print "</div>"

    print "<div class='col-md-4 col-md-offset-1 view-col'>"

    print "<h2 class='view-col-header page-header'>View List <a class='pull-right view-col-button' href='AddView.cgi?uid=%s&sid=%s&remote=%s'><i class='glyphicon glyphicon-plus'></i></a></h2>"%(uid, sid, remote)

    views = ViewModel.GetAll(uid)

    if views:

        for v in views:

            print "<div class='thumbnail'>"

            print "<h3 class='view-col-entry'>%s "%(v[1])

            print "<a class='pull-right text-danger view-col-remove-button' href='../../Controllers/RemoveView.cgi?uid=%s&sid=%s&remote=%s&vid=%s'><i class='glyphicon glyphicon-trash'></i></a></h3>"%(uid, sid, remote, v[0])

            print "<p class='view-col-entry'>%s</p>"%v[2]

            #print "<a class='pull-right text-warning view-col-edit-button' href='EditView.cgi?uid=%s&sid=%s&remote=%s&vid=%s'><i class='glyphicon glyphicon-pencil'></i></a></h3>"%(uid, sid, remote, v[0])

            print "</div>"

    print "</div>"

    print "</div>"

    print "</div>"

    print "</div>"

    ######################### content  #########################

    ######################### Fatality #########################
    print "</body>"

    print "</html>"

################ main #####################

if SessionModel.connect() and UserModel.connect() and Net2NetModel.connect() and ViewModel.connect() and PortModel.connect() and NetworkModel.connect():

    timestamp = SessionModel.Validate(uid, sid, remote, now)

    ##################### Init ##########################################

    #################### Validation ####################################

    if not timestamp:

        SessionModel.Close(uid, remote)

        del UserModel

        del SessionModel

        del NetworkModel

        del PortModel

        del Net2NetModel

        del ViewModel
    
	print "<!DOCTYPE html><html>"

    	print "<head>"

        print """<script language=\"JavaScript\">{location.href=\"../../index.cgi\";self.focus();}</script>"""
	print """</head></html>"""

    else:
	printpage()	

	del UserModel

	del SessionModel

	del NetworkModel

	del PortModel

	del Net2NetModel

	del ViewModel


else:

    print "Database Connection Error. Configuration File Not Found."

    print SessionModel.connect() and UserModel.connect() and Net2NetModel.connect() and ViewModel.connect() #and PortModel.connect() and NetworkModel.connect()

    del UserModel

    del SessionModel

    del NetworkModel

    del PortModel

    del Net2NetModel

    del ViewModel


######################### Fatality #########################
