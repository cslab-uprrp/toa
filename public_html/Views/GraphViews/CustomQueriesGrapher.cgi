#!/usr/bin/python



#This file is used to graph the custom query graphs, this is not used for the normal Day,Weekly,Mohtly and Yearly graphs

import MySQLdb
import time
from os.path import join as pjoin
import datetime
import sys
import re
import cgi
import cgitb
cgitb.enable()

sys.path.append('../../Models/')
from SessionModel import SessionModel

from Config import Config

config=Config()

TOAPATH=config.getToaPath();

DB_NAME=config.getDBName();
DB_HOST='localhost'
DB_USER=config.getUser();
DB_PASS=config.getPassword();

INCREMENT=config.getCronTime()

interval_modulation=INCREMENT #sets the number that thetime is going to be modulated by, should be the same as the time increment (if 5min then 300)so that if the module is 0 then the unixtime has ben incremented correctly 


sys.path.append(TOAPATH+'/bin/')
from FlowQueries import *


db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
c = db.cursor()


def validate(form):
	if form.has_key('uid') and form.has_key('sid') and form.has_key('remote'):
		uid=form.getvalue('uid')
		sid=form.getvalue('sid')
		remote=form.getvalue('remote')
		now = datetime.datetime.now()#generate the TimeStamp

		tmstp = now.minute#converting the TimeStamp to string   

		sm = SessionModel()


		if sm.connect():

    			timestamp = sm.Validate(uid, sid, remote)

    			if((timestamp+5)<=tmstp or timestamp == -1):

        			sm.Close(uid, remote)

        			del sm
				c.close()
				return 0
			else:
				return 1
		else:
			c.close()
			return 0
		return 1
	else:
		c.close()
		return 0
	
def normalizeall (input,output,rangeb,rangea):
        start=rangeb
        end=rangea
        join = [[0 for i in range(7)] for j in range(((end-start)/300)-1)]
        c1=c2=x=0
        start =( start - start%300) + 300
        while start <end :
            if c1<len(input) and input[c1][3]==start :
                join[x][0]=input[c1][0]
                join[x][2]=input[c1][1]
                join[x][4]=input[c1][2]
                c1=c1+1
            else:
                join[x][0]=0
                join[x][2]=0
                join[x][4]=0
            if c2<len(output) and output[c2][3]==start  :
                join[x][1]=output[c2][0]
                join[x][3]=output[c2][1]
                join[x][5]=output[c2][2]
                c2=c2+1
            else:
                join[x][1]=0
                join[x][3]=0
                join[x][5]=0

            join[x][6]=start
            start=start+INCREMENT
            x=x+1

        t=tuple(tuple(x) for x in join)
        return t
def normalize (input,output,rangeb,rangea):
#This function and normalizeall are used when a net2net graph is called, to join the data of the two sepearete queries,  found in input and output, into one data structure
        start=rangeb
        end=rangea
        join = [[0 for i in range(3)] for j in range(((end-start)/300)-1)]
        c1=c2=x=0
        start =( start - start%300) + 300
        while start <end :
          
            if c1<len(input) and  input[c1][1]==start  :
                join[x][0]=input[c1][0]
                c1=c1+1
            else:
                join[x][0]=0
            if c2<len(output) and output[c2][1]==start :
                join[x][1]=output[c2][0]
                c2=c2+1
            else:
                join[x][1]=0

            join[x][2]=start
            start=start+INCREMENT
            x=x+1

        t=tuple(tuple(x) for x in join)
        return t

def create_hashes(row,type=None):

#This function creates a hash with a counter for each network that is accessed using the network id as a key
#The purpose is to have different counters for each network so that in case of data inconcesty (some networks have more points in the graphs than others) we can maintain track of the number of points per network even if their quantity varies. 
#Receives rows which contains the network ids and their data. It uses rows to get the network ids that are used as keys in the hash.
# x is the network id and counter[x] is the counter for that network
#It also initializes hashes for the input( data 1 ) and output data (data2), for the average data of each network and the what the data is going to divided for (typediv) (typediv may not be necessary) 
	if type==None:	
		data1={}
		data2={}
		avgdata1={}
		avgdata2={}
		typediv={}
		counter={}
		for i in row.keys():
			counter[i]=0
			data1[i]=0
			data2[i]=0
			avgdata1[i]=0
			avgdata2[i]=0
			typediv[i]=1
		return counter,data1,data2,avgdata1,avgdata2,typediv
	else:
		data={}
		avgdata={}
		typediv={}	
		counter={}
		
		for i in row.keys():	
			counter[i]=0
			data[i]=0
			avgdata[i]=0
			typediv[i]=1
	
		return counter,data,avgdata,typediv
def create_hashes_all(row):
#  Does the same as the previous function but for the "all"graph. Contains 6 data hashes for input and output of octects,packets and flows (respectievely ) 
        data1={}
        data2={}
	data3={}
	data4={}
	data5={}
	data6={}
        avgdata1={}
        avgdata2={}
        avgdata3={}
        avgdata4={}
        avgdata5={}
        avgdata6={}
        typediv={}
        counter={}
        for i in row.keys():
                counter[i]=0
                data1[i]=0
                data2[i]=0
                data3[i]=0
                data4[i]=0
                data5[i]=0
                data6[i]=0
                avgdata1[i]=0
                avgdata2[i]=0
                avgdata3[i]=0
                avgdata4[i]=0
                avgdata5[i]=0
                avgdata6[i]=0
                typediv[i]=[1,1,1]
        return counter,data1,data2,data3,data4,data5,data6,avgdata1,avgdata2,avgdata3,avgdata4,avgdata5,avgdata6,typediv

def setsizetype_all_selectall(row):
        #this function sets the type of size (MB,GB,KB...) that the data is. This is done to propperly resize the lines in the graph since it is easier to read  5 mb than its equivalent in bytes. 
                # It its specifically for the graph that displays all because it sizetype is an array that will hold the sizes of the octects,flows, and packets. 
                        #It receives row which is an dictionary/hash  that contains all the data and  has network ids as keys 

        max = {}
        for i in row.keys():
                max[i]=[0,0,0] 
        
        sizetype={}
        for i in row.keys():
                sizetype[i]=["bytes","bytes","bytes"]
	
	for x in row.keys(): 
            #x is the network index in the row and max hashes  , i is the index indicating a specific point with network data inside the row[x] tupple ,t is the index inside a block of data that specifies between an input or output. In row[x][i] when t is 0-1 we are evaluating the octects, when t is 2-3 we are evaluating the packets and when it is 4-5 we are evaluating the flows. [t] means input and the [t+1] corresponds to the output 
                if len(row[x])>0:
                        for i in range(len(row[x])):
                                t=0
                                for m in range(len(max[x])):
					
                                        if max[x][m] <row[x][i][t]:
                                                max[x][m]=row[x][i][t]

                                        if max[x][m]<row[x][i][t+1]:
                                                max[x][m]=row[x][i][t+1]
                                        t+=2
                        for i in range(len(max[x])):
                                        
                                    if max[x][i] >= 1073741824:
                                            sizetype[x][i]="GB"
                                    elif max[x][i] >= 1048576:
                                            sizetype[x][i]="MB"
                                    elif max[x][i] >= 1024:
                                            sizetype[x][i]="KB"
                                    else:
                                            sizetype[x][i]="bytes"
					
		
	return sizetype

