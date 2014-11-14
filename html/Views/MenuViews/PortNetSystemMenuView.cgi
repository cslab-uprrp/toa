#!/usr/bin/python

import cgi
import sys 
import os
import MySQLdb
import cgitb
from datetime import datetime
sys.path.append('../../Models')
from NetworkModel import NetworkModel
from PortModel import PortModel

print "Content-Type: text/html\n\n"

print 

form = cgi.FieldStorage()

identification = form.getvalue("id")

Port = PortModel()

Network = NetworkModel()

devices = Network.GetAll()

if(form.has_key("Admin")):

	html = "<ul>"

	for dev in devices:

		if dev[0] == int(identification):

			ports = Port.Get(dev[0])

			nets = Network.GetNetwork2(dev[0])

			html += "<li id='%s'><div id='dev%s' onclick='GetGraphsView(%s,1)'>DEVICE GRAPH</div><div id='p'>PORT<div id='port_menu'><select name='port' onchange='GetPortGraphsView(this, %s, 1)'><option value=''>Ports</option>"%(dev[0], dev[0], dev[0], dev[0])

			for p in ports:

				html += "<option value='%s'>%s</option>"%(p[0], p[1])

			html += "</select><br></div></div><div id='n'>NET2NET<div id='net_menu'><select name='net' onchange='GetNet2NetGraphsView(this, %s, 1)'><option value=''>Net2Net</option>"%(dev[0])

			for n in nets:

				html += "<option value='%s'>%s</option>"%(n[0], n[1])

			html += "</select><br></div></div></li>"

	html += "</ul>"

else:

	html = "<ul>"

	for dev in devices:

		if dev[0] == int(identification):

			ports = Port.Get(dev[0])

			nets = Network.GetNetwork2(dev[0])

			html += "<li id='%s'><div id='dev%s' onclick='GetGraphsView(%s)'>DEVICE GRAPH</div><div id='p'>PORT<div id='port_menu'><select name='port' onchange='GetPortGraphsView(this, %s)'><option value=''>Ports</option>"%(dev[0], dev[0], dev[0], dev[0])

			for p in ports:

				html += "<option value='%s'>%s</option>"%(p[0], p[1])

			html += "</select><br></div></div><div id='n'>NET2NET<div id='net_menu'><select name='net' onchange='GetNet2NetGraphsView(this, %s)'><option value=''>Net2Net</option>"%(dev[0])

			for n in nets:

				html += "<option value='%s'>%s</option>"%(n[0], n[1])

			html += "</select><br></div></div></li>"

	html += "</ul>"

print html
