
#This script is in charge of creating the graph files that are stored in /var/www/js/graphs and are displayed in the page. These functions are called from flowsgrapher.py located in /opt/nap/bin/ 

import MySQLdb
import time
from functions import *
from QueryBuilder import *
from os.path import join as pjoin
import sys
from Config import Config
config=Config()
DB_NAME=config.getDBName();
DB_HOST='localhost'
DB_USER=config.getUser();
DB_PASS=config.getPassword();

INCREMENT=config.getCronTime()

#sets the number that the time is going to be modulated by
interval_modulation=INCREMENT 
db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
c = db.cursor()



#this function sets the type of size (MB,GB,KB...) that the data is. This is done to resize them on the graph propperly .
# It its specifically for the graph that displays all because it sizetype is an array that will hold the sizes of the octects,flows, and packets. 
#It receives row which is an array that contains all the data, and sizetype which is the array that is going to be modified and returned 
#Does not return the max because in the "all" graph that is not dispayed 
def setsizetype_all(row,sizetype):
        max=[0,0,0]


        if len(row) >0:

                for i in range (len(row)):
                        t=0
                        for m in range (len(max)):
                                if max[m] <row[i][t]:
                                        max[m]=row[i][t]
                                if max[m] <row[i][t+1]:
                                        max[m]=row[i][t+1]
                                t+=2

                for i in range(len(max)):

                        if max[i] >= 1073741824:
                                sizetype[i]="GB"
                        elif max[i] >= 1048576:
                                sizetype[i]="MB"
                        elif max[i] >= 1024:
                                sizetype[i]="KB"
                        else:
                                sizetype[i]="bytes"
                return sizetype

#this function sets the type of size (MB,GB,KB...) that the data is and returns it in the variable sizetype.  
# It its specifically for the individual graphs that display octects or packets or flows
#It receives row which is an array that contains all the data                                                                           
# It returns the max and min of the data 
def setsizetype (row,sizetype):
	max=0;
	min=0; 	
	sizetype="bytes"
	
	# If row has elements (If there is data in the database) 
	if len(row) > 0:
		max=row[0][0]
		min=row[0][1]
		for m in range(len(row)):
			if max<row[m][0]:
				max=row[m][0]
			if max <row[m][1]:
				max=row[m][1]
			if min>row[m][0]:
				min=row[m][0]
			if min >row[m][1]:
				min=row[m][1]
	       
                if max >= 1073741824:
                       sizetype = "GB"
                elif max >= 1048576:
                       sizetype = "MB"
                elif max >= 1024:
                       sizetype = "KB"
		
	return sizetype,max,min;	

# This function is for the individual graphs
# This function writes the headers for the graphs. 
#It receives fd which is the pointer to the file and sizetype indicating the size of the data 
def gen_ioscript_header(fd,sizetype):
	fd.write(("""
        // Create and populate the data table.
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'date');
        data.addColumn('string', 'x');
        data.addColumn(\'number\', \'Input %s \');
        data.addColumn(\'number\', \'Output %s \');""")%(sizetype,sizetype))
	
# This function is for the "all" graphs
# This function writes the headers for the graphs. 
#It receives fd which is the pointer to the file and sizetype indicating the size of the data 
def gen_ioascript_header(fd,sizetype):
	fd.write("""
        // Create and populate the data table.
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'date');
        data.addColumn('string', 'x');
        data.addColumn(\'number\', \'Octects Input %s \');
        data.addColumn(\'number\', \'Octects Output  %s\');
        data.addColumn(\'number\', \'Packets Input  %s \');
        data.addColumn(\'number\', \'Packets Output %s \');
        data.addColumn(\'number\', \'Flows Input %s \');
        data.addColumn(\'number\', \'Flows Output %s \');""" %(sizetype[0],sizetype[0],sizetype[1],sizetype[1],sizetype[2],sizetype[2]))
	
	

