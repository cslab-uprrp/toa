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

NetworkModel = NetworkModel()

Networks = NetworkModel.GetAll()

form = cgi.FieldStorage()

if(form.has_key("Admin")):

	html = "<p style='margin-left:20px;' >Select the network desired to monitor: <select id='network' name='network' onchange='GetSecondSystemMenu(this.options[this.selectedIndex].value, 1);'><option value='None'>Select Network</option>"

	for dev in Networks:

		html += "<option value='%s'>%s</option>"%(dev[0], dev[1])

	html += "</select></p><div class='second_form' id='second_form'></div><br><div class='third_form' id='third_form'></div><div class='time_form' id='time_form'></div>"

else:

	html = "<p style='margin-left:20px;' >Select the network desired to monitor: <select id='network' name='network' onchange='GetSecondSystemMenu(this.options[this.selectedIndex].value);'><option value='None'>Select Network</option>"

	for dev in Networks:

		html += "<option value='%s'>%s</option>"%(dev[0], dev[1])

	html += "</select></p><div class='second_form' id='second_form'></div><br><div class='third_form' id='third_form'></div><div class='time_form' id='time_form'></div>"

print html

