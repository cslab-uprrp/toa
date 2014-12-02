#!/usr/bin/python

########### Imports #######################

import cgi
import re
import sys 
import os
import cgitb
import datetime
import urllib, hashlib
import sys
sys.path.append("../Models")
from SessionModel import SessionModel
from PortModel import PortModel
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

fullName = form.getvalue("Name")

email = form.getvalue("Email")

staff = form.getvalue("Staff")

phone = form.getvalue("Phone")

passwd = form.getvalue("Password")

cpasswd = form.getvalue("CPassword")

pastInfo = {"name":fullName, "email":email, "phone":phone}

now = datetime.datetime.now()#generate the TimeStamp

tmstp = now.minute#converting the TimeStamp to string   

SessionModel = SessionModel()

UserModel = UserModel()

if SessionModel.connect() and UserModel.connect():

	timestamp = SessionModel.Validate(uid, sid, remote)

	if((timestamp+5)<=tmstp or timestamp == -1):

	    SessionModel.Close(uid, remote)

	    del UserModel

	    del SessionModel

	    print """<script language=\"JavaScript\">{location.href=\"../index.cgi\";self.focus();}</script>"""

	SessionModel.UpdateTimeStamp(tmstp, uid, remote)

	errors = []

	fail = False

	if not re.match("^[A-Z][a-z]*(\s[A-Z][a-z])*$", str(fullName)):
	
		errors.append("Incorrect name format.")

		fail = True

        if not re.match("^([0-9]*)$", str(phone)):

		errors.append("Incorrect phone number format")

                fail = True

        if not re.match("^[0-1]$", str(staff)):

		errors.append("Please do not modify the configuration")

                fail = True

        if not re.match("([a-zA-Z0-9]|\.|_|-|\+|$)+@[a-zA-Z0-9]+(\.[a-zA-Z]+)+$", str(email)):

		errors.append("Invalid email")

                fail = True

        if not re.match(".(?=.{8,})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#\$%@&\?\*]).*$", str(passwd)) and not re.match(".(?=.{8,})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#\$%@&\?\* ]).*$", str(cpasswd)):

		errors.append("Incorrect password format")

                fail = True

        if not str(passwd) == str(cpasswd):

		errors.append("Password must match confirmation")

                fail = True

	if not fail:

		UserModel.Create(fullName, phone, passwd, email, staff)

		errors.append("Account Added.")

		print """<script language=\"JavaScript\">{location.href=\"../Views/AdminViews/AddAccount.cgi?uid=%s&sid=%s&remote=%s&errors=%s\";self.focus();}</script>"""%(uid, sid, remote, errors)
		

	print """<script language=\"JavaScript\">{location.href=\"../Views/AdminViews/AddAccount.cgi?uid=%s&sid=%s&remote=%s&errors=%s&pastInfo=%s\";self.focus();}</script>"""%(uid, sid, remote, errors, pastInfo)

else:

    print "Database Connection Error. Configuration File Not Found."


del UserModel

del SessionModel

print """<script language=\"JavaScript\">{location.href=\"../Views/AdminViews/AddAccount.cgi?uid=%s&sid=%s&remote=%s\";self.focus();}</script>"""%(uid, sid, remote)