def setsizetype_selectall(row):  
           #this function sets the type of size (MB,GB,KB...) that the data is and returns it in the variable sizetype.  This is done to resize them on the graph propperly .
                           # It its specifically for the individual graphs that display octects or packets or flows and not all of them (for the "all" graph corresponding functions see above)
                                           #It receives row which is a hash that contains the data and has network ids as keys
            # It also returns the max and min amount of data. It defines a hash/dictionary for the max and min and iterates over the data to determine them. 
		min={}
		
		max={}
        	sizetype={}
    		for i in row.keys():
			max[i]=min[i]=0


			
            #i is the network index in the row and max hashes  , m is the index indicating a specific point with network data inside the row[i] tupple ,t is the index inside a block of data that specifies between an input or output  In row[x][i] when the next index is  [0] means input and the [1] corresponds to the output 

                for i in row.keys():

                       		 if len(row[i]) > 0:
                       	         	max[i]=row[i][0][0]
                                	min[i]=row[i][0][1]
                                	for m in range(len(row[i])):
                                       		if max[i]<row[i][m][0]:
                                               		 max[i]=row[i][m][0]
                                        	if max[i]<row[i][m][1]:# The max value of a network is calculated taking into account the inputs and outputs , [0] is input, [1] is output. The same happens for the min
                                                	max[i]=row[i][m][1]
                                        	if min[i]>row[i][m][0]:
                                                	min[i]=row[i][m][0]
                                        	if min[i]>row[i][m][1]:
                                                	min[i]=row[i][m][1]
					

                                        if max[i] >= 1073741824:
                                            sizetype[i]="GB"
                                        elif max[i] >= 1048576:
                                            sizetype[i]="MB"
                                        elif max[i] >= 1024:
                                            sizetype[i]="KB"
                                        else:
                                            sizetype[i]="bytes"
			
		return sizetype,max,min

def setsizetype_plus_selectall(row, type):
           #this function sets the type of size (MB,GB,KB...) that the data is and returns it in the variable sizetype.  This is done to resize them on the graph propperly .
                           # It its specifically for the individual graphs when more then one network is chosen. 
                                           #It receives row which is a hash that contains the data and has network ids as keys
            # It also returns the max and min amount of data. It defines a hash/dictionary for the max and min and iterates over the data to determine them. 
	    #This function has the same functioning as the one above but it is called when the user wants to graphs various networks at the same time by checking more than one checkbox in the menu
            #Another function was created because when the user chooses more than one network we have three graphs per type of data, one only contains the input, another the output and another their sum.This is done to avoid one cluttered graph with everything on it
                        min={}
		
			max={}
        		sizetype={}
    			for i in row.keys():
				sizetype[i]="bytes"
				max[i]=min[i]=0
			
                	for i in row.keys():# i is the index for the network, m is the index inside one of the tupples containing data from that network, [0] means input data and [1] means output

                        	if len(row[i]) > 0:
					if type=="p":

	                                	max[i]=row[i][0][0]+row[i][0][1]#
        	                        	min[i]=row[i][0][1]+row[i][0][0]
					elif type=="i":
						max[i]=row[i][0][0]
						min[i]=row[i][0][0]
					else:
						max[i]=row[i][0][1]
						min[i]=row[i][0][1]		
                                for m in range(len(row[i])):
					if type=="p":
                                        	if max[i]<row[i][m][0]+row[i][m][1]:
                                               		 max[i]=row[i][m][0]+row[i][m][1]
                                   		if min[i]>row[i][m][0]+row[i][m][1]:
                                                	min[i]=row[i][m][0]+row[i][m][1]
					elif  type=="i":
                                        	if max[i]<row[i][m][0]:
                                               		 max[i]=row[i][m][0]
                                   		if min[i]>row[i][m][0]:
                                                	min[i]=row[i][m][0]
					else:
						
                                        	if max[i]<row[i][m][1]:
                                               		 max[i]=row[i][m][1]
                                   		if min[i]>row[i][m][1]:
                                                	min[i]=row[i][m][1]
					

                                if max[i] >= 1073741824:
                                            sizetype[i]="GB"
                                elif max[i] >= 1048576:
                                            sizetype[i]="MB"
                                elif max[i] >= 1024:
                                            sizetype[i]="KB"
                                else:
                                            sizetype[i]="bytes"


			return sizetype,max,min


def GetLabel(c,type,network,checkbox_marked):
    #receives the database cursor (c), weather its normal i/o data, port data or net2net data (type),
    # If the user just wants normal i/o data (when the grapInt function  is called, since there are no checlboxes it uses the network id (network)
    #When it deals with port or net2net data the ids that correspond to the port_ids and net2net connection ids are in checkbox_marked (this happens when this function is called from graphInt_plus)
    #It returns label which contain the labels (names like RUM, RCM, etc.)  corresponding to the ids in the database 
	label_hash={}
	label_hashto={}

	if type=="i/o":
		c.execute("""select label from NETWORK where n_id=%s""" % (network))
		label= c.fetchall()
		if len(label)<=0:
			print "ERROR: no network corresponds to id"
			exit(1)
		label_hash[network]=label[0]
		

	if type=="port":
			
	#	c.execute ("""select label from NETWORK where n_id=%s"""%(network))
        #	label=c.fetchall() #uncomment to add network label to graph title, deemed unecessary and cluttersome 
        #       Code has changed a little so simply uncommenting this may cuase problem with the dictionary because if a port if is also the same as a network id (like 1) then two things will correspond to the same key and be overwritten

		for i in range(len(checkbox_marked)):
			c.execute("""select port from PORT  where p_id=%s """%(checkbox_marked[i]))
			labelport=c.fetchall()
			if len(labelport)<=0:
				print "ERROR: no port  corresponds to port id"
				exit(1)
		
	
			label_hash[checkbox_marked[i]]=labelport[0]



	elif type=="p2p":
		c.execute ("""select label from NETWORK where n_id=%s"""%(network))
		label=c.fetchall()
		if len(label)<=0:
			print "ERROR: no network corresponds to id"
			exit(1)
		label_hash[network]=label[0]
                #label_hash will contain the from label and label_hashto will contain the destination labels
		for i in range(len(checkbox_marked)):
			c.execute(""" select label from NETWORK, NET2NET where tn_id=n_id and  nn_id=%s;"""%(checkbox_marked[i]))
			labelto=c.fetchall()
			if len(labelto)<=0:
				print "ERROR: no destination network corresponds to id"
				exit(1)
                        #print labelto;
			label_hashto[checkbox_marked[i]]=labelto[0]
                       
        		
	return label_hash,label_hashto #lista de tuplos con los labels del network que pertenece y a los que se conecta, acesar el label con lista[posicion][0]


	
def IntRangeO(c, id, checkbox_marked, rangea, rangeb,type):
    #This function retrieves the octects values from the database corresponding to the network id specified in id (when type==" i/o" ) or in checkbox marked when type is otherwie. 
    # It receives c which is the cursor for the database, and the time lapse to be graphed  is expressed in unixtime in rangea and rangeb
    # When the type is " i/o " this function is called from graphInt and otherwise it is called from graphInt_plus 
    # It returns a hash (netdata) that has the id as a key containing tupples with the input, output data
        
	if type=="i/o":
		c.execute("""select ioctect, ooctect,  time_unix from rrd_n where nid=%s and time_unix<'%s' and time_unix>'%s' order by time_unix""" % (id, rangea, rangeb))
		netdata={}
		netdata[id]=c.fetchall()
		return netdata
	elif type=="port":
			netdata={}
			for i in range(len(checkbox_marked)):
				
			
				c.execute("""select ioctect,ooctect,time_unix from rrd_port where pid=%s and time_unix <'%s' and time_unix > '%s' order by time_unix"""%(checkbox_marked[i],rangea,rangeb))
				netdata[checkbox_marked[i]]=c.fetchall() # acessing should be netdata[port id][i][x]
			return netdata
	
		
	else:
			netdata={}
			for i in range(len(checkbox_marked)):
				
		                fromandto=GetFromandTo(c,checkbox_marked[i])
                                reverseid=GetReverseNet2Net(c,fromandto[0],fromandto[1])
                                reverseid=reverseid[0]
			        c.execute("""select ioctect,time_unix from rrd_to_net where nn_id=%s and time_unix <'%s' and time_unix > '%s' order by time_unix"""%(checkbox_marked[i],rangea,rangeb))
                                input=c.fetchall()
			        c.execute("""select ioctect,time_unix from rrd_to_net where nn_id=%s and time_unix <'%s' and time_unix > '%s' order by time_unix"""%(reverseid,rangea,rangeb))
                                output=c.fetchall()
                                netdata[checkbox_marked[i]]=normalize(input,output,rangeb,rangea)

			return netdata
		
