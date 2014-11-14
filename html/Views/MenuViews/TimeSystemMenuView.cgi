#!/usr/bin/python

import cgi
import os
import sys
import cgitb
from datetime import datetime


print "Content-Type: text/html\n\n"
print 

html = "<br><div class='row'><div class='col-md-5 col-md-offset-1'><div class='input-group'><span class='input-group-addon'><i class='glyphicon glyphicon-calendar'></i></span><input class='form-control' name='d1' type='text' id='calendar1' placeholder='From'></div></div><div class='col-md-5'><div class='input-group'><span class='input-group-addon'><i class='glyphicon glyphicon-calendar'></i></span><input class='form-control' name='d2' type='text' id='calendar2' placeholder='to'></div></div></div><br>"

print html