# This function writes the data columns for the graphs
# It receives the file pointer (fd), the current unix time(now), the starting point to plot the graph (first) , the sizetype of the data (sizetype)
# the data (row) and evaluate which indicates if its a graph of data,month,week or year
def gen_iodata(fd, now, first, sizetype, row, evaluate, type=None):

        #Set  the increments of time in the graph for each point, 
	if evaluate == "D":
		sumador = INCREMENT
	elif evaluate == "S":
		sumador = INCREMENT*6
	elif evaluate == "M":
		sumador = INCREMENT * 24
	elif evaluate == "A":
		sumador = INCREMENT * 288
	
	data1=0.00
	data2=0.00

	limit=first+sumador
	counter=0
	typediv=1

        # Depending on the sizetype the typediv is set and then used to divide and scale the data
	if sizetype=="KB":
		typediv=1024.0
	elif sizetype=="MB":
		typediv=1048576.0
	elif sizetype=="GB":
		typediv=1073741824.0

	i = 0 
	#variable that will hold the timstamp 
	time_graph = 0
	



	# loops while the the starting point hasnt reached the current time which is when the graph ends
	while first <= now: 
		# limit represents the end of the interval of data that is going to create a single point in the graph.
		while first < limit: 
	


			# if the counter is in the sizeof the array and the timestamp in the database correspons to the time whre the graph is going to put it
    			# The row[i][2]-(row[i][2]%INCREMENT  is jsut in case the data point in the array does not contain a time stamp that falls in the correct  increments
	                if  i < len(row) and first==(row[i][2]-(row[i][2]%INCREMENT)): 
				data1=data1 + row[i][0]
				data2=data2 + row[i][1]
				
					
				
				time_graph = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(first))
	                        i+=1
	                        
	                else:
                                # if the times do not match or the counter is bigger then the array (which means the time of the graph has exceeded the amount of data available, then we just put 0
				data1=data1 + 0
				data2=data2 + 0
				time_graph = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(first))
			first+=INCREMENT  
			counter=counter+1
		
		#averages the data out, if in the graph a single day then counter will be 1
		avgdata1=data1/counter
		avgdata2=data2/counter
	 
		timedisplay=time_graph.split("-")
                # Sets the time stamp to be display in the graph, if its a day, then it only displays the hours, if its a week then it displays the das and the hour and so on 
		if evaluate=="D":

			split_time=timedisplay[2].split(" ")
			fd.write(""" data.addRow(["'%s'","'%s'",%.2f, %.2f]); """ % (split_time[1],time_graph, avgdata1/typediv, avgdata2/typediv))
		
		elif evaluate=="S":
			
			fd.write(""" data.addRow(["'%s'", "'%s'",%.2f, %.2f]); """ % (timedisplay[2], time_graph,avgdata1/typediv, avgdata2/typediv))
		elif evaluate=="M":
			
			fd.write(""" data.addRow([ "'%s'","'%s'",%.2f, %.2f]); """ % (timedisplay[1]+" "+timedisplay[2], time_graph,avgdata1/typediv, avgdata2/typediv))

		else:	
			
			fd.write(""" data.addRow(["'%s'", "'%s'",%.2f, %.2f]); """ % (time_graph, time_graph, avgdata1/typediv, avgdata2/typediv))


		counter=0
		# Once first reaches limit we increment the limit again, and start a new loop in a new interval that is going to correpond to a point in the graph
	        limit=limit+sumador 
                
		# reset data to 0 so it doesnt affect the avareges of the new interval/point in graph
		data1=data2=0 

# This function writes the data columns for the " all" graph
# It receives the file pointer (fd), the current unix time and end point (now), the starting point of the graph (first) 
# the sizetype for all the data (sizetype), the data (row), and evaluate which indicates if its a graph of data,month,week or year
def gen_ioadata(fd, now, first,sizetype,row, evaluate, type=None):


        #Set  the increments of time in the graph for each point, 

	if evaluate == "D":
		sumador = INCREMENT
	elif evaluate == "S":
		sumador = 1800
	elif evaluate == "M":
		sumador = 7200
	elif evaluate == "A":
		sumador = 86400
 	# We hace six data points for the inputs and outputs of the octects, packets and flows	
	data1=0.0
	data2=0.0
	data3=0.0
	data4=0.0
	data5=0.0
	data6=0.0
	limit=first+sumador
	counter=0

	graph_data = ""
	i = 0
	

	typediv=[1,1,1]

        for i in range(len(sizetype)): #loops through each of the inputs and outputs of the 3 types of data (o,p and f) 	
		if sizetype[i]=="KB":
			typediv[i]=1024.0
		elif sizetype[i]=="MB":
			typediv[i]=1048576.0
		elif sizetype[i]=="GB":
			typediv[i]=1073741824.0

	# loops while the the starting point hasnt reached the current time which is when the graph ends
        while row and first <= now: 
		# limit represents the end of the interval of data that is going to create a single point in the graph.
		while first < limit: 


			if  i < len(row) and first==(row[i][6] -(row[i][6]%INCREMENT)):
                             # row[i][2]-(row[i][2]%INCREMENT) is in case the data point in the array does not contain a time stamp that falls in the correct interval
                                data1=data1 + row[i][0]
                                data2=data2 + row[i][1]
                                data3=data3 + row[i][2]
                                data4=data4 + row[i][3]
                                data5=data5 + row[i][4]
                                data6=data6 + row[i][5]
                                i+=1
				
				time_graph = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(first))
                        else:
                                 # if the times do not match or the counter is bigger then the array then we just put 0

                                data1=data1 + 0
                                data2=data2 + 0
                                data3=data3 + 0
                                data4=data4 + 0
                                data5=data5 + 0
                                data6=data6 + 0
				time_graph = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(first))
		
			first+=INCREMENT
			counter=counter+1
                #averages the data out, if in the graph a single day then counter will be 1

		#avgdata es el promedio de la data calculado
		avgdata1=data1/counter
		avgdata2=data2/counter
		avgdata3=data3/counter
		avgdata4=data4/counter
		avgdata5=data5/counter
		avgdata6=data6/counter
		timedisplay=time_graph.split("-")
                if evaluate=="D":

                        split_time=timedisplay[2].split(" ")
	
			fd.write(""" data.addRow(["'%s'","'%s'", %.2f, %.2f, %.2f, %.2f, %.2f, %.2f]); """ % (split_time[1], time_graph,avgdata1/typediv[0], avgdata2/typediv[0], avgdata3/typediv[1],avgdata4/typediv[1],avgdata5/typediv[2],avgdata6/typediv[2]))
             	elif evaluate=="S":
			fd.write(""" data.addRow(["'%s'", "'%s'",%.2f, %.2f, %.2f, %.2f, %.2f, %.2f]); """ % (timedisplay[1], time_graph,avgdata1/typediv[0], avgdata2/typediv[0], avgdata3/typediv[1],avgdata4/typediv[1],avgdata5/typediv[2],avgdata6/typediv[2]))

		elif evaluate=="M":
			fd.write(""" data.addRow(["'%s'", "'%s'",%.2f, %.2f, %.2f, %.2f, %.2f, %.2f]); """ % (timedisplay[1] +" "+ timedisplay[2],time_graph, avgdata1/typediv[0], avgdata2/typediv[0], avgdata3/typediv[1],avgdata4/typediv[1],avgdata5/typediv[2],avgdata6/typediv[2]))
		else :
			  
			fd.write(""" data.addRow(["'%s'", "'%s'", %.2f, %.2f, %.2f, %.2f, %.2f, %.2f]); """ % (time_graph,time_graph, avgdata1/typediv[0], avgdata2/typediv[0], avgdata3/typediv[1],avgdata4/typediv[1],avgdata5/typediv[2],avgdata6/typediv[2]))
		counter=0
	        limit=limit+sumador
		# reset data to 0 so it doesnt affect the avareges of the new interval/point in graph
		data1=data2=data3=data4=data5=data6=0
		

