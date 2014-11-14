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
from SessionModel import SessionModel
from NetworkModel import NetworkModel
from UserModel import UserModel

cgitb.enable()

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

nid = form.getvalue("nid")

nid = str(nid).strip("(),L")

nid = int(nid)

now = datetime.datetime.now()#generate the TimeStamp

tmstp = now.minute#converting the TimeStamp to string   

SessionModel = SessionModel()

NetworkModel = NetworkModel()

UserModel = UserModel()

if SessionModel.connect() and UserModel.connect() and NetworkModel.connect():

	timestamp = SessionModel.Validate(uid, sid, remote)

	if((timestamp+5)<=tmstp or timestamp == -1):

	    SessionModel.Close(uid, remote)

	    del NetworkModel

	    del UserModel

	    del SessionModel

	    print """<script language=\"JavaScript\">{location.href=\"../index.cgi\";self.focus();}</script>"""

	SessionModel.UpdateTimeStamp(tmstp, uid, remote)

	NetworkModel.Remove(nid)

	del NetworkModel

	del UserModel

	del SessionModel

	print """<script language=\"JavaScript\">{location.href=\"../Views/AdminViews/Dashboard.cgi?uid=%s&sid=%s&remote=%s\";self.focus();}</script>"""%(uid, sid, remote)

else:

	print "Database Connection Error. Configuration File Not Found."

	del NetworkModel

	del UserModel

	del SessionModel