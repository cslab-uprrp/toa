##### Imports #####

import struct
import socket
import re         
import MySQLdb  
import sys
from Config import Config

##### Imports #####

class ValidationModel:

	def __init__(self, name = None, user = None, passwd = None, flows_path = None, graphs_path = None, crontime = None):

		if name == None:

			try:

				dbinfo = Config()

			except:

				pass

			try:

				conn = MySQLdb.connect(user=dbinfo.getUser(), passwd=dbinfo.getPassword(), db=dbinfo.getDBName(), host="localhost")

				self.cursor = conn.cursor()

			except MySQLdb.Error, e:

				pass

   				#print "Error %d: %s" % (e.args[0],e.args[1])

		else:

			dbinfo = Config(None, name, user, passwd, flows_path, graphs_path, crontime)

			try:

				conn = MySQLdb.connect(user=dbinfo.getUser(), passwd=dbinfo.getPassword(), db=dbinfo.getDBName(), host="localhost")

				self.cursor = conn.cursor()

			except MySQLdb.Error, e:

				pass

   				#print "Error %d: %s" % (e.args[0],e.args[1])


   	def __del__(self):

		self.cursor.close()


	###################### UserModel Methods ############################

	def isValidEmail(self, Email):

		validator = re.compile("^[a-zA-Z0-9-_.]+\@[a-zA-Z0-9-_.]+\.\w+")

		valid = validator.match(Email)

		if valid:

			return 1

		return 0


	def isValidNetLabel(self, NetLabel):

		validator = re.compile("^[a-zA-Z\d]+$")

		valid = validator.match(NetLabel)

		if valid:

			return 1

		return 0

	def isNumber(self, Number):
	
		validator = re.compile("\d+")

		valid = validator.match(Number)

		if valid:

			return 1

		return 0

	def isValidIp(self, Address):

		validator = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

		valid = validator.match(Address)

		if valid:

			return 1

		return 0


	def isName(self, Name):

		validator = re.compile("^[A-Za-z]+$")

		valid = validator.match(Name)

		if valid:

			return 1

		return 0