#Function to write the footer of the individual graphs
#It receives fd (file object) , label is title of the graph,graphname is the name of the network the graph corresponds to, 
#type  indicates the type of the data (packets,flows,etc) ,the max and min , and the size type 
def gen_ioscript_footer(fd, label, type,graphname,max,min,sizetype):
	

        # sets the number to be divided to scale down the data with the sizetype (NOTE: remember to turn this into a function)
        if sizetype=="KB":
                typediv=1024.0
        elif sizetype=="MB":
                typediv=1048576.0
        elif sizetype=="GB":
                typediv=1073741824.0
	else:
		typediv=1

        if min >= 1073741824:
                minlabel = "%.2f GB" % (min / 1073741824.0)
        elif min >= 1048576:
                minlabel = "%.2f MB" % (min / 1048576.0)
        elif min >= 1024:
                minlabel = "%.2f KB" % (min / 1024.0)
        else:
                minlabel = "%.2f bytes" % min 

        fd.write("""

	var graphtitle='%s Traffic %s Max: %.2f %s Min: %s'
	var xtitle='Time'
	var ytitle='%s'
	var maxvalue='%s'

	
        
      
	""" % (label, type,max/typediv,sizetype,minlabel, type, int(max/typediv)))



#Function to write the footer of the "all"  graph
# It receives fd which is the poibnter to the file, label which is the title of the graph,  graphname  which is the name  of the network the graph corresponds to
def gen_ioascript_footer(fd, label, graphname): 

        
	fd.write("""
	    var graphtitle="%s Net Traffic ";
	    var xtitle='Time';
            var ytitle='All'
            
	
	    """ % (label))	

###################################Functions called from the flowsgrapher.py script that use the functions defined above ###################################

# This function (called from flowsgrapher.py , is responsible from generating the graph file for the 24 hour single network graphs that contain the octect,packets,flows and "all" graphs, 
# This function receives , the current unix time, the title of the graph in label, the id of the network and th path where it is going to be written 
def graphInt24h(now, label, id, path):

        
    db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
    c = db.cursor()
    #object to use the functions defined in QueryBuilder.py  to retreive data from the database 
    qb = QueryBuilder()
	
    FILE1=open(pjoin(path, label+ "_1dnet.js"), "w")

    # writes a file  on /var/www/js/graphs with the name  "label"_1d.html

    FILE2=open(pjoin(path, label+ "_1dpak.js"), "w")

    # writes a file  on /var/www/js/graphs with the name  "label"_1d.html

    FILE3=open(pjoin(path, label+ "_1dflw.js"), "w")

    # writes a file  on /var/www/js/graphs with the name  "label"_1d.html

    FILE4=open(pjoin(path, label+ "_1dcpl.js"), "w")

    # writes a file  on /var/www/js/graphs with the name  "label"_1d.html

    sizetype="bytes"
    sizetype_array=["bytes","bytes","bytes"]

    #first is initialized by substracting 24 hours in unix time to our current unix time
    first=now-86400 


# The I/O Network data (24h)
	
    row = qb.IntRangeO(c, id, now, first) #Gets the dara from the database
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE1,sizetype)
    gen_iodata(FILE1, now, first, sizetype, row, "D")
    gen_ioscript_footer(FILE1, label, "Network", "viz1",max,min,sizetype) 

	
# The I/O Packet data(24h)
		
    row = qb.IntRangeP(c, id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE2,sizetype)

    gen_iodata(FILE2, now, first,sizetype,row, "D")
    gen_ioscript_footer(FILE2, label, "Packet", "viz2",max,min,sizetype) 

# The I/O Flow data(24h)

	
    row = qb.IntRangeF(c, id, now, first)
		
    sizetype,max,min=setsizetype(row,sizetype)
		
    gen_ioscript_header(FILE3,sizetype)

    gen_iodata(FILE3, now, first,sizetype, row, "D")
    gen_ioscript_footer(FILE3, label, "Flows", "viz3",max,min,sizetype) 

# The I/O network, packet, flow(24h)
    row = qb.IntRangeAll(c, id, now, first)
	
    sizetype_array=setsizetype_all(row,sizetype_array)
    gen_ioascript_header(FILE4,sizetype_array)
    gen_ioadata(FILE4, now, first,sizetype_array,row, "D")
    gen_ioascript_footer(FILE4, label, "viz4")
	




    c.close()
