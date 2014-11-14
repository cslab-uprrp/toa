#!/usr/bin/python

########### Imports #######################

import cgi
import sys 
import os
import cgitb
import datetime
import urllib, hashlib
import sys
sys.path.append("../Models")
from GraphModel import GraphModel

cgitb.enable()

########## Imports #######################

############### Init #######################

print "Content-Type: text/html\n\n"

print 

form = cgi.FieldStorage()#getting the values of the form in case of a validation error

vid = form.getvalue("vid")

graph_name = str(form.getvalue("graph_name"))

GraphModel = GraphModel()

if GraphModel.connect():

	status = GraphModel.Add(graph_name, vid)

	if status:

		print "Graph Added to View Successfully."

	else:

		print "Unable to Add Graph to View."

	del GraphModel

else:

	print "Database Connection"

	del GraphModel