#!/usr/bin/python

import cgi
import os
import sys
import MySQLdb
import cgitb
from datetime import datetime
sys.path.append('../../Models')
from NetworkModel import NetworkModel
from PortModel import PortModel

cgitb.enable()

print "Content-Type: text/html\n\n"
print 

form = cgi.FieldStorage()

id = form.getvalue("id")

PortModel = PortModel()

NetworkModel = NetworkModel()

form = cgi.FieldStorage()

if PortModel.connect() and NetworkModel.connect():

	if(form.has_key("Admin")):

		if(id != 'None'):

			ports = PortModel.Get(id)

			net2net = NetworkModel.GetNetwork2(id)

			html = "<label class='radio'><input name='ftype' id='ftype' type='radio' value='i/o' onclick='ClearThirdSystemMenu();GetTimeSystemMenu(1);' name='selection'> I/O: The general amount of traffic in this network</label>"

			if(len(ports)>0):

				html += "<label class='radio'><input name='ftype' id='ftype' type='radio' value='port' onclick='GetThirdSystemMenu(%s, 1, 1);GetTimeSystemMenu(1);' name='selection'> Port: The traffic of a specific port</label>"%id

			if(len(net2net)>0):

				html += "<label class='radio'><input name='ftype' id='ftype' type='radio' value='p2p' onclick='GetThirdSystemMenu(%s, 2, 1);GetTimeSystemMenu(1);' name='selection'> P2P: Traffic from one point in the network to another</label>"%id

			print html

		else:

			print ""

else:

    print "Database Connection Error. Configuration File Not Found."

del PortModel

del NetworkModel