def IntRangeP(c, id, checkbox_marked,rangea, rangeb,type):
    #This function retrieves the packet  values from the database corresponding to the network id specified in id (when type==" i/o" ) or in checkbox marked when type is otherwie. 
    # It receives c which is the cursor for the database, and the time lapse to be graphed  is expressed in unixtime in rangea and rangeb
    # When the type is " i/o " this function is called from graphInt and otherwise it is called from graphInt_plus 
    # It returns a hash (netdata) that has the id as a key containing tupples with the input, output data
        if type=="i/o":
		c.execute("""select ipacks, opacks, time_unix from rrd_n where nid=%s and time_unix<'%s' and time_unix>'%s' order by time_unix""" % (id, rangea, rangeb))
		netdata={}
		netdata[id]=c.fetchall()
		return netdata
	elif type=="port":
			netdata={}
			for i in range(len(checkbox_marked)):
				
			
				c.execute("""select ipacks,opacks,time_unix from rrd_port where pid=%s and time_unix <'%s' and time_unix > '%s' order by time_unix"""%(checkbox_marked[i],rangea,rangeb))
				netdata[checkbox_marked[i]]=c.fetchall() # acessing should be netdata[port id][i][x]
			return netdata
		
	else:
			netdata={}
			for i in range(len(checkbox_marked)):
				
		                fromandto=GetFromandTo(c,checkbox_marked[i])
                                reverseid=GetReverseNet2Net(c,fromandto[0],fromandto[1])
                                reverseid=reverseid[0]
			        c.execute("""select ipacks,time_unix from rrd_to_net where nn_id=%s and time_unix <'%s' and time_unix > '%s' order by time_unix"""%(checkbox_marked[i],rangea,rangeb))
                                input=c.fetchall()
			        c.execute("""select ipacks,time_unix from rrd_to_net where nn_id=%s and time_unix <'%s' and time_unix > '%s' order by time_unix"""%(reverseid,rangea,rangeb))
                                output=c.fetchall()
                                netdata[checkbox_marked[i]]=normalize(input,output,rangeb,rangea)
                                    
			return netdata
		
def IntRangeF(c, id, checkbox_marked,rangea, rangeb,type):
    #This function retrieves the flows values from the database corresponding to the network id specified in id (when type==" i/o" ) or in checkbox marked when type is otherwie. 
    # It receives c which is the cursor for the database, and the time lapse to be graphed  is expressed in unixtime in rangea and rangeb
    # When the type is " i/o " this function is called from graphInt and otherwise it is called from graphInt_plus 
    # It returns a hash (netdata) that has the id as a key containing tupples with the input, output data
        if type=="i/o":
		c.execute("""select iflows, oflows, time_unix, time_unix from rrd_n where nid=%s and time_unix<'%s' and time_unix>'%s' order by time_unix""" % (id, rangea, rangeb))
		netdata={}
		netdata[id]=c.fetchall()
		return netdata
	
	elif type=="port":
			netdata={}
			for i in range(len(checkbox_marked)):
				
			
				c.execute("""select iflows,oflows,time_unix from rrd_port where pid=%s and time_unix <'%s' and time_unix > '%s' order by time_unix"""%(checkbox_marked[i],rangea,rangeb))
				netdata[checkbox_marked[i]]=c.fetchall() # acessing should be netdata[port id][i][x]
			return netdata
		
	else:
			netdata={}
			for i in range(len(checkbox_marked)):
		                fromandto=GetFromandTo(c,checkbox_marked[i])
                                reverseid=GetReverseNet2Net(c,fromandto[0],fromandto[1])
                                reverseid=reverseid[0]
			        c.execute("""select iflows,time_unix from rrd_to_net where nn_id=%s and time_unix <'%s' and time_unix > '%s' order by time_unix"""%(checkbox_marked[i],rangea,rangeb))
                                input=c.fetchall()
			        c.execute("""select iflows,time_unix from rrd_to_net where nn_id=%s and time_unix <'%s' and time_unix > '%s' order by time_unix"""%(reverseid,rangea,rangeb))
                                output=c.fetchall()
                                netdata[checkbox_marked[i]]=normalize(input,output,rangeb,rangea)
			return netdata

		
def IntRangeAll(c, id, checkbox_marked, rangea, rangeb,type):
    #This function retrieves the octects, , packets and  flows  values from the database corresponding to the network id specified in id (when type==" i/o" ) or in checkbox marked when type is otherwie. 
    # It receives c which is the cursor for the database, and the time lapse to be graphed  is expressed in unixtime in rangea and rangeb
    # When the type is " i/o " this function is called from graphInt and otherwise it is called from graphInt_plus 
    # It returns a hash (netdata) that has the id as a key containing tupples with the input, output data
	if type=="i/o":
		c.execute("""select ioctect,ooctect,ipacks,opacks,iflows,oflows, time_unix from rrd_n where nid=%s and time_unix<'%s' and time_unix>'%s' order by time_unix""" % (id, rangea, rangeb))
		netdata={}
		netdata[id]=c.fetchall()
		return netdata
	elif type=="port":
			netdata={}
			for i in range(len(checkbox_marked)):
				
			
				c.execute("""select ioctect,ooctect,ipacks,opacks,iflows,oflows,time_unix from rrd_port where pid=%s and time_unix <'%s' and time_unix > '%s' order by time_unix"""%(checkbox_marked[i],rangea,rangeb))
				netdata[checkbox_marked[i]]=c.fetchall() # acessing should be netdata[port id][i][x]
			return netdata

		
	else:
			netdata={}
			for i in range(len(checkbox_marked)):
		                fromandto=GetFromandTo(c,checkbox_marked[i])
                                reverseid=GetReverseNet2Net(c,fromandto[0],fromandto[1])
                                reverseid=reverseid[0]
			        c.execute("""select ioctect,ipacks,iflows,time_unix from rrd_to_net where nn_id=%s and time_unix <'%s' and time_unix > '%s' order by time_unix"""%(checkbox_marked[i],rangea,rangeb))
                                input=c.fetchall()
			        c.execute("""select ioctect,ipacks,iflows,time_unix from rrd_to_net where nn_id=%s and time_unix <'%s' and time_unix > '%s' order by time_unix"""%(reverseid,rangea,rangeb))
                                output=c.fetchall()
                                netdata[checkbox_marked[i]]=normalizeall(input,output,rangeb,rangea)
				
			return netdata
		
		

	
def gen_ioscript_header_selectall(sizetype,label,labelto,type):
        # This function creates the graph headers when only one network is chosen. 
        # It receives sizeype which is either mb, kb,bytes or GB, type which is either i/o port or net2net. 
        # Label is the network label when type is i/o and port . When it is net2net it contains the from label and labelto contains the destination
	graph_head = """
        
        // Create and populate the data table.
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'x');"""
        if  type=="p2p":

    	    for i in sizetype.keys():
		graph_head+="""
	        data.addColumn(\'number\', \' %s Input   %s \');
       		data.addColumn(\'number\', \'%s Output %s \');"""%(labelto[i][0],sizetype[i],labelto[i][0],sizetype[i])
        else:
    	    for i in sizetype.keys():
		graph_head+="""
	        data.addColumn(\'number\', \' %s Input   %s \');
       		data.addColumn(\'number\', \'%s Output %s \');"""%(label[i][0],sizetype[i],label[i][0],sizetype[i])

        return graph_head
