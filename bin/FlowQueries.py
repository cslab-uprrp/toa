import sys
import struct
import socket
import re
import MySQLdb

##### SELECT QUERIES #####

def GetLabel(c, id):
	c.execute("""select label from NETWORK where n_id=%s""" % id) 
	return c.fetchone()[0]

def GetNetworks(c):
	c.execute("""select n_id, label from NETWORK""")
	return c.fetchall()

def GetNetworksByUser(c, uid):
	c.execute("""select USUARIO_NETWORK.n_id, label from USUARIO_NETWORK, NETWORK where USUARIO_NETWORK.uid=%s and USUARIO_NETWORK.n_id = NETWORK.n_ID""" % uid) 
	return c.fetchall()

def GetNetwork(c, id):
	c.execute("""select label, interface, asn, tom from NETWORK where n_id=%s""" % id)
	result = c.fetchone()	
	if result:
		return result[0], result[1], result[2], result[3]._data.keys()[0] 

	return None, None, None, None

def GetPorts(c, id):
	c.execute("""select p_id, port from PORT where n_id=%s""" % id)
	return c.fetchall()

def GetPortGraphInfo(c, id, p_id):
	c.execute("""select label, port from NETWORK, PORT where NETWORK.n_id=%s and PORT.p_id=%s""" % (id, p_id))
	return c.fetchone()

def Get2NetGraphInfo(c, id, nn_id):
	c.execute("""select n_id, label from NETWORK, NET2NET where (NETWORK.n_id=fn_id or NETWORK.n_id=tn_id) and NET2NET.nn_id=%s and NET2NET.fn_id=%s""" % (nn_id, id))
	return c.fetchall()


def GetNetworksToSelect(c, id):
	c.execute("""select n_id, label from NETWORK where not EXISTS (select * from NET2NET where fn_id=%s and n_id = tn_id) and n_id <> %s""" % (id,id))
	return c.fetchall()

def GetNetwork2(c, id):
	c.execute("""select nn_id, label, tn_id from NETWORK, NET2NET where fn_id=%s and tn_id=n_id""" % id)
	return c.fetchall()

def GetFromandTo(c,id):
    #this function gets a net2net id and returns the from and to network ids of that connection in an array
        c.execute("select fn_id, tn_id from NET2NET where nn_id=%s"%id)
        return c.fetchall()[0]

def GetReverseNet2Net(c,fn,to):
    #this function gets the from and to network ids of a net2net connection and returns the nn_id (net2net id) of a reverse connection where the to and fn are inversed
        c.execute(" select nn_id from NET2NET where tn_id=%s and fn_id=%s " % (fn,to))
        return c.fetchone()

def GetNetBlocks(c, id):
	c.execute("""select nb_id, ip_from, ip_to from NET_BLOCK where n_id=%s""" % id)
	return c.fetchall()


def displaySelect(name, id, values, default):
        print """<select name='%s' id='%s' onchange="netSelect()">""" % (name,id)
        for val in values:
		if val[0] == default:
       			print "<option value='%s' selected>%s" % (val[0], val[1])
		else:
			print "<option value='%s'>%s" % (val[0], val[1])
        print "</select>"




### DEF INPUT VALIDATION ###
def checkAlpha(str):
	m = re.match("[A-Za-z]+[A-Za-z0-9\-_]*[A-Za-z0-9]$", str)	
	if m:
		if not str == m.group():
			Exit()
	else:
		Exit()

	pass

### INSERT QUERIES ###
def Exit():
	sys.exit(0)

def NewDevice(c, form):
	
	label, tom, asn, int = CheckDeviceInfo(form)	

	try:
		c.execute("""insert into NETWORK (label, tom, interface, asn) values ("%s", "%s", %s, %s)""" % (label, tom, int, asn)) 
		return c.lastrowid
	except MySQLdb.IntegrityError, e:
		print e		
	except:
		print "Unknown Error Please contact administrator"


	return None

def CheckDeviceInfo(form):
	asn = "NULL"
	int = "NULL"
	# REMEMBER INPUT VALIDATION
	try:
		label = form.getfirst("net") 
		tom = form.getfirst("tom")
	except: 
		Exit()

	if tom == "interface":
		if  not form.has_key("int"):
			Exit() 
	elif tom == "as":
		if not form.has_key("as"):
			Exit()
	elif tom == "network":
		pass
	else:
		Exit()

	if form.has_key("int"):
		int = CheckShort(form, "int")
	if form.has_key("as"):
		asn = CheckShort(form, "as")

	return label, tom, asn, int

