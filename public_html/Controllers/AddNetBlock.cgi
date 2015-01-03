#!/usr/bin/python

########### Imports #######################

import cgi
import sys 
import os
import cgitb
import time
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

nid = form.getvalue("nid")

nid = str(nid).strip("(),L")

nid = int(nid)

port = form.getvalue("Port")

now = time.time()#generate the TimeStamp

SessionModel = SessionModel()

UserModel = UserModel()

PortModel = PortModel()

timestamp = SessionModel.Validate(uid, sid, remote, now)

if not timestamp:

    SessionModel.Close(uid, remote)

    del PortModel

    del UserModel

    del SessionModel

    print """<script language=\"JavaScript\">{location.href=\"../index.cgi\";self.focus();}</script>"""

SessionModel.UpdateTimeStamp(now, uid, remote)

PortModel.Add(nid, port)

print """<script language=\"JavaScript\">{location.href=\"../Views/AdminViews/ManagePorts.cgi?nid=%s&uid=%s&sid=%s&remote=%s\";self.focus();}</script>"""%(nid, uid, sid, remote)