def gen_ioscript_plus_header_selectall(sizetype,label,labelto,type,ifp2p):
        # This function creates the graph headers when only one network is chosen.
	# this is called when more than one network is checkmarked  
        # It receives sizeype which is either mb, kb,bytes or GB, ifp2p says if it is a net2net graph. 
        # Label is the network label when ifp2p is not p2p (meaning it  is i/o or port)
        # labelto contains the destination
	graph_head = """
        // Create and populate the data table.
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'x');"""
	if type=="p":
		column=" Input + Output"
	elif type=="i":
		column="Input"
	else:
		column=" Output"
        if ifp2p=="p2p":
	    for i in sizetype.keys():
		graph_head+="""
	        data.addColumn(\'number\', \' %s %s  %s \');"""%(labelto[i][0],column,sizetype[i])
        else:
	    for i in sizetype.keys():

		graph_head+="""
	        data.addColumn(\'number\', \' %s %s  %s \');"""%(label[i][0],column,sizetype[i])

        return graph_head

def gen_ioascript_header_selectall(sizetype,label,labelto,type):
        # This function creates the graph headers when only one network is chosen in an "all" graph. 
        # It receives sizeype which is either mb, kb,bytes or GB, type which is either i/o port or net2net. 
        # Label is the network label when type is i/o and port . When it is net2net it contains the from label and labelto contains the destination
        graph_head = """
        // Create and populate the data table.
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'x');"""


        if type=="p2p":
            for i in sizetype.keys():
                graph_head+="""
                data.addColumn(\'number\', \' %s Octects Input %s \');
                data.addColumn(\'number\', \' %s OCtects Output %s \');
                data.addColumn(\'number\', \' %s Packets Input %s \');
                data.addColumn(\'number\', \'%s Packets Output %s \');
                data.addColumn(\'number\', \'%s Flows Input %s \');
                data.addColumn(\'number\', \'%sFlows Output %s \');"""%(labelto[i][0],sizetype[i][0],labelto[i][0],sizetype[i][0],labelto[i][0],sizetype[i][1],labelto[i][0],sizetype[i][1],labelto[i][0],sizetype[i][2],labelto[i][0],sizetype[i][2])
        else:
            for i in sizetype.keys():
                graph_head+="""
                data.addColumn(\'number\', \' %s Octects Input %s \');
                data.addColumn(\'number\', \' %s OCtects Output %s \');
                data.addColumn(\'number\', \' %s Packets Input %s \');
                data.addColumn(\'number\', \'%s Packets Output %s \');
                data.addColumn(\'number\', \'%s Flows Input %s \');
                data.addColumn(\'number\', \'%s Flows Output %s \');"""%(label[i][0],sizetype[i][0],label[i][0],sizetype[i][0],label[i][0],sizetype[i][1],label[i][0],sizetype[i][1],label[i][0],sizetype[i][2],label[i][0],sizetype[i][2])


        return graph_head


	
def gen_iodata_selectall(now,first,row,sizetype,evaluate):
        # This function generates the data part of the graph for graphs with one network only except the "all" graph
        # It receives now and first which indicate the time itnerval for the graph being generated
        # row is a dictionary containing all the data with the network id as key
        # sizetype indicate if it is bytes, kb,mb or gb. Evaluate indicates if it is a graph for a day,week, month or year
        if evaluate == "D":
                sumador = INCREMENT 
                #sumador indicates the interval we are averaging. If it is a day we dont average and display points every time intervaldesignated in the INCREMENT in the config file. If it is another we sopecify a time interval where we aggregate all those points in the itnerval and generate a point based on the average of those points. 

        elif evaluate == "W":
                sumador = 1800
        elif evaluate == "M":
                sumador = 7200
        else:
                sumador = 86400

        limit=first+sumador
        

	counter,data1,data2,avgdata1,avgdata2,typediv=create_hashes(row)

	totalcount=0 
        # total count is an iterater used when inteating from first to limit, to then divide with to calculate the average. 
        for i in row.keys():
                #for each network we set typediv which id used to convert the numbers from bytes to the type of data specified in sizetype

                if sizetype[i]=="KB":
                        typediv[i]=1024.0
                elif sizetype[i]=="MB":
                        typediv[i]=1048576.0
                elif sizetype[i]=="GB":
                        typediv[i]=1073741824.0

        graph_data = ""
       
        time_graph = 0


        while first <= now: #iterates over the time interval

                while first <  limit: #the interval that is being agregated and avareged
                        time_graph=time_graph = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(first)) # lo puedo hacer aqui por que el tiempo para todos los networks es el mismo
                        
			for x in row.keys():# iterates over the networks 
			#x is the index that identifies the network
                                 dbtime=0
                                 if counter[x]<len(row[x]):#check if counter is not bigger than the amount of data
                                    dbtime=row[x][counter[x]][2] #The time of the current data point in the row array
                                    if dbtime%INCREMENT !=0: #if the data point in the array does not contain a time stamp that falls in the 5 minute increments 
                                        dbtime =  (dbtime - (dbtime%INCREMENT) ) #+ 300
                                 if  counter[x] < len(row[x])  and    first==dbtime : # IMPORTANTE: verificar si esto afecta en algo y por que surgia el bug con el if 
					data1[x]=data1[x] + row[x][counter[x]][0]
                                        data2[x]=data2[x] + row[x][counter[x]][1]
                         		counter[x]=counter[x]+1           
					    #graph_data += (""" data.addRow(["'%s'", %s, %s]); """ % (row[i][2], row[i][0]/divi, row[i][1]/divi))
                               	 else:
					
					
                                        data1[x]=data1[x] +0
                                        data2[x]=data2[x] + 0
								
                         		#counter[x]=counter[x]+1           
                        
			            #graph_data += (""" data.addRow(["'%s'", 0, 0]); """ %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(first))))
                        first+=INCREMENT
                        totalcount+=1
                for l in data1.keys():
                        avgdata1[l]=data1[l]/totalcount#avgdata is the average of the data being calculated
                for l in data2.keys():
                        avgdata2[l]=data2[l]/totalcount#avgdata es el promedio de la data calculado
                timedisplay=time_graph.split("-")

                if evaluate=="D": #the following ifs and else are for formatting the date displayed in the graph(i.e if it is for 24h we only show the hours)

                        split_time=timedisplay[2].split(" ")
                        graph_data+=("""data.addRow(["'%s'" """)%(split_time[1])
                        for m in avgdata1.keys():
                                graph_data+=(""" ,%.2f,%.2f """) %(avgdata1[m]/typediv[m],avgdata2[m]/typediv[m])
                        graph_data+=("""]);""")


                elif evaluate=="W":
                        graph_data+=("""data.addRow(["'%s'" """)%(timedisplay[2])
                        for m in avgdata1.keys():
                                graph_data+=(""", %.2f,%.2f """) %(avgdata1[m]/typediv[m],avgdata2[m]/typediv[m])
                        graph_data+=("""]);""")

                elif evaluate=="M":
			graph_data+=("""data.addRow(["'%s'" """) %(timedisplay[1]+" "+timedisplay[2])
			for m in avgdata1.keys():
				graph_data+=(""" ,%.2f,%.2f """)%(avgdata1[m]/typediv[m],avgdata2[m]/typediv[m])

		
                        graph_data+=("""]);""")
                else:

                        graph_data+=("""data.addRow(["'%s'" """%(timedisplay))
                        for m in avgdata1.keys():
                                graph_data+=(""" ,%.2f,%.2f """) %(avgdata1[m]/typediv[m],avgdata2[m]/typediv[m])
                        graph_data+=("""]);""")
