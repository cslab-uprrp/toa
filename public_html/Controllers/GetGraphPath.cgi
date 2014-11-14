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

gid = form.getvalue("gid")

GraphModel = GraphModel()

print GraphModel.Get('graph_path', 'gid', gid)

del GraphModel