##################################################################	
# This function (called from flowsgrapher.py , is responsible from generating the graph file for the 1  week  single network graphs that contain the octect,packets,flows and "all" graphs, 
# This function receives , the current unix time, the title of the graph in label, the id of the network and th path where it is going to be written 
def graphInt1s(now, label, id, path):

    qb = QueryBuilder()
        
    db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
    c = db.cursor()

    FILE1=open(pjoin(path,label+ "_1wnet.js"), "w")
     
    FILE2=open(pjoin(path,label+ "_1wpak.js"), "w")
     
    FILE3=open(pjoin(path,label+ "_1wflw.js"), "w")
     
    FILE4=open(pjoin(path,label+ "_1wcpl.js"), "w")
     
    first=now-604800

    sizetype_array=["bytes","bytes","bytes"]
    sizetype="bytes"

	#The I/O Network data (1s)
	
    row = qb.IntRangeO(c, id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE1,sizetype)
    gen_iodata(FILE1, now, first,sizetype, row, "S")
    gen_ioscript_footer(FILE1, label, "Network", "viz1",max,min,sizetype) 
	
	#The I/O Packet data (1s)
	
    row = qb.IntRangeP(c, id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE2,sizetype)
    gen_iodata(FILE2, now, first,sizetype, row, "S")
    gen_ioscript_footer(FILE2, label, "Packets", "viz2",max,min,sizetype) 

	#The I/O Flows data(1s)

	
    row = qb.IntRangeF(c, id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE3,sizetype)
    gen_iodata(FILE3, now, first, sizetype,row, "S")
    gen_ioscript_footer(FILE3, label, "Flows", "viz3",max,min,sizetype) 
   
	#The I/O Network,Packets, Flows (1s)
	
    row = qb.IntRangeAll(c, id, now, first)
    sizetype_array=setsizetype_all(row,sizetype_array)
    gen_ioascript_header(FILE4,sizetype_array)
    gen_ioadata(FILE4, now, first,sizetype_array, row, "S")
    gen_ioascript_footer(FILE4, label, "viz4")
	
     

     

     

     

    c.close()
#######################################################################################

# This function (called from flowsgrapher.py , is responsible from generating the graph file for the 1  month  single network graphs that contain the octect,packets,flows and "all" graphs, 
# This function receives , the current unix time, the title of the graph in label, the id of the network and th path where it is going to be written 
def graphInt1m(now, label, id, path):

    qb = QueryBuilder()
        
    db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
    c = db.cursor()

    FILE1=open(pjoin(path,label+ "_1mnet.js"), "w")
     
    FILE2=open(pjoin(path,label+ "_1mpak.js"), "w")
     
    FILE3=open(pjoin(path,label+ "_1mflw.js"), "w")
     
    FILE4=open(pjoin(path,label+ "_1mcpl.js"), "w")
     

    first=now-2419200
	
    sizetype_array=["bytes","bytes","bytes"]
    sizetype="bytes"
    # The I/O Network (1m)
	
    row = qb.IntRangeO(c, id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE1,sizetype)
    gen_iodata(FILE1, now, first, sizetype,row, "M")
    gen_ioscript_footer(FILE1, label, "Network", "viz1",max,min,sizetype) 
	


       # The I/O Packets (1m)
	
    row = qb.IntRangeP(c, id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE2,sizetype)
    gen_iodata(FILE2, now, first, sizetype,row, "M")
    gen_ioscript_footer(FILE2, label, "Packets", "viz2",max,min,sizetype) 

	# The I/O Flows (1m)
	
    row = qb.IntRangeF(c, id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE3,sizetype)
    gen_iodata(FILE3, now, first, sizetype,row, "M")
    gen_ioscript_footer(FILE3, label, "Flows", "viz3",max,min,sizetype) 
	

	# The I/0 Network,Packets,Flows (1m), "M"
	
	
    row = qb.IntRangeAll(c, id, now, first)
    sizetype_array=setsizetype_all(row,sizetype_array)
    gen_ioascript_header(FILE4,sizetype_array)
    gen_ioadata(FILE4, now, first,sizetype_array, row, "M")
    gen_ioascript_footer(FILE4, label, "viz4")
	#FILE.write(graph_content)
     
     
     
     

    c.close()
##################################################################################

# This function (called from flowsgrapher.py , is responsible from generating the graph file for the 1  year  single network graphs that contain the octect,packets,flows and "all" graphs, 
# This function receives , the current unix time, the title of the graph in label, the id of the network and th path where it is going to be written 
def graphInt1a(now, label, id, path):

    db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
    c = db.cursor()
    FILE1=open(pjoin(path,label+ "_1anet.js"), "w")
     
    FILE2=open(pjoin(path,label+ "_1apak.js"), "w")
     
    FILE3=open(pjoin(path,label+ "_1aflw.js"), "w")
     
    FILE4=open(pjoin(path,label+ "_1acpl.js"), "w")
     
    
    first=now-29030400
    sizetype="bytes"
    sizetype_array=["bytes","bytes","bytes"]

	# The I/0 Network (1a)

    qb = QueryBuilder()

		
    row = qb.IntRangeO(c, id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE1,sizetype)
    gen_iodata(FILE1, now, first, sizetype,row, "A")
    gen_ioscript_footer(FILE1, label, "Network" , "viz1",max,min,sizetype) 
	
	# The I/0 Packets (1a)
	
	
    row = qb.IntRangeP(c, id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE2,sizetype)
    gen_iodata(FILE2, now, first, sizetype,row, "A")
    gen_ioscript_footer(FILE2, label, "Packets" , "viz2",max,min,sizetype) 
	
	# The I/0 Flows (1a)
	
    row = qb.IntRangeF(c, id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE3,sizetype)	
    gen_iodata(FILE3, now, first, sizetype,row, "A")
    gen_ioscript_footer(FILE3, label, "Flows" , "viz3",max,min,sizetype) 

	# The Network,Packets,Flows (1a)
	
	
   	
    row = qb.IntRangeAll(c, id, now, first)
    sizetype_array=setsizetype_all(row,sizetype_array)
    gen_ioascript_header(FILE4,sizetype_array)
    gen_ioadata(FILE4, now, first, sizetype_array,row, "A")
    gen_ioascript_footer(FILE4, label, "viz4")

     
     
     
     

    c.close()