#############################
                totalcount=0
                limit=limit+sumador
		for i  in row.keys():
			data1[i]=data2[i]=0;
	return  graph_data

def gen_iodata_plus_selectall(now,first,row,sizetype,type,evaluate):
        # This function generates the data part of the graph for graphs with more than one  network
        # It receives now and first which indicate the time itnerval for the graph being generated
        # row is a dictionary containing all the data with the network id as key
        # sizetype indicate if it is bytes, kb,mb or gb. Evaluate indicates if it is a graph for a day,week, month or year
        # type indicates if it is a graph about  output, input or output+input. This is the way graphs with more than one network are organized
        if evaluate == "D":
                sumador = INCREMENT
        elif evaluate == "W":
                sumador = 1800
        elif evaluate == "M":
                sumador = 7200
        else:
                sumador = 86400

        limit=first+sumador
        

	counter,data,avgdata,typediv=create_hashes(row,"plus")

	totalcount=0 

        # total count is an iterater used when inteating from first to limit, to then divide with to calculate the average. 
        for i in row.keys():


                if sizetype[i]=="KB":
                        typediv[i]=1024.0
                elif sizetype[i]=="MB":
                        typediv[i]=1048576.0
                elif sizetype[i]=="GB":
                        typediv[i]=1073741824.0

        graph_data = ""
       
        time_graph = 0


        while first <= now:
                #iterates over the whole interval specified
                while first < limit:
                        #iterates over the interval being averaged 
                        time_graph=time_graph = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(first)) # lo puedo hacer aqui por que el tiempo para todos los networks es el mismo
                        
			for x in row.keys(): 
			#x is the network key
                                 dbtime=0
                                 if counter[x]<len(row[x]):#check if counter is not bigger than the amount of data
                                    dbtime=row[x][counter[x]][2] #The time of the current data point in the row array
                                    if dbtime%INCREMENT !=0: #if the data point in the array does not contain a time stamp that falls in the 5 minute increments 
                                        dbtime =  (dbtime - (dbtime%INCREMENT) ) #+ 300

                             	 if  counter[x] < len(row[x])  and first==dbtime : 
					if type=="p": #if type is p (plus) then it is the sum of input and ouput
						data[x]=data[x]+row[x][counter[x]][0]+row[x][counter[x]][1]
					elif type=="i":#input
						data[x]=data[x]+row[x][counter[x]][0]
					else:#output
						data[x]=data[x]+row[x][counter[x]][1]
						
                         		counter[x]=counter[x]+1           
                               	 else:
					
					
                                        data[x]=data[x] +0
								
                        first+=INCREMENT
                        totalcount+=1
                for l in data.keys():
                        avgdata[l]=data[l]/totalcount#avgdata is the average of the data calculated
                timedisplay=time_graph.split("-")

                if evaluate=="D": #formatting the time for the graph

                        split_time=timedisplay[2].split(" ")
                        graph_data+=("""data.addRow(["'%s'" """)%(split_time[1])
                        for m in avgdata.keys():
                                graph_data+=(""" ,%.2f""") %(avgdata[m]/typediv[m])
                        graph_data+=("""]);""")


                elif evaluate=="W":
                        graph_data+=("""data.addRow(["'%s'" """)%(timedisplay[2])
                        for m in avgdata.keys():
                                graph_data+=(""", %.2f """) %(avgdata[m]/typediv[m])
                        graph_data+=("""]);""")

                elif evaluate=="M":


                        graph_data+=("""data.addRow(["'%s'" """)%(timedisplay[1]+" "+timedisplay[2])
                        for m in avgdata.keys():
                                graph_data+=(""" ,%.2f """) %(avgdata[m]/typediv[m])
                        graph_data+=("""]);""")
                else:

                        graph_data+=("""data.addRow(["'%s'" """)%(timedisplay)
                        for m in avgdata.keys():
                                graph_data+=(""" ,%.2f """) %(avgdata[m]/typediv[m])
                        graph_data+=("""]);""")
#############################
                totalcount=0
                limit=limit+sumador
		for i  in row.keys():
			data[i]=0
	return  graph_data

def gen_ioadata_selectall(now,first,row,sizetype,evaluate):
        # This function generates the data part of the graph for "all" graphs with one network only 
        # It receives now and first which indicate the time itnerval for the graph being generated
        # row is a dictionary containing all the data with the network id as key
        # sizetype indicate if it is bytes, kb,mb or gb. Evaluate indicates if it is a graph for a day,week, month or year
	

        if evaluate == "D":
                sumador = INCREMENT
        elif evaluate == "W":
                sumador = 1800
        elif evaluate == "M":
                sumador = 7200
        else:
                sumador = 86400
	
        limit=first+sumador
                #sumador indicates the interval we are averaging. If it is a day we dont average and display points every time intervaldesignated in the INCREMENT in the config file. If it is another we sopecify a time interval where we aggregate all those points in the itnerval and generate a point based on the average of those points. 
	
        counter,data1,data2,data3,data4,data5,data6,avgdata1,avgdata2,avgdata3,avgdata4,avgdata5,avgdata6,typediv=create_hashes_all(row)
	totalcount=0 #Cuenta todas las iteraciones para si es necesario desps dividir y sacar el promedio
        graph_data = ""
        
	

       	for n in sizetype.keys():
                for m in range(len(sizetype[n])):
                        if sizetype[n][m]=="KB":
                                typediv[n][m]=1024.0
                        elif sizetype[n][m]=="MB":
                                typediv[n][m]=1048576.0
                        elif sizetype[n][m]=="GB":
                                typediv[n][m]=1073741824.0


	
        
        while first <=  now:
		
                while first < limit:
		       		      
                       time_graph = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(first))
                       for x in row.keys():
                          dbtime=0
                          if counter[x]<len(row[x]):#check if counter is not bigger than the amount of data
                            dbtime=row[x][counter[x]][6] #The time of the current data point in the row array
                            if dbtime%INCREMENT !=0: #if the data point in the array does not contain a time stamp that falls in the 5 minute increments 
                                dbtime =  (dbtime - (dbtime%INCREMENT) ) # Fixes the above problem 
		          
		          if  counter[x]< len(row[x]) and dbtime==first: 		
				#data 1 and  2 are octects, 3 and 4 are packets and 5 and 6 are flows
                       		data1[x]=data1[x] + row[x][counter[x]][0]
                       		data2[x]=data2[x] + row[x][counter[x]][1]
                      		data3[x]=data3[x] + row[x][counter[x]][2]
                       		data4[x]=data4[x] + row[x][counter[x]][3]
                       		data5[x]=data5[x] + row[x][counter[x]][4]
                       		data6[x]=data6[x] + row[x][counter[x]][5]
		       			
               	       		counter[x]+=1
			  else:
                       		data1[x]=data1[x] + 0
                       		data2[x]=data2[x] + 0
                      		data3[x]=data3[x] + 0
                       		data4[x]=data4[x] + 0
                       		data5[x]=data5[x] + 0
                       		data6[x]=data6[x] + 0
			
		       first+=INCREMENT
                       totalcount+=1
           	for x in data1.keys():#There is no specific reason for iterating over data 1 because all of them have the same keys

                        avgdata1[x]=data1[x]/totalcount#avgdata es el promedio de la data calculado
                        avgdata2[x]=data2[x]/totalcount
                        avgdata3[x]=data3[x]/totalcount#avgdata es el promedio de la data calculado
                        avgdata4[x]=data4[x]/totalcount
                        avgdata5[x]=data5[x]/totalcount#avgdata es el promedio de la data calculado
                        avgdata6[x]=data6[x]/totalcount
                timedisplay=time_graph.split("-")
                if evaluate=="D": #date formatting 

                        split_time=timedisplay[2].split(" ")

                        graph_data+=(""" data.addRow(["'%s'" """)%(split_time[1])
                        for x in row.keys():
                                graph_data+= ("""  ,%.2f, %.2f, %.2f, %.2f, %.2f, %.2f """)% ( avgdata1[x]/typediv[x][0], avgdata2[x]/typediv[x][0], avgdata3[x]/typediv[x][1],avgdata4[x]/typediv[x][1],avgdata5[x]/typediv[x][2],avgdata6[x]/typediv[x][2])
                        graph_data+="]);"
		elif evaluate=="W":
			
                        graph_data+=("""data.addRow(["'%s'" """)%(timedisplay[2])
                        for x in row.keys():
                                graph_data+=(""", %.2f,%.2f,%.2f,%.2f,%.2f,%.2f """) %(avgdata1[x]/typediv[x][0],avgdata2[x]/typediv[x][0],avgdata3[x]/typediv[x][1],avgdata4[x]/typediv[x][1],avgdata5[x]/typediv[x][2],avgdata6[x]/typediv[x][0])
                        graph_data+=("""]);""")
		elif evaluate=="M":
			
                        graph_data+=("""data.addRow(["'%s'" """)%(timedisplay[1]+" "+timedisplay[2])
			for x in row.keys():
                           	graph_data+= ("""  ,%.2f, %.2f, %.2f, %.2f, %.2f, %.2f """)% ( avgdata1[x]/typediv[x][0], avgdata2[x]/typediv[x][0], avgdata3[x]/typediv[x][1],avgdata4[x]/typediv[x][1],avgdata5[x]/typediv[x][2],avgdata6[x]/typediv[x][2])
                        graph_data+="]);"
		else:
					
                        graph_data+=("""data.addRow(["'%s'" """)%(timedisplay)
			for x in row.keys():
                           	graph_data+= ("""  ,%.2f, %.2f, %.2f, %.2f, %.2f, %.2f """)% ( avgdata1[x]/typediv[x][0], avgdata2[x]/typediv[x][0], avgdata3[x]/typediv[x][1],avgdata4[x]/typediv[x][1],avgdata5[x]/typediv[x][2],avgdata6[x]/typediv[x][2])
                        graph_data+="]);"
		
                totalcount=0

                limit=limit+sumador
                for x  in row.keys():
                        data1[x]=data2[x]=data3[x]=data4[x]=data5[x]=data6[x]=0
        return graph_data




