#!/usr/bin/python

######################### imports  #########################

import cgi
import sys 
import os
import cgitb
cgitb.enable()
import datetime
import urllib, hashlib
import sys
sys.path.append("Models")
from NetworkModel import NetworkModel
from PortModel import PortModel
from Net2NetModel import Net2NetModel
from Config import Config

config=Config()
PATH=config.getGraphsPath() 
#PATH="graphs/"
######################### imports  #########################

######################### headers  #########################

print "Content-Type: text/html"     

print 

print "<!DOCTYPE html><html>"

print "<head>"

print "<title>ToaNMS</title>"

print "<link rel='stylesheet' href='Style/bootstrap/css/style.css'/>"

print "<link type='text/css' href='./Jit/Examples/css/base.css' rel='stylesheet' />"
        
print "<link type='text/css' href='./Jit/Examples/css/Sunburst.css' rel='stylesheet' />"
         
print "<script language='javascript' type='text/javascript'src='./Jit/jit.js'></script>"

print """<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>"""

print "<script src='http://www.google.com/jsapi'></script>"

print """<script src="Style/bootstrap/js/bootstrap.min.js"></script>"""

print "<script type='text/javascript' src='http://platform.twitter.com/widgets.js'></script>"

print """<script src="Controllers/GraphController.js"></script>"""

print """<script src="Controllers/Top100Controller.js"></script>"""

print """<script src='Style/bootstrap/js/helpers.js'></script>"""

print "<script type='text/javascript'>google.load('visualization', '1', {packages: ['corechart']});</script>"

print "<script>var elem = document.getElementsByClassName('popover');for(i=0; i<elem.length;i++){elem[i].popover();}</script>"

print "</head>"

######################### headers #########################

print "<body onload='P2PGraph()'>"

######################### banner  #########################

print "<div class='container-fluid'>"

print "<div class='row'>"

print "<div class='col-md-9'>"

print "<h1 class='brand'>Toa Network Monitoring System</h1>"

print "</div>"

print "<div class='col-md-2 col-md-offset-1'>"

print "</div>"

print "</div>"

print "</div>"

######################### banner  #########################

######################### feature bar #####################

print "<div class='row feature-bar'>"

print "<div class='col-md-11 col-md-offset-1'>"

NetworkModel = NetworkModel()

PortModel = PortModel()

Net2NetModel = Net2NetModel()

if not NetworkModel.connect() or not Net2NetModel.connect() or not PortModel.connect():

	print "<div class='btn-group feature-bar-group'>"

	print "<a href='index.cgi' class='btn btn-default btn-lg btn-info btn-feature-bar'>Home</a>"

	print "<a href='#DeviceMenu' data-toggle='modal' class='btn btn-default btn-lg btn-info btn-feature-bar'>Device</a>"

	print "<div class='modal' id='DeviceMenu'>"

	print "<div class='modal-header'><h3>Database System Connection Error.</h3></div>"

	print "</div>"

else:

	print "<div class='btn-group feature-bar-group'>"

	print "<a href='index.cgi' class='btn btn-default btn-lg btn-feature-bar'>Home</a>"

	print "<div class='btn-group'>"

	print "<a href='#DeviceMenu' data-toggle='dropdown' class='btn btn-default btn-lg btn-feature-bar last'>Device</a>"

	print "<ul class='dropdown-menu' role='menu'>"

	devices = NetworkModel.GetAll()

	for device in devices:

		print "<li class='dropdown-submenu'><a href=#Device class='dropdown-hover'>%s</a><ul class='dropdown-menu'><li><a href='#' onclick=\"GraphView('%s', 'all', 'day', 'device', 'default', 'default', 'default', 'default')\">Interface Graph</a></li>"%(device[1], device[1])

		ports = PortModel.Get(device[0])

		if(len(ports) > 0):

			print "<li class='dropdown-submenu'><a href=#Port class='dropdown-hover'>Port Graph</a><ul class='dropdown-menu'>"

			for port in ports:

				print "<li><a href=# onclick=\"GraphView('%s', 'all', 'day', 'port', '%s', 'default', 'default', 'default')\">%s</a></li>"%(device[1], port[1], port[1])

			print "</ul></li>"

		net2nets = Net2NetModel.Get(device[0])

		if(len(net2nets) > 0):

			print "<li class='dropdown-submenu'><a href=#Net2Net class='dropdown-hover'>Net2Net Graph</a><ul class='dropdown-menu'>"

			for net2net in net2nets:

				print "<li><a href=# onclick=\"GraphView('%s', 'all', 'day', 'net2net', 'default', '%s', 'default', 'default')\">%s</a>"%(device[1],net2net[1], net2net[1])

			print "</ul></li>"

		print "</li></ul>"

	del NetworkModel

	del PortModel

	del Net2NetModel

	print "</div>"

	print "</div>"

print "</div>"

print "</div>"

######################### feature bar #####################

######################### content  #########################

print "<div class='container-fluid' id='content'>"

print "<div class='row'>"

print "<div class='col-md-7'>"

print "<div class='jumbotron p2p-jumbotron'>"

if os.path.isfile(PATH + "/p2p_graph.js"):

	print "<div id='container'>"
				
	print "<div id='center-container'>"
   		 		
	print "<div id='infovis'></div>"  

	print "</div>"

	#print "<div id='right-container'>"

	#print "<div id='inner-details'></div>"
		
	#print "</div>"

else:
	print "<div id='container'>"
	print "<div>"
				
        
        print "<br><center><h1><p class='text-danger'>You dont see the p2p graph? <br><br>Try refreshing the page.</p></h1></center>"
	
	print "</div>" 

print "</div>"

print "</div>"

print "</div>"

print "<div class='col-md-5'>"

print "<div class='jumbotron login-jumbotron'>"

print "<center><br><form action='Controllers/AuthenticationController.cgi' method='post' class='form-horizontal'>"

print "<div class='input-group input-group-lg'>"

print "<span class='input-group-addon'><i class='glyphicon glyphicon-envelope'></i></span>"

print "<input class='form-control' type='text' name='username' placeholder='Username'>"""

print "</div><br><br>"

print "<div class='input-group input-group-lg'>"

print "<span class='input-group-addon'><i class='glyphicon glyphicon-lock'></i></span>"

print "<input class='form-control' type='password' name='password' placeholder='Password'>"

print "</div>"

form = cgi.FieldStorage()

if form.has_key("validation"):

	print "<p class='text-danger pull-left error-msg'>Invalid email or password. Try again</p>"

print "<input class='btn btn-default btn-lg pull-right btn-login' type='submit' value='Login'>"

print "</form></div>"

print "</div>"

print "</div>"

######################### content  #########################

print "</body></html>"