################################## PORT GRAPHS ##################################################


# This function (called from flowsgrapher.py , is responsible from generating the graph file for the 24 hour port  graphs that contain the octect,packets,flows and "all" graphs, 
# This function receives the unix time, the title of the graph (label),the name of the network  (nlabel) the id of the port in the database and the path where it is going to be written 
def graphPort24h(now, nlabel, label, id, path):

    label=str(label)
    db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
    c = db.cursor()
    qb = QueryBuilder()
    FILE1=open(pjoin(path,"%s-p%s_1dnet.js") % (nlabel, label), "w") # the name of the file is "name of network"-"port number"_1.d.js 
     
    FILE2=open(pjoin(path,"%s-p%s_1dpak.js") % (nlabel, label), "w") # the name of the file is "name of network"-"port number"_1.d.html
     
    FILE3=open(pjoin(path,"%s-p%s_1dflw.js") % (nlabel, label), "w") # the name of the file is "name of network"-"port number"_1.d.html
     
    FILE4=open(pjoin(path,"%s-p%s_1dcpl.js") % (nlabel, label), "w") # the name of the file is "name of network"-"port number"_1.d.html
     
	
    first=now-86400

    sizetype="bytes"
    sizetype_array=["bytes","bytes","bytes"]
	################### The Port of Network (1d)############
	
    row = qb.PortRangeO(c, id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE1,sizetype)
    gen_iodata(FILE1, now, first, sizetype,row,"D")
    gen_ioscript_footer(FILE1, nlabel+'-'+label, "Network", "viz1",max,min,sizetype) 


	##################  The Port  Packets (1d) ###############
	
	
    row = qb.PortRangeP(c, id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE2,sizetype)
    gen_iodata(FILE2, now, first,sizetype, row,"D")
    gen_ioscript_footer(FILE2, nlabel+'-'+label, "Packets", "viz2",max,min,sizetype) 

	################# The Port  Flows (1d) ##################

     	 
	
    row = qb.PortRangeF(c, id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE3,sizetype)
    gen_iodata(FILE3, now, first, sizetype,row,"D")
    gen_ioscript_footer(FILE3, nlabel+'-'+label, "Flows", "viz3",max,min,sizetype) 

	############### The Port  of Network,Packets,Flows (1d) ######
     	 
	
    row = qb.PortRangeAll(c, id, now, first)
    sizetype_array=setsizetype_all(row,sizetype_array)
    gen_ioascript_header(FILE4,sizetype_array)
    gen_ioadata(FILE4, now, first, sizetype_array,row,"D")
    gen_ioascript_footer(FILE4,nlabel+'-'+ label, "viz4")

     
     
     
     
   
    c.close()
############################################################

# This function (called from flowsgrapher.py , is responsible from generating the graph file for the 1 week  port  graphs that contain the octect,packets,flows and "all" graphs, 
# This function receives the unix time, the title of the graph (label),the name of the network  (nlabel) the id of the port in the database and the path where it is going to be written 
def graphPort1s(now,nlabel, label, id, path):
	
	
    label=str(label)

    db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
    c = db.cursor()
    qb = QueryBuilder()
   # the name of the file is "name of network"-"port number"_1.d.js 
    FILE1=open(pjoin(path,"%s-p%s_1wnet.js") % (nlabel, label), "w") 
     
    # the name of the file is "name of network"-"port number"_1.d.js
    FILE2=open(pjoin(path,"%s-p%s_1wpak.js") % (nlabel, label), "w") 
     
    # the name of the file is "name of network"-"port number"_1.d.js
    FILE3=open(pjoin(path,"%s-p%s_1wflw.js") % (nlabel, label), "w") 
     
   # the name of the file is "name of network"-"port number"_1.d.js
    FILE4=open(pjoin(path,"%s-p%s_1wcpl.js") % (nlabel, label), "w") 
     
    first=now-604800

    sizetype_array=["bytes","bytes","bytes"]
    sizetype="bytes"
	
	######s############# The Port  of Network (1s)###############

	
	
    row = qb.PortRangeO(c, id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE1,sizetype)
    gen_iodata(FILE1, now, first, sizetype,row,"S")
    gen_ioscript_footer(FILE1, nlabel+'-'+label, "Network", "viz1",max,min,sizetype) 
	##################  The Port  Packets (1s) ###############
	
	
    row = qb.PortRangeP(c, id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE2,sizetype)
    gen_iodata(FILE2, now, first,sizetype, row,"S")
    gen_ioscript_footer(FILE2, nlabel+'-'+label, "Packets", "viz2",max,min,sizetype) 

	################# The Port  Flows (1s) ##################

     	 
	
    row = qb.PortRangeF(c, id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE3,sizetype)
    gen_iodata(FILE3, now, first, sizetype,row,"S")
    gen_ioscript_footer(FILE3, nlabel+'-'+label, "Flows", "viz3",max,min,sizetype) 
	############### The Port  of Network,Packets,Flows (1d) ######
     	 
	
    row = qb.PortRangeAll(c, id, now, first)
    sizetype_array=setsizetype_all(row,sizetype_array)
    gen_ioascript_header(FILE4,sizetype_array)
    gen_ioadata(FILE4, now, first, sizetype_array,row,"S")
    gen_ioascript_footer(FILE4, nlabel+'-'+label, "viz4")

     
     
     
     


    c.close()