def gen_ioscript_footer_selectall(label,labelto, type, unit,graphname,max,min,sizetype,id):
    #unit indicates if it is octects packets or flows
    #This function generates the footer for graphs  (except the all graph) 
    # label contains the label for the network and if type is p2p then it will contain the label of the from network while labelto will contain the destination network
    #max and min are the maximum and minimun points in the graph .
    #unit graphname are identifiers used in the html for the css
        typediv={}
        minlabel={}
        for i in sizetype.keys():

                if sizetype[i]=="KB":
                        typediv[i]=1024.0
                elif sizetype[i]=="MB":
                        typediv[i]=1048576.0
                elif sizetype[i]=="GB":
                        typediv[i]=1073741824.0
		else:
			typediv[i]=1
                #This part of the code sets a seperate type of size for the min values, before only the max was set for averaging purposes
                # this section can be moved to the sizetype function 

                if min [i] >= 1073741824:
                    minlabel[i] = "%.2f GB" % (min[i] / 1073741824.0) #2f is used to round up the numbers 
                elif min[i] >= 1048576:
                    minlabel[i] = "%.2f MB" % (min[i] / 1048576.0)
                elif min[i] >= 1024:
                    minlabel[i] = "%s.2f KB" % (min[i] / 1024.0)
                else:
                    minlabel[i] = "%s bytes" % min[i] 
	if type=="p2p": #According to the type the footer is formated different
		graph_foot=""
		for m in label.keys():
		    graph_footbegining=("""var net = new google.visualization.AreaChart(document.getElementById('%s'));
       		     	net.draw(data, {curveType: "function",
       	       		  width:750, height: 400, title: '%s   Traffic  From %s  to :""")%(graphname,unit,label[m][0])
                                #print graph_foot
                for m in labelto.keys():
		     graph_foot+="""  %s Max: %.2f %s  Min: %s """%(labelto[m][0],max[m]/typediv[m],sizetype[m],minlabel[m])
			

		graph_foot+=("""', titleX: 'Time', titleY: '%s',
                        vAxis: {maxValue: 10}}
                );
        
      """ % ( unit))
                graph_foot=graph_footbegining+graph_foot
	elif type=="port":
		
		graph_foot=("""var net = new google.visualization.AreaChart(document.getElementById('%s'));
       		     	net.draw(data, {curveType: "function",
       	       		  width:750, height: 400, title: '%s   Traffic  """)%(graphname,unit)
		for m in label.keys():
		
				  graph_foot+=""" Port  %s Max: %.2f %s  Min: %s """%(label[m][0],int(max[m])/typediv[m],sizetype[m],minlabel[m])
			

		graph_foot+=("""', titleX: 'Time', titleY: '%s',
                        vAxis: {maxValue: 10}}
                );
        
      """ % ( unit))
	else:
		for m in label.keys():
				graph_foot=("""var net = new google.visualization.AreaChart(document.getElementById('%s'));
       		     	net.draw(data, {curveType: "function",
       	       		  width:750, height: 400, title: '%s   Traffic  From %s  Max: %.2f %s Min: %s """)%(graphname,unit, label[m][0],max[m]/typediv[m],sizetype[m],minlabel[m])
		

		graph_foot+=("""', titleX: 'Time', titleY: '%s',
                        vAxis: {maxValue: 10}}
                );
        
      """ % ( unit))
		
		
		
        return graph_foot

def gen_ioascript_footer_selectall(label,labelto,type, graphname,id):
    #This function generates the footer for the all graph 
    # label contains the label for the network and if type is p2p then it will contain the label of the from network while labelto will contain the destination network
    # graphname are identifiers used in the html for the css
	if type=="p2p":
		graph_foot=""
		for i in label.keys():
            
       		 		graph_footbegin = """var net = new google.visualization.LineChart(document.getElementById('%s')).
       	     draw(data, {curveType: "function",
       	                 width:750, height: 400,title: ' Net Traffic From %s To:"""%(graphname,label[i][0])
		for i in labelto.keys():
				graph_foot+=""" %s """%(labelto[i][0])
		graph_foot=graph_footbegin+graph_foot

	elif type=="port":
		
       		 graph_foot = """new google.visualization.LineChart(document.getElementById('%s')).
       	     draw(data, {curveType: "function",
       	                 width:750, height:400,title: ' Net Traffic From """%(graphname)
		
		 for i in label.keys():
			graph_foot+=" Port %s "%(label[i][0]) 
	else:
		for i in label.keys(): 
       		 		graph_foot = """new google.visualization.LineChart(document.getElementById('%s')).
       	     draw(data, {curveType: "function",
       	                 width:750, height: 400,title: ' Net Traffic From %s:"""%(graphname,label[i][0])

	graph_foot+="""', titleX: 'Time', titleY: 'Network',
                        vAxis: {maxValue: 10}}
                );


       """ 

	return graph_foot

def create_title(label,labelto,type,first,now,id):
    #this function receives the labels for the networks and generates a title for the graph.
    # if type is p2p label will contain the from network and labelto will contain the destination network 
	if type=="p2p":	
                title=""
		for i in label.keys():
				title1="""%s to 
					"""%(label[i][0])
		for  i in labelto.keys():
				title+="  %s " %(labelto[i][0])
		title=title1+title
	elif type=="port":
                title="Ports: "
		for i in label.keys():
			
				title+=" %s "%(label[i][0])
		
	else:
		for i in label.keys():
			title="%s"%(label[i][0])
       	title+=""" from %s to 
		 %s""" % ( first, now)
		
	return title