def SaveDevice(c, id, form):
	label, tom, asn, int = CheckDeviceInfo(form)	
	try:
		return c.execute("""update NETWORK set tom="%s", interface=%s,asn=%s where n_id=%s""" % (tom, int, asn, id)) 
	except MySQLdb.IntegrityError, e:
		print e
		return None
	except:
		print "Unknown Error Please contact administrator"


def CheckShort(form, key):
	if not form.has_key(key):
		Exit()
	else:
		v = form.getfirst(key)
		try:
			v = int(v)
		except:
			Exit()
	
	if v >= 0 and v <= 65535:
		return v
	else:
		Exit()

def CheckIP(form, key):
	if not form.has_key(key):
		Exit()
	addrv = form.getfirst(key)
	m = re.match("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$|^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$|^[0-9]{1,3}\.[0-9]{1,3}$|^[0-9]{1,3}$", addrv)	
	if m:
		if not addrv == m.group():
			Exit()
		addr = m.group().split(".")
		for a in addr:
			a = int(a)
			if a < 0 or a > 255:
				Exit()
	else:
		Exit()

	return addrv 

def AddPort(c, id, form):
	p = CheckShort(form, "p")	
	try:
		return c.execute("""insert into PORT (n_id, port) values (%s, %s)""" % (id, p)) 
	except MySQLdb.IntegrityError, e:
		print e
		return None
	except:
		print "Unknown Error Please contact administrator"


def CheckIDs(form, key):
	if not form.has_key(key):
		Exit()

	ids = form.getvalue(key)
	for i in ids:
		try:
			i = int(i)
		except:
			Exit()
	return ids

def RemovePorts(c, id, form):
	ports = CheckIDs(form, "ports")
	for p in ports:
		DelPort(c, id, p)

def DelPort(c, id, pid):
	try:
		c.execute("""delete from PORT where p_id=%s and n_id=%s""" % (pid, id))
	except:
		print "Unknown Error Please contact administrator"

def AddLink(c, id, form):
	net2 = CheckShort(form, "net2")
	try:
		return c.execute("""insert into NET2NET (fn_id, tn_id) values (%s, %s)""" % (id, net2)) 
	except MySQLdb.IntegrityError, e:
		print e
		return None
	except:
		print "Unknown Error Please contact administrator"

def RemoveLinks(c, id, form):
	links = CheckIDs(form, "links")
	for l in links:
		DelLink(c, id, l)

def DelLink(c, id, lid):
	try:
		c.execute("""delete from NET2NET where nn_id=%s and fn_id=%s""" % (lid, id))
	except:
		print "Unknown Error Please contact administrator"
	
def AddNetBlock(c, id, form):
	ip_from = CheckIP(form, "ip_from")
	ip_to = CheckIP(form, "ip_to")
	ip_from = struct.unpack("!L", socket.inet_aton(ip_from))[0] 
	ip_to = struct.unpack("!L", socket.inet_aton(ip_to)) [0]
	
	if ip_from > ip_to:
		Exit()

	try:
		return c.execute("""insert into NET_BLOCK (n_id, ip_from, ip_to) values (%s, %s, %s)""" % (id, ip_from, ip_to)) 
	except MySQLdb.IntegrityError, e:
		print e
		return None
	except:
		print "Unknown Error Please contact administrator"

def RemoveBlocks(c, id, form):
	blocks = CheckIDs(form, "blocks")
	for b in blocks:
		DelBlock(c, id, b)

def DelBlock(c, id, bid):
	try:
		c.execute("""delete from NET_BLOCK where nb_id=%s and n_id=%s""" % (bid, id))
	except:
		print "Unknown Error Please contact administrator"


def RemoveDevPorts(c, id):
	c.execute("""delete from PORT where n_id=%s""" % id)

def RemoveDevNetBlocks(c, id):
	c.execute("""delete from NET_BLOCK where n_id=%s""" % id)

def RemoveDevLinks(c, id):
	c.execute("""delete from NET2NET where nn_id=%s or fn_id=%s""" % (id, id))

def RemoveUserDevice(c, id):
	c.execute("""delete from USUARIO_NETWORK where n_id=%s""" % id)

def RemoveDevice(c, id):
	c.execute("""delete from NETWORK where n_id=%s""" % id)
	RemoveDevPorts(c, id)
	RemoveDevNetBlocks(c, id)
	RemoveDevLinks(c, id)
	

def CreateJob(c, id):
	c.execute("""insert into JOB (uid) values (%s)""" % id)
	return c.lastrowid()
	

def DeleteJob(c, jid):
	c.execute("""delete from JOB where jid=%s""" % jid)	