# This function (called from flowsgrapher.py , is responsible from generating the graph file for the 1 month port  graphs that contain the octect,packets,flows and "all" graphs, 
# This function receives the unix time, the title of the graph (label),the name of the network  (nlabel) the id of the port in the database and the path where it is going to be written 
def graphPort1m(now,nlabel, label, id, path):
    
    label=str(label)
	
    db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
    c = db.cursor()
    qb = QueryBuilder()
# the name of the file is "name of network"-"port number"_1.d.js 
    FILE1=open(pjoin(path,"%s-p%s_1mnet.js") % (nlabel, label), "w") 
     
    FILE2=open(pjoin(path,"%s-p%s_1mpak.js") % (nlabel, label), "w") 
     
    FILE3=open(pjoin(path,"%s-p%s_1mflw.js") % (nlabel, label), "w") 
     
    FILE4=open(pjoin(path,"%s-p%s_1mcpl.js") % (nlabel, label), "w") 
     
        
    first=now-2419200
	
    sizetype_array=["bytes","bytes","bytes"]
    sizetype="bytes"
	
	################### The Port  of Network (1m)###############

	
	
    row = qb.PortRangeO(c, id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE1,sizetype)
    gen_iodata(FILE1, now, first, sizetype,row,"M")
    gen_ioscript_footer(FILE1, nlabel+'-'+label, "Network", "viz1",max,min,sizetype) 

	##################  The Port  Packets (1m) ###############
	
	
    row = qb.PortRangeP(c, id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE2,sizetype)
    gen_iodata(FILE2, now, first, sizetype,row,"M")
    gen_ioscript_footer(FILE2, nlabel+'-'+label, "Packets", "viz2",max,min,sizetype) 

	################# The Port  Flows (1m) ##################

     	 
	
    row = qb.PortRangeF(c, id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE3,sizetype)
    gen_iodata(FILE3, now, first, sizetype,row,"M")
    gen_ioscript_footer(FILE3, nlabel+'-'+label, "Flows", "viz3",max,min,sizetype) 

	############### The Port  of Network,Packets,Flows (1d) ######
     	 
	
    row = qb.PortRangeAll(c, id, now, first)
    sizetype_array=setsizetype_all(row,sizetype_array)
    gen_ioascript_header(FILE4,sizetype_array)
    gen_ioadata(FILE4, now, first,sizetype_array, row,"M")
    gen_ioascript_footer(FILE4, nlabel+'-'+label, "viz4")

	
     
     
     
     


    c.close()
# This function (called from flowsgrapher.py , is responsible from generating the graph file for the 1 year  port  graphs that contain the octect,packets,flows and "all" graphs, 
# This function receives the unix time, the title of the graph (label),the name of the network  (nlabel) the id of the port in the database and the path where it is going to be written 
def graphPort1a(now,nlabel, label, id, path):

    label=str(label)
	
    db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
    c = db.cursor()
    qb = QueryBuilder()

     # the name of the file is "name of network"-"port number"_1.d.js 
    FILE1=open(pjoin(path,"%s-p%s_1anet.js") % (nlabel, label), "w") 
     
    FILE2=open(pjoin(path,"%s-p%s_1apak.js") % (nlabel, label), "w") 
     
    FILE3=open(pjoin(path,"%s-p%s_1aflw.js") % (nlabel, label), "w") 
     
    FILE4=open(pjoin(path,"%s-p%s_1acpl.js") % (nlabel, label), "w") 
     
	
    first=now-29030400
	
    sizetype_array=["bytes","bytes","bytes"]
    sizetype="bytes"

	   # The Port  Network (1a)

        
    row = qb.PortRangeO(c, id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE1,sizetype)
    gen_iodata(FILE1, now, first, sizetype,row, "A")
    gen_ioscript_footer(FILE1, nlabel+'-'+label, "Network" , "viz1",max,min,sizetype) 

        # The Port Packets (1a)

        
    row = qb.PortRangeP(c, id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE2,sizetype)
    gen_iodata(FILE2, now, first, sizetype,row, "A")
    gen_ioscript_footer(FILE2, nlabel+'-'+label, "Packets" , "viz2",max,min,sizetype) 

        # The Port Flows (1a)
        
    row = qb.PortRangeF(c, id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE3,sizetype)
    gen_iodata(FILE3, now, first, sizetype,row, "A")
    gen_ioscript_footer(FILE3, nlabel+'-'+label, "Flows" , "viz3",max,min,sizetype) 

        # The Network,Packets,Flows (1a)

        
    row = qb.PortRangeAll(c, id, now, first)
    sizetype_array=setsizetype_all(row,sizetype_array)
    gen_ioascript_header(FILE4,sizetype_array)
    gen_ioadata(FILE4, now, first, sizetype_array,row, "A")
    gen_ioascript_footer(FILE4, nlabel+'-'+label, "viz4")
