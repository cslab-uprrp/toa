#!/usr/bin/python

########### Imports #######################

import cgi
import sys 
import os
import re
import cgitb
import datetime
import urllib, hashlib
import sys
sys.path.append("../Models")
from SessionModel import SessionModel
from ViewModel import ViewModel
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

view_name = str(form.getvalue("view_name"))

view_description = str(form.getvalue("view_description"))

now = datetime.datetime.now()#generate the TimeStamp

tmstp = now.minute#converting the TimeStamp to string 

validator = [re.compile('[a-zA-Z0-9]+[a-zA-Z0-9\_\-]*$'), re.compile('[a-zA-Z0-9\s\t\n\.]*$')]  

SessionModel = SessionModel()

ViewModel = ViewModel()

UserModel = UserModel()

if SessionModel.connect() and ViewModel.connect() and UserModel.connect():

	timestamp = SessionModel.Validate(uid, sid, remote)

	if((timestamp+5)<=tmstp or timestamp == -1):

	    SessionModel.Close(uid, remote)

	    del ViewModel

	    del UserModel

	    del SessionModel

	    print """<script language=\"JavaScript\">{location.href=\"../index.cgi\";self.focus();}</script>"""

	SessionModel.UpdateTimeStamp(tmstp, uid, remote)

	errors = []

	if validator[0].match(view_name) and validator[1].match(view_description):

		if ViewModel.Add(view_name, view_description, uid):

			errors.append('View Added')

	else:

		if not validator[0].match(view_name):

			errors.append('View name must contain only letters, _, - or numbers.')

		if not validator[1].match(view_description):

			errors.append('Invalid view description.')

	del ViewModel

	del UserModel

	del SessionModel

	print """<script language=\"JavaScript\">{location.href=\"../Views/AdminViews/AddView.cgi?uid=%s&sid=%s&remote=%s&errors=%s\";self.focus();}</script>"""%(uid, sid, remote, str(errors))


else:

	print "Database Connection Error. Configuration File Not Found."

	del ViewModel

	del UserModel

	del SessionModel