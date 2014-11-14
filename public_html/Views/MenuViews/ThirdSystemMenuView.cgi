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

state = form.getvalue("state")

PortModel = PortModel()

NetworkModel = NetworkModel()

if PortModel.connect() and NetworkModel.connect():

	html = "<br><div class='row'>"

	if(id != 'None'):

		if(state == '1'):

			ports = PortModel.Get(id)

			for p in ports:

				html += "<div class='col-md-2'><label class='checkbox-inline'><input name='checkboxoptions' type='checkbox' value='%s'>%s</label></div>"%(p[0], p[1])

		else:

			net2net = NetworkModel.GetNetwork2(id)

			for n in net2net:

				html += "<div class='col-md-2'><label class='checkbox-inline'><input name='checkboxoptions' type='checkbox' value='%s'>%s</label></div>"%(n[0], n[1])

	else:

		html += ""

	print html+"</div>"

else:

    print "Database Connection Error. Configuration File Not Found."

    print SessionModel.connect() and UserModel.connect() and Net2NetModel.connect() and ViewModel.connect() #and PortModel.connect() and NetworkModel.connect()

del PortModel

del NetworkModel