#######################################
     
     
     
     

    c.close()    
##################### Point 2 Point graphs ############################

# This function (called from flowsgrapher.py , is responsible from generating the graph file for the 24 hour Point to Point/Net 2 Net  graphs that contain the octect,packets,flows and "all" graphs, 
# This function receives the unix time, the title of the graph (to_label),the name of the network  (nlabel) the id of the port in the database and the path where it is going to be written 
def graphP2P24h(now,nlabel, nn_id, to_label, path):

	
    db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
    c = db.cursor()
    qb = QueryBuilder()
    FILE1=open(pjoin(path,"%s_%s_1dnet.js")%(nlabel, to_label), "w") #The file will be named "source"_"destination"_1d.js
     
    FILE2=open(pjoin(path,"%s_%s_1dpak.js")%(nlabel, to_label), "w") #The file will be named "source"_"destination"_1d.html
     
    FILE3=open(pjoin(path,"%s_%s_1dflw.js")%(nlabel, to_label), "w") #The file will be named "source"_"destination"_1d.html
     
    FILE4=open(pjoin(path,"%s_%s_1dcpl.js")%(nlabel, to_label), "w") #The file will be named "source"_"destination"_1d.html
     
		
    first=now-86400
    sizetype="bytes"
    sizetype_array=["bytes","bytes","bytes"]

	################ P2P  Network(1d)#################
		
        
    row = qb.ToNetRangeO(c, nn_id,now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE1,sizetype)
    gen_iodata(FILE1, now, first, sizetype,row, "D")
    gen_ioscript_footer(FILE1, nlabel+' to '+to_label, "Network","viz1",max,min,sizetype) 
	
	############  P2P Packets (1d) ###################

	 
       
    row = qb.ToNetRangeP(c, nn_id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE2,sizetype)
    gen_iodata(FILE2, now, first, sizetype,row, "D")
    gen_ioscript_footer(FILE2, nlabel+' to '+to_label,"Packets", "viz2",max,min,sizetype) 

	############ P2P Flows (1d) ##################

	
        
    row = qb.ToNetRangeF(c, nn_id, now, first)
	

    sizetype,max,min=setsizetype(row,sizetype)
	
		
    gen_ioscript_header(FILE3,sizetype)
    gen_iodata(FILE3, now, first, sizetype,row, "D")
    gen_ioscript_footer(FILE3, nlabel+' to '+to_label,"Flows", "viz3",max,min,sizetype) 

	######### P2P Network,Packets,Flows (1d) ##########
	
	
        
    row = qb.ToNetRangeAll(c, nn_id, now, first)
    sizetype_array=setsizetype_all(row,sizetype_array)
    gen_ioascript_header(FILE4,sizetype_array)
	
    gen_ioadata(FILE4, now, first, sizetype_array,row, "D")
    gen_ioascript_footer(FILE4, nlabel+' to '+to_label, "viz4")

	
     
     
     
     


    c.close()
# This function (called from flowsgrapher.py , is responsible from generating the graph file for the 1 week  Point to Point/Net 2 Net  graphs that contain the octect,packets,flows and "all" graphs, 
# This function receives the unix time, the title of the graph (to_label),the name of the network  (nlabel) the id of the port in the database and the path where it is going to be written 
def graphP2P1s(now,nlabel, nn_id, to_label, path):

	
    qb = QueryBuilder()

    db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
    c = db.cursor()

	#The file will be named "source"_"destination"_1d.js
    FILE1=open(pjoin(path,"%s_%s_1wnet.js")%(nlabel, to_label), "w") 
     
    FILE2=open(pjoin(path,"%s_%s_1wpak.js")%(nlabel, to_label), "w")
     
    FILE3=open(pjoin(path,"%s_%s_1wflw.js")%(nlabel, to_label), "w") 
     
    FILE4=open(pjoin(path,"%s_%s_1wcpl.js")%(nlabel, to_label), "w") 
     
	
    first=now-604800

    sizetype="bytes"
    sizetype_array=["bytes","bytes","bytes"]
	################ P2P  Network(1s)#################
		
        
    row = qb.ToNetRangeO(c, nn_id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE1,sizetype)
    gen_iodata(FILE1, now, first, sizetype,row, "S")
    gen_ioscript_footer(FILE1, nlabel+' to '+to_label, "Network","viz1",max,min,sizetype) 

	
	############  P2P Packets (1s) ###################

	 
        
    row = qb.ToNetRangeP(c, nn_id,now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE2,sizetype)
    gen_iodata(FILE2, now, first, sizetype,row, "S")
    gen_ioscript_footer(FILE2, nlabel+' to '+to_label,"Packets", "viz2",max,min,sizetype) 

	############ P2P Flows (1s) ##################

	
        
    row = qb.ToNetRangeF(c, nn_id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE3,sizetype)
    gen_iodata(FILE3, now, first, sizetype,row, "S")
    gen_ioscript_footer(FILE3, nlabel+' to '+to_label,"Flows", "viz3",max,min,sizetype) 

	######### P2P Network,Packets,Flows (1s) ##########
	
	
        
    row = qb.ToNetRangeAll(c, nn_id, now, first)
    sizetype_array=setsizetype_all(row,sizetype_array)
    gen_ioascript_header(FILE4,sizetype_array)
    gen_ioadata(FILE4, now, first, sizetype_array,row, "S")
    gen_ioascript_footer(FILE4, nlabel+' to '+to_label, "viz4")   



     
     
     
     

    c.close()               