def graphInt_plus(label,labelto,id,checkbox_marked, now, first,type,evaluate):
        #this function is different than graphInt because it is called when more than one network or port  is chosen
        # this is not used for the i/o graphs because it is always one network
        # Because of this graphs are generated for input+output, input and output (notice the p, i and o parameters)
        #  port ids or net2 net connections cjhosen are stored in the checkbox_marked array
        #It recieves first and now which are the time interval for the graph
        #Evaluate indicates if it is a time interval of less than a day, a week , month or a year or more
        #id is the network id
        #title is the graph title created with the create_title function and label label to are the labels corresponding the options chosen

	
        FILE=""


	
	
	first=first-first%INCREMENT #the 2 following lines normilieze the timestamp in case it is out of sync with the increment expected  

        now=now-now%INCREMENT
	

	# The I/O Network data (24h)
	

	row = IntRangeO(c,id,checkbox_marked,now,first,type)


	if row:#Cautionary if for checking if there was nothing in the database, if that happens row is empty and we dont graph.  
			    
			FILE+="#graph"

                        sizetype,max,min=setsizetype_plus_selectall(row,"p") #en este caso los return values son un hashes 
			FILE+=gen_ioscript_plus_header_selectall(sizetype,label,labelto,"p",type)
			FILE+=gen_iodata_plus_selectall(now,first,row,sizetype,"p",evaluate)
			FILE+=gen_ioscript_footer_selectall(label,labelto,type, "Octects", "viz1",max,min,sizetype,id) 
		
			FILE+="#graph"
			sizetype,max,min=setsizetype_plus_selectall(row,"o") #en este caso los return values son un hashes 
			FILE+=gen_ioscript_plus_header_selectall(sizetype,label,labelto,"o",type)
			FILE+=gen_iodata_plus_selectall(now,first,row,sizetype,"o",evaluate)
			FILE+=gen_ioscript_footer_selectall(label,labelto,type, "Octects", "viz2",max,min,sizetype,id) 
			
			FILE+="#graph"
                        sizetype,max,min=setsizetype_plus_selectall(row,"i") #en este caso los return values son un hashes 
			FILE+=gen_ioscript_plus_header_selectall(sizetype,label,labelto,"i",type)
			FILE+=gen_iodata_plus_selectall(now,first,row,sizetype,"i",evaluate)
			FILE+=gen_ioscript_footer_selectall(label,labelto,type, "Octects", "viz3",max,min,sizetype,id) 

	
# The I/O Packet data
	

	row = IntRangeP(c, id,checkbox_marked,now, first,type)

	if row:
			FILE+="#graph"
			sizetype,max,min=setsizetype_plus_selectall(row,"p") #en este caso los return values son arreglos
			FILE+=gen_ioscript_plus_header_selectall(sizetype,label,labelto,"p",type)
			FILE+=gen_iodata_plus_selectall(now,first,row,sizetype,"p",evaluate)
			FILE+=gen_ioscript_footer_selectall(label, labelto,type,"Packet", "viz4",max,min,sizetype,id) 
			
			FILE+="#graph"
			sizetype,max,min=setsizetype_plus_selectall(row,"o") #en este caso los return values son arreglos
			FILE+=gen_ioscript_plus_header_selectall(sizetype,label,labelto,"o",type)
			FILE+=gen_iodata_plus_selectall(now,first,row,sizetype,"o",evaluate)
			FILE+=gen_ioscript_footer_selectall(label,labelto, type,"Packet", "viz5",max,min,sizetype,id) 


			FILE+="#graph"
			sizetype,max,min=setsizetype_plus_selectall(row,"i") #en este caso los return values son arreglos
			FILE+=gen_ioscript_plus_header_selectall(sizetype,label,labelto,"i",type)
			FILE+=gen_iodata_plus_selectall(now,first,row,sizetype,"i",evaluate)
			FILE+=gen_ioscript_footer_selectall(label,labelto, type,"Packet", "viz6",max,min,sizetype,id) 
# The I/O Flow data


	row = IntRangeF(c, id, checkbox_marked, now, first,type)

	if row:
			FILE+="#graph"

			sizetype,max,min=setsizetype_plus_selectall(row,"p") #en este caso los return values son arreglos
			FILE+=gen_ioscript_plus_header_selectall(sizetype,label,labelto,"p",type)
			FILE+=gen_iodata_plus_selectall(now,first,row,sizetype,"p",evaluate)
			FILE+=gen_ioscript_footer_selectall(label,labelto, type,"Flows", "viz7",max,min,sizetype,id) 
			
			FILE+="#graph"
			
			sizetype,max,min=setsizetype_plus_selectall(row,"o") #en este caso los return values son arreglos
			FILE+=gen_ioscript_plus_header_selectall(sizetype,label,labelto,"o",type)
			FILE+=gen_iodata_plus_selectall(now,first,row,sizetype,"o",evaluate)
			FILE+=gen_ioscript_footer_selectall(label, labelto,type,"Flows", "viz8",max,min,sizetype,id) 
			
			FILE+="#graph"
                        sizetype,max,min=setsizetype_plus_selectall(row,"i") #en este caso los return values son arreglos
			FILE+=gen_ioscript_plus_header_selectall(sizetype,label,labelto,"i",type)
			FILE+=gen_iodata_plus_selectall(now,first,row,sizetype,"i",evaluate)
			FILE+=gen_ioscript_footer_selectall(label,labelto, type,"Flows", "viz9",max,min,sizetype,id) 





	
	return FILE
def graphInt(label,labelto,id,checkbox_marked, now, first,type,evaluate):

	#An i/o graph is always just one netowkr
        #this function is called when one network, port or net2net  is chosen
        # The  port ids or net2 net connections cjhosen are stored in the checkbox_marked array
        #It recieves first and now which are the time interval for the graph
        #Evaluate indicates if it is a time interval of less than a day, a week , month or a year or more
        #id is the network id
        #title is the graph title created with the create_title function and label label to are the labels corresponding the options chosen
        FILE=""
	
	first=first-first%INCREMENT 

        now=now-now%INCREMENT
	

	

	row = IntRangeO(c,id,checkbox_marked,now,first,type)


	if row:
			    FILE+="#graph"
			    sizetype,max,min=setsizetype_selectall(row) #en este caso los return values son un hashes 
			    FILE+=gen_ioscript_header_selectall(sizetype,label,labelto,type)
			    FILE+=gen_iodata_selectall(now,first,row,sizetype,evaluate)
			    FILE+=gen_ioscript_footer_selectall(label,labelto,type, "Octects", "viz1",max,min,sizetype,id) 
	
# The I/O Packet data(24h)
	

	row= IntRangeP(c, id,checkbox_marked,now, first,type)

	if row:
			    FILE+="#graph"
			    sizetype,max,min=setsizetype_selectall(row) #en este caso los return values son arreglos
			    FILE+=gen_ioscript_header_selectall(sizetype,label,labelto,type)
			    FILE+=gen_iodata_selectall(now,first,row,sizetype,evaluate)
			    FILE+=gen_ioscript_footer_selectall(label,labelto, type,"Packet", "viz2",max,min,sizetype,id) 


# The I/O Flow data(24h)


	row = IntRangeF(c, id, checkbox_marked, now, first,type)

	if row:
			    FILE+="#graph"
			    sizetype,max,min=setsizetype_selectall(row) #en este caso los return values son arreglos
			    FILE+=gen_ioscript_header_selectall(sizetype,label,labelto,type)
			    FILE+=gen_iodata_selectall(now,first,row,sizetype,evaluate)
			    FILE+=gen_ioscript_footer_selectall(label, labelto,type,"Flows", "viz3",max,min,sizetype,id) 
			

