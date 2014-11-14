
import re
import os
import flowtools
FLOWS_LOCATION = "/CassandraVol/flows"

#**********************************************	**********************************
# The function getIpOctets split an Ip address into network class. For instance,*
# if ip = "136.234.112.3" and the number of octets is 2, the function will		*
# return "136.234".																*
# Pre: the function recieves the whole Ip address and the number of octects to	*
# return.																		*
# Post: The function returns a string containing the new ip address.			*
#********************************************************************************
 
def getIpOctets(ip,octet_numbers):

	ip = ip.split('.') # we get a list with all the octects
	newIp = "" # this variable holds the new ip.
	ip_index = 0 # counter to put only doc between numbers. We do not want, "136.234."
	for i in ip[0:octet_numbers]: # we only take the octects selected by the user.
		#following line doesn't work in version 2.4.3 of python.
		#newIp+=i+("." if count != n-1 else "") # we add a point after each octect execpt the last.
		#instead we use:
		newIp+=i+("",".")[ip_index!=octet_numbers-1]
		ip_index+=1
	return newIp

class Validation:
	
	#def __init__(self,uflow_path,uSrcIp,uDstIp,uSrc_prefix,uDst_prefix,uThold,uTholdValue,uParse):
	def __init__(self):
		pass
		# self.app = app.split('|')[0]
		# self.version = app.split('|')[1]
		# self.srcIp = form.getvalue("srcIp")
		# self.dstIp = form.getvalue("dstIp")
		# self.src_prefix=form.getvalue("src_pre")
		# self.dst_prefix=form.getvalue("dst_pre")
		# self.parse = form.getvalue("PARSE")
		# self.validated = False
	
		# if self.app == 'cube_app':
		# 	self.thold =form.getvalue("thold")
		# 	self.thold_value=form.getvalue("tvalue")
		# elif self.app == 'graph_app':
		# 	if self.version == 'time':
		# 		pass


	def isInteger(self,user_input):
		for letter in user_input:
			# we check is the letter is in the range of 0-9.
			if ord(letter) not in range(47,57):
				return False
		return True

	def ipIsValid(self,IP):
		if IP is None: return False
		ipv4_pattern = re.compile("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
		return (True,False)[ipv4_pattern.match(IP)==None] or IP == 'null'
	
	def wasValidated(self):
		if self.validate: raise Exception('Input was already validated')
	
	def notValidated(self):
		if self.validate: raise Exception('Please validate user input before continue.')

	def validateFlow(self,flow_path):
		# We check that the file to be opened exists.
		if os.path.exists(flow_path):
			try: Flow_Set = flowtools.FlowSet(flow_path)
			except: return -1
			return Flow_Set
		return -1

	def checkAndSetPrefix(self):
		if not self.isInteger(self.src_prefix): self.src_prefix=int(self.src_prefix)
		else: self.src_prefix = 0
		if self.isInteger(self.dst_prefix): self.dst_prefix=int(self.dst_prefix)
		else: self.dst_prefix = 0
		
		if not (self.src_prefix%8==0 and self.src_prefix <= 32): self.src_prefix=0
		if not (self.dst_prefix%8==0 and self.dst_prefix <= 32): self.dst_prefix=0
		self.src_prefix=self.src_prefix/8
		self.dst_prefix=self.dst_prefix/8
	
	def parseValid(self):
		return (self.isInteger(self.parse) and (self.parse=='0' or self.parse=='1'))

	def tholdIsValid(self):
		return (self.thold=='packets' or self.thold=='octets')

	def valid_tValue(self):
		
		if self.validated: self.wasValidated()	
		if not self.tholdIsValid(): return False
		if self.thold_value != None: self.thold_value = self.thold_value.split('|')
		else: return False
		
		if len(self.thold_value) != 2 or self.thold_value[0] == '': return False
			
		if self.thold == 'packets':
			return self.isInteger(self.thold_value[0]) and self.thold_value[1]==''

		if self.thold == 'octets':
			if self.thold_value[1] != '1024' or self.thold_value[1] != '1048576' or self.thold_value[1] != '1073741824':
				self.thold_value[1] = 1024
			else: self.thold_value[1] = int(self.thold_value[1])

			if self.isInteger(self.thold_value[0]): 
				self.thold_value[0] = int(self.thold_value[0])
				return self.thold_value[0] > 0
		
	def validFormInput(self):
		if self.app == 'cube_app':
			if (self.ipIsValid(self.srcIp) and self.ipIsValid(self.dstIp)) and (self.valid_tValue()) and self.parseValid():
				self.checkAndSetPrefix()
				self.validated = True
				return True
			else: return False
		else:
			print 'src = ',self.ipIsValid(self.srcIp)
			print 'dst = ',self.ipIsValid(self.dstIp)
			print 'parsevalid=',self.parseValid()
			print '\n\n'
			print
			if (self.ipIsValid(self.srcIp) and self.ipIsValid(self.dstIp)) and self.parseValid():
				self.checkAndSetPrefix()
				self.validated = True
				return True
			else: return False

	def getValidatedData(self):
		if self.app == 'cube_app':
			return self.srcIp, self.dstIp, self.src_prefix,
			self.dst_prefix, self.thold, self.thold_value
		else:
			return self.srcIp, self.dstIp, self.src_prefix,self.dst_prefix
