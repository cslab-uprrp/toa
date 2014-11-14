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

nid = form.getvalue("nid")

nid = str(nid).strip("(),L")

nid = int(nid)

sid = form.getvalue("sid")

remote = form.getvalue("remote")

label = form.getvalue("Label")

monitoringType = form.getvalue("Type")

if form.has_key("InterfaceId"):

	try:

		interfaceNumber = int(form.getvalue("InterfaceId"))

	except:

		interfaceNumber = form.getvalue("InterfaceId")

else:

	interfaceNumber = None

if form.has_key("ASNumber"):

	try:

		asNumber = int(form.getvalue("ASNumber"))

	except:

		asNumber = form.getvalue("ASNumber")

else:

	asNumber = None

if form.has_key("MinBytes"):

	try:

		minBytes = int(form.getvalue("MinBytes"))

	except:

		minBytes = form.getvalue("MinBytes")

else:

	minBytes = None

if form.has_key("MaxBytes"):

	try:

		maxBytes = int(form.getvalue("MaxBytes"))

	except:

		maxBytes = form.getvalue("MaxBytes")

else:

	maxBytes = None

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

	errors = []

	try:

		if not re.match('^[a-zA-Z][a-zA-Z0-9]*$', label):

			errors.append("Name must contain only letters and numbers")

			errors.append("Name must start with letter")

	except:

		errors.append("Name must contain only letters and numbers")

		errors.append("Name must start with letter")

	try:
	
		if not re.match('^[as]|[interface]|[network]$', str(monitoringType)):

			errors.append("Please do not alter Toa's code")

	except:

		errors.append("Please do not alter Toa's code")

	try:
	
		if re.match('^interface$', str(monitoringType)) and not re.match('^[0-9]+$', str(interfaceNumber)):

			errors.append("Please select an interface number")

	except:

		if re.match('^interface$', str(monitoringType)):

			errors.append("Please select an interface number")

	try:
	
		if re.match('^as$', str(monitoringType)) and not re.match('^[0-9]+$', str(asNumber)):

			errors.append("Please select an AS number")

	except:

		if re.match('^as$', str(monitoringType)):

			errors.append("Please select an AS number")

	try:
	
		if not re.match('^[0-9]+$', str(minBytes)) or not re.match('^[0-9]+$', str(maxBytes)):

			errors.append("Invalid treshold. Treshold must be integers")

		elif int(minBytes) > int(maxBytes):

			errors.append("Invalid treshold")

	except:

		errors.append("Invalid treshold. Treshold must be integers")

	if not NetworkModel.Save(nid, label, monitoringType, interfaceNumber, asNumber, minBytes, maxBytes):

		errors.append("A device with that interface or as number already exist")

	if (errors):

		del NetworkModel

		del UserModel

		del SessionModel

		print "<script language=\"JavaScript\">{location.href=\"../Views/AdminViews/EditNetwork.cgi?uid=%s&sid=%s&remote=%s&errors=%s&nid=%s\";self.focus();}</script>"%(uid, sid, remote, errors, nid)			

	del NetworkModel

	del UserModel

	del SessionModel

	print """<script language=\"JavaScript\">{location.href=\"../Views/AdminViews/EditNetwork.cgi?uid=%s&sid=%s&remote=%s&nid=%s\";self.focus();}</script>"""%(uid, sid, remote, nid)


else:

	print "Database Connection Error. Configuration File Not Found."

	del NetworkModel

	del UserModel

	del SessionModel