# The I/O network, packet, flow(24h)


	row = IntRangeAll(c, id, checkbox_marked,now, first,type)
	if row :
	
			    FILE+="#graph"
			    sizetype_array=setsizetype_all_selectall(row) # en este caso el return value es un una lsita de 2 dimensiones
               		    FILE+= gen_ioascript_header_selectall(sizetype_array,label,labelto,type)
	               	    FILE+=gen_ioadata_selectall( now, first,row ,sizetype_array,evaluate )
			    FILE+=gen_ioascript_footer_selectall(label,labelto, type,"viz4",id)
	


	
	return FILE
###################################################################	

def check_earliest(first,checkbox_options,type,id):
###This function checks if the time given is before the database started recording data
## If thats the case it returns 0 and if not it returns 1  
#If the type is io it checks the earliest time for that network
#Else it checks the minimun from the earliest times of the optionc checked in the form
#if the first value is less than the earliest timefound in the database it returns 0
	earliest=[]
	
	if type=="i/o":
		sql="""select time_unix from rrd_n where nid=%s order by time_unix asc  limit 1"""%(id)
		c.execute(sql)
		m=c.fetchone()[0]
		if first < m:
			
			return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(m))
	else:
		if type=="port":
			sql="""select time_unix from rrd_port where pid="""
		else:
			sql="""Select time_unix from rrd_to_net where nn_id="""
	
		for i in range(len(checkbox_options)):
			c.execute(sql+ """ %s order by time_unix asc  limit 1"""%(checkbox_options[i]))
			try:
				earliest.append(c.fetchone()[0])
			except:
				
				earliest.append(0) # si no hay nada de data despliega la otra y a esta le pone 0 



		for i in earliest: 
			if first <  i:
			
				return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(max(earliest)))
				
	
	return 1


def checkdate(form,label,labelto,type,id,checkbox_marked):
#This function verifies the time interval for the graph is valid. If it is it calls the grapher function, if not it displays an error
#It receives the form containing the user's input, the label of the network, type which specifie sif it is i/o, port or net2net , the id of the network and label, and an array checkbox_marked (if type is i/o this variable is 0), that contains the checkbox marked in the form


	current_time=int(time.time())
        #converts the time in the form to unix time (make another function of this when possible)
	if form.has_key("d2") and form.has_key("d1"):
		first= form.getfirst("d1")#get first gets the first input therefore avoiding anything after a ; character
		now = form.getfirst("d2")
                if  re.match("\d\d\d\d-\d\d-\d\d\s\d\d:\d\d:\d\d$",first) !=None and  re.match("\d\d\d\d-\d\d-\d\d\s\d\d:\d\d:\d\d$",now)!=None:#reasure valid input

		    first=time.strptime(first,"%Y-%m-%d %H:%M:%S")
		    first=time.mktime(first)

		    now =time.strptime(now,"%Y-%m-%d %H:%M:%S")
		    now=time.mktime(now)
		    now=int(now)
		    first=int(first)


		    e_interval=now-first
                #The next if and else use the time interval calculated to determine if we are going to graph on a daily scale, weekly, monthly or yearly
                #This is used so the grapher knows how to avarege the data.

		    if e_interval>=604800 and e_interval<2629743:
		        	evaluate="W" 
		    elif e_interval>=2629743 and e_interval<31556926:
		        	evaluate="M"
		    elif e_interval>=31556926:
		        	evaluate="Y"
		    else:
		        	evaluate="D"
				
    		    earliest=check_earliest(first,checkbox_marked,type,id) #this function checks if there is any data for the time when the interval begins
                    #If there is no data recorded because the user is asking for a time interval that started before data started being store, an error notice is given
		    if earliest!=1: #if the previous function returns false this is executed
			
       		        	graphs=""" ERROR: The database has no record of that time period. This query can be executed after %s  """%(earliest)
		    elif first>current_time   or now>current_time  :#If the time in first or the time specified in now is in the future generate an error
       		 	    graphs="""ERROR: Graphing and visualizing the future is currently not supported"""
		    elif  first<=now-600 :#If the interval is correct 

			    if checkbox_marked==0:# If the user chose the i/o option, no checkboxes where marked therefore it is 0 
				
				graphs = graphInt(label,labelto, id,checkbox_marked, now, first,type,evaluate)
			    elif len(checkbox_marked) <=1:  
				graphs = graphInt(label,labelto, id,checkbox_marked, now, first,type,evaluate)
			    else: #if multiple networks where chosen a different graphing scheme is used 
				graphs = graphInt_plus(label,labelto, id,checkbox_marked, now, first,type,evaluate)
		    elif first>now-600 and first<=now :# El intervale es menor o igual a 5 minutos por lo que no hay data si es de presente o si es de una fecha pasada solo hay un punto 
                   #If the interval is  is equal or less than the cron time  we generate an error because either there is no data or it results in only one point in the graph.

        		graphs="""ERROR: The time interval is to short ,it must be at least 10+ minutes"""
		    elif first>now:
	
        		graphs="""ERROR:  The first input must be a time  before the second input"""

		    else:#If something unexpected happens
 	
        		graphs="""ERROR: Oops!! Unkown Error"""

                else:
        		graphs="""ERROR:The time field contains a non valid input"""
	else:
		graphs="ERROR: no time was chosen\n"
        print graphs





#########################################################################
######################### Main #########################################
######################################################################

form = cgi.FieldStorage()

print "Content-Type: text/html\n\n"
print 

if (validate(form)!=1):
	print "ERROR: You must be logged in to use this feature\n"
	exit(1)

if form.has_key("id"):
	id=form.getfirst('id')
	if (re.match("(\d)+$",id)!=None) :
		id = int(id)
	else:
		print "ERROR: id is not a valid input\n"
		exit(1)

else :
	print "ERROR: No network was chosen \n"
	exit(1)

if form.has_key("graphtype"):
      	type=form.getfirst("graphtype")
	
        if re.match("(port|p2p|i/o)$", type) == None:  
		print "ERROR: type is not a valid input"
		exit(1)
#type es el de donde viene la data si del network, port o p2p
else:
	print "ERROR: no graph type was chosen\n"
	exit(1)

	

if type!="i/o":
	if form.has_key("checkbox_marked"):
		
                checkbox_marked = form.getvalue("checkbox_marked")
                if isinstance(checkbox_marked, basestring): #if it is a string meaning that only one box was selected (done to avoid iterating over a string)
		       	if (re.match("(\d)+$",checkbox_marked)!=None) :
                        	cm=[int(checkbox_marked)]
                        	checkbox_marked=cm
			else:
				print "ERROR: checkbox_marked is not a valid input"
                else:
                    for i in range(len( checkbox_marked)):#lo convierto a int por que com se recibe la lista por el form esta en string
		       	if (re.match("(\d)+$",checkbox_marked[i])!=None) :
				checkbox_marked[i]=int(checkbox_marked[i])
			else:
				
				print "ERROR: checkbox_marked is not a valid input"
				exit(1);
		label,labelto=GetLabel(c,type,id,checkbox_marked)
                #print checkbox_marked
                #print label,labelto
		checkdate(form,label,labelto,type,id,checkbox_marked)
	
	else:# and  type !="i/o":#if checkbox are empty but it is still port or p2p
		
        		print""" ERROR: No option was chosen"""
else:

	
	checkbox_marked=0
	label,labelto=GetLabel(c,type,id,checkbox_marked)

	checkdate(form,label,labelto,type,id,checkbox_marked)


