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
from ViewModel import ViewModel
from UserModel import UserModel

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

vid = form.getvalue("vid")

vid = str(vid).strip("(),L")

vid = int(vid)

now = datetime.datetime.now()#generate the TimeStamp

tmstp = now.minute#converting the TimeStamp to string   

SessionModel = SessionModel()

ViewModel = ViewModel()

UserModel = UserModel()

if SessionModel.connect() and UserModel.connect() and ViewModel.connect():

	timestamp = SessionModel.Validate(uid, sid, remote)

	if((timestamp+5)<=tmstp or timestamp == -1):

	    SessionModel.Close(uid, remote)

	    del ViewModel

	    del UserModel

	    del SessionModel

	    print """<script language=\"JavaScript\">{location.href=\"../index.cgi\";self.focus();}</script>"""

	SessionModel.UpdateTimeStamp(tmstp, uid, remote)

	ViewModel.Remove(vid)

	del ViewModel

	del UserModel

	del SessionModel

	print """<script language=\"JavaScript\">{location.href=\"../Views/AdminViews/Dashboard.cgi?uid=%s&sid=%s&remote=%s\";self.focus();}</script>"""%(uid, sid, remote)

else:

	del ViewModel

	del UserModel

	del SessionModel

	print "Database Connection Error. Configuration File Not Found."