##### Imports #####

import struct
import socket
import re         
import MySQLdb  
import sys
import bcrypt


from Config import Config

##### Imports #####

class UserModel:

	def connect(self, name = None, user = None, passwd = None, flows_path = None, graphs_path = None, crontime = None):

		try:	
		
			dbinfo = Config()
		
			try:

				conn = MySQLdb.connect(user=dbinfo.getUser(), passwd=dbinfo.getPassword(), db=dbinfo.getDBName(), host="localhost")

				self.cursor = conn.cursor()

				return True

			except MySQLdb.Error, e:
				
				pass
                                
				sys.exit(0)
   				
				print "Error %d: %s" % (e.args[0],e.args[1])

				return False


		except:

			dbinfo = Config(None, name, user, passwd, flows_path, graphs_path, crontime)


			try:

				conn = MySQLdb.connect(user=dbinfo.getUser(), passwd=dbinfo.getPassword(), db=dbinfo.getDBName(), host="localhost")

				self.cursor = conn.cursor()

				return True

			except MySQLdb.Error, e:
				
				pass
   				
   				print "Error %d: %s" % (e.args[0],e.args[1])

   				return False


   	def __del__(self):
		
		try:
		
			self.cursor.close()
		
		except:
			pass

	###################### UserModel Methods ############################


	def GetAll(self, uid = None):

		if uid == None:

			self.cursor.execute("""SELECT name FROM USUARIO""")

		else:

			self.cursor.execute("""SELECT name FROM USUARIO WHERE uid != '%s'"""%id)

		return self.cursor.fetchall()


	def Get(self, email, passwd):

		try:

			passwd = bcrypt.hashpw(passwd, '$2a$10$tWEM0OEUvxEyFWJIGaxP2.')

			self.cursor.execute("""select uid from USUARIO where email = '%s' and passwd = '%s'"""%(email, passwd))

			return self.cursor.fetchone()[0]

		except:

			return False


	def Email(self, uid):

		try:
	
			self.cursor.execute("""select email from USUARIO where uid = '%s'"""%(uid))

			return self.cursor.fetchone()

		except MySQLdb.Error:

			return False


	def Privilege(self, id):

		try:

			self.cursor.execute("""SELECT staff FROM USUARIO WHERE uid='%s'"""%id)

			return self.cursor.fetchone()
		except MySQLdb.Error:

			return False

	def ChangePassword(self, np, id):

		try:

			passwd = bcrypt.hashpw(np, '$2a$10$tWEM0OEUvxEyFWJIGaxP2.')

			self.cursor.execute("""UPDATE USUARIO SET passwd='%s' WHERE uid='%s'"""%(passwd,id))

			return True

		except:

			return False


	def Create(self, name, phone, pasw, email, staff):

		try:

			pasw = bcrypt.hashpw(pasw, '$2a$10$tWEM0OEUvxEyFWJIGaxP2.')

			self.cursor.execute("""INSERT INTO USUARIO (name, phone, passwd, email, staff) VALUES ('%s', '%s', '%s', '%s','%s')"""%(name, phone,pasw,email,staff))

			return True

		except MySQLdb.Error:

			return False

	def Delete(self, id):

		try:

			self.cursor.execute("""DELETE FROM USUARIO WHERE uid = '%s'"""%id)

			return True

		except MySQLdb.Error:

			return False

