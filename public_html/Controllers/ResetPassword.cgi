#!/usr/bin/python

########### Imports #######################

import cgi
import sys 
import os
import re
import cgitb
import time
import urllib, hashlib
import sys
sys.path.append("../Models")
from SessionModel import SessionModel
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

now = time.time()#generate the TimeStamp

password = form.getvalue("password")

cpassword = form.getvalue("cpassword")

validator = re.compile('.(?=.{8,})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#\$%@&\?\* "]).*$') 

SessionModel = SessionModel()

UserModel = UserModel()

if SessionModel.connect() and UserModel.connect():

	timestamp = SessionModel.Validate(uid, sid, remote, now)

	if not timestamp:

	    SessionModel.Close(uid, remote)

	    del UserModel

	    del SessionModel

	    print """<script language=\"JavaScript\">{location.href=\"../index.cgi\";self.focus();}</script>"""

	SessionModel.UpdateTimeStamp(now, uid, remote)

	errors = []

	if validator.match(password) and validator.match(cpassword):

		if UserModel.ChangePassword(password, uid):

			errors.append('Password Changed')

	else:

		if not validator.match(password) or validator.match(cpassword):

			errors.append('Password must contain at least 8 characters, one number, one letter and one unique character')

		if not password == cpassword:

			errors.append('Password and Confirmation Password must match')

	del UserModel

	del SessionModel

	print """<script language=\"JavaScript\">{location.href=\"../Views/AdminViews/ResetPassword.cgi?uid=%s&sid=%s&remote=%s&errors=%s\";self.focus();}</script>"""%(uid, sid, remote, str(errors))


else:

	print "Database Connection Error. Configuration File Not Found."

	del UserModel

	del SessionModel