# This function (called from flowsgrapher.py , is responsible from generating the graph file for the 1 month  Point to Point/Net 2 Net  graphs that contain the octect,packets,flows and "all" graphs, 
# This function receives the unix time, the title of the graph (to_label),the name of the network  (nlabel) the id of the port in the database and the path where it is going to be written 
def graphP2P1m(now,nlabel, nn_id, to_label, path):

	
    qb = QueryBuilder()

    db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
    c = db.cursor()
    #The file will be named "source"_"destination"_1d.js
    FILE1=open(pjoin(path,"%s_%s_1mnet.js")%(nlabel, to_label), "w") 
     
    FILE2=open(pjoin(path,"%s_%s_1mpak.js")%(nlabel, to_label), "w") 
     
    FILE3=open(pjoin(path,"%s_%s_1mflw.js")%(nlabel, to_label), "w") 
     
    FILE4=open(pjoin(path,"%s_%s_1mcpl.js")%(nlabel, to_label), "w") 
     
	
    first=now-2419200
	
    sizetype="bytes"
    sizetype_array=["bytes","bytes","bytes"]

	################ P2P  Network(1m)#################
		
        
    row = qb.ToNetRangeO(c, nn_id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE1,sizetype)
    gen_iodata(FILE1, now, first, sizetype,row, "M")
    gen_ioscript_footer(FILE1, nlabel+' to '+to_label ,"Network","viz1",max,min,sizetype) 

	
	############  P2P Packets (1m) ###################

	 
        
    row = qb.ToNetRangeP(c, nn_id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE2,sizetype)
    gen_iodata(FILE2, now, first, sizetype,row, "M")
    gen_ioscript_footer(FILE2, nlabel+' to '+to_label,"Packets", "viz2",max,min,sizetype) 
	############ P2P Flows (1M) ##################

	
        
    row = qb.ToNetRangeF(c, nn_id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE3,sizetype)
    gen_iodata(FILE3, now, first, sizetype,row, "M")
    gen_ioscript_footer(FILE3, nlabel+' to '+to_label,"Flows", "viz3",max,min,sizetype) 

	######### P2P Network,Packets,Flows (1M) ##########
	
	
        
    row = qb.ToNetRangeAll(c, nn_id,now, first)
    sizetype_array=setsizetype_all(row,sizetype_array)
    gen_ioascript_header(FILE4,sizetype_array)
    gen_ioadata(FILE4, now, first, sizetype_array,row, "M")
    gen_ioascript_footer(FILE4, nlabel+' to '+to_label, "viz4")


     
     
     
     

    c.close()
# This function (called from flowsgrapher.py , is responsible from generating the graph file for the 1 year to Point/Net 2 Net  graphs that contain the octect,packets,flows and "all" graphs, 
# This function receives the unix time, the title of the graph (to_label),the name of the network  (nlabel) the id of the port in the database and the path where it is going to be written 
def graphP2P1a(now,nlabel, nn_id, to_label, path):

    db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
    c = db.cursor()
	
    qb = QueryBuilder()

    #The file will be named "source"_"destination"_1d.js
    FILE1=open(pjoin(path,"%s_%s_1anet.js")%(nlabel, to_label), "w") 
     
    FILE2=open(pjoin(path,"%s_%s_1apak.js")%(nlabel, to_label), "w") 
     
    FILE3=open(pjoin(path,"%s_%s_1aflw.js")%(nlabel, to_label), "w") 
     
    FILE4=open(pjoin(path,"%s_%s_1acpl.js")%(nlabel, to_label), "w") 
     

	
    first=now-29030400
	
    sizetype="bytes"
    sizetype_array=["bytes","bytes","bytes"]

	################ P2P  Network(1a)#################
		
        
    row = qb.ToNetRangeO(c, nn_id,now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE1,sizetype)
    gen_iodata(FILE1, now, first,sizetype, row, "A")
    gen_ioscript_footer(FILE1, nlabel+' to '+to_label ,"Network","viz1",max,min,sizetype) 

	
	############  P2P Packets(1a) ###################

	 
        
    row = qb.ToNetRangeP(c, nn_id, now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE2,sizetype)
    gen_iodata(FILE2, now, first,sizetype, row, "A")
    gen_ioscript_footer(FILE2, nlabel+' to '+to_label,"Packets", "viz2",max,min,sizetype) 

	############ P2P Flows (1a) ##################

	
        
    row = qb.ToNetRangeF(c, nn_id,now, first)
    sizetype,max,min=setsizetype(row,sizetype)
    gen_ioscript_header(FILE3,sizetype)
    gen_iodata(FILE3, now, first, sizetype,row, "A")
    gen_ioscript_footer(FILE3, nlabel+' to '+to_label,"Flows", "viz3",max,min,sizetype) 

	######### P2P Network,Packets,Flows (1a) ##########
	
	
        
    row = qb.ToNetRangeAll(c, nn_id, now, first)
	

    sizetype_array=setsizetype_all(row,sizetype_array)
    gen_ioascript_header(FILE4,sizetype_array)
    gen_ioadata(FILE4, now, first, sizetype_array,row, "A")
    gen_ioascript_footer(FILE4, nlabel+' to '+to_label, "viz4")



     
     
     
     

    c.close()
###################################################################################################### THE END ####################################################################################
