#!/usr/bin/python

import cgi
import sys 
import os
import MySQLdb
import cgitb
from datetime import datetime
sys.path.append('../../Models')
from NetworkModel import NetworkModel

print "Content-Type: text/html\n\n"

print 

form = cgi.FieldStorage()

NetworkModel = NetworkModel()

Networks = NetworkModel.GetAll()

if(form.has_key("Admin")):

	html = ""

	count = 0

	for Net in Networks:

		html += "<a href=#><div class=device id=%s onclick='GetPortNetSystemMenu(%s, %s, 1)'><br>%s</div></a>"%(Net[0], Net[0], count, Net[1])

		count += 1

else:

	html = ""

	count = 0

	for Net in Networks:

		html += "<a href=#><div class=device id=%s onclick='GetPortNetSystemMenu(%s, %s)'><br>%s</div></a>"%(Net[0], Net[0], count, Net[1])

		count += 1

print html