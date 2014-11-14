#!/usr/bin/python
import re
import cgi
import sys 
import os
import MySQLdb
import cgitb
import datetime

sys.path.append('../../Models/')

from Config import Config
config=Config()
GRAPH_PATH=config.getGraphsPath()
GRAPH_PATH+="/" # Just in case de user didn't type the last / in the config file 
from SessionModel import SessionModel


uid=sid=remote=""

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
				return 0
			else:
				return 1
		else:
			return 0
		return 1
	else:
		return 0

def  printgraphs(admin,graph,type,w,h,divid,filter=None):


   file=open(graph,'r')
   graphdata=file.read()
   graphdata=graphdata.replace("data","data%s"%(divid))
   response=""

   eventhandler="""      //  google.visualization.events.addListener(net%s, 'select', function(e){
                                 
                                //document.getElementById('APP_FILTER').style.display = 'inline';
                       //  });

                     google.visualization.events.addListener(net%s,'select',function(e){
                               var item = net%s.getSelection()[0];
                               if (item == undefined){

                                 return ;
                                }
                               
                               if (item.row != null && item.column != null){
					//alert(data%s.getFormattedValue(item.row, 1))
                               		$('#%s-popover').css('display','block');
                                       $( "#dialog" ).dialog({modal: true });
                                       $("#active").button({label:"Open"})
                                       var flowDate = data%s.getFormattedValue(item.row, 1);
                                       document.getElementById('APP_FILTER').selectedIndex = 0;        
                                       document.getElementById('%s').addEventListener('click',function() { 
						getApp(flowDate,'%s','%s','%s'); 
						this.removeEventListener('click', arguments.callee);
						$('#%s-popover').css('display', 'none');
						} ,false);        
                               }

                       });

                         """ %(divid,divid,divid,divid,divid,divid,divid+"submit",uid,sid,remote,divid)

   if type !='cpl':
	#Read the data for the graphs and the js functions to draw it from js file
	response+= graphdata


	response+="""
	var view%s = new google.visualization.DataView(data%s);
	view%s.setColumns([0,2,3]); //here you set the columns you want to display
	var net%s = new google.visualization.AreaChart(document.getElementById('%s'));
	net%s.draw(view%s, {curveType: "function",
	 width:%s, height:%s, title: graphtitle , titleX: xtitle, titleY: ytitle,
                        vAxis: {maxValue: maxvalue}}
                );


      """%(divid,divid,divid,divid,divid,divid,divid,w,h)
	if filter!=None and filter=="day" and admin==1:
		response+=eventhandler 
   else:
	
	response+=graphdata

	response+= """
	var view%s = new google.visualization.DataView(data%s);
	view%s.setColumns([0,2,3,4,5,6,7]); //here you set the columns you want to display
	    net%s = new google.visualization.AreaChart(document.getElementById('%s'))
            net%s.draw(view%s, {curveType: "function",
                        width:%s, height:%s,title: graphtitle, titleX: xtitle, titleY: ytitle,
                        vAxis: {maxValue: 10}}
                );

	"""%(divid,divid,divid,divid,divid,divid,divid,w,h)
	
	if filter!=None and filter=="day" and admin==1:
		response+=eventhandler 

   response+="\n\n"
   file.close()	
   return response
def getviews(admin,type,filter,entity,h,w,portlabel,tolabel,label,views):

	
   	if h=='default':
		h='400'
	if w=='default':
		w='750'
	
	DB_NAME=config.getDBName();
	DB_HOST='localhost'
	DB_USER=config.getUser();
	DB_PASS=config.getPassword();

	db = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME, host=DB_HOST)
	c = db.cursor()

	#paths=views.split("$")
	sql="select  graph_name from VIEW_GRAPH,GRAPH where v_id=%s and VIEW_GRAPH.g_id=GRAPH.gid;"%(views)
	c.execute(sql)
	paths=c.fetchall()
	response=""
	i=0
	for path in paths:
		path=path[0] 
		if re.match('(([a-zA-Z0-9]|-|_)+_1(d|m|a|w)(net|pak|flw).js|([a-zA-Z0-9]|-|_)+_([a-zA-Z0-9]|-|_)+_1(d|m|a|w)(net|pak|flw).js|([a-zA-Z0-9]|-|_)+-p([a-zA-Z0-9]|-|_)+_1(d|m|a|w)(net|pak|flw).js)$',path)!=None:
			divid='view%s'%(i+1)
			response+='#graph\n\n'+ printgraphs(admin,GRAPH_PATH+path,'net',w,h,divid)
		
		elif re.match('(([a-zA-Z0-9]|-|_)+_1(d|m|a|w)cpl.js|([a-zA-Z0-9]|-|_)+_([a-zA-Z0-9]|-|_)+_1(d|m|a|w)cpl.js|([a-zA-Z0-9]|-|_)+-p([a-zA-Z0-9]|-|_)+_1(d|m|a|w)cpl.js)$',path)!=None:

			divid='view%s'%(i+1)
			response+='#graph\n\n'+  printgraphs(admin,GRAPH_PATH+path,'cpl',w,h,divid)
		else:
			response+= '#graph ERROR: wrong path %s format for views'%(path)
		i+=1
	return response
#Id, Type (all, pak, flw,col), filter(day,week,month,day), entity(device, port, Net2net),h,w(optional)
def getGraph(admin,type,filter,entity,h, w,portlabel,tolabel,label):

	
   	if h=='default':
		h='400'
	if w=='default':
		w='750'
	graph=""
	
	if filter=='day':
		f='1d'
	elif filter=='week':
		f='1w'
	elif filter=='month':
		f='1m'
	elif filter=='year':
		f='1a'
	if entity=='device':
		#id is network id 
		#GetLabel returns the label for that id 

		graph=GRAPH_PATH+label+'_'+f
		


	elif entity=='port':
		#id is the port if (pid from the database)


		graph=GRAPH_PATH+label+'-p'+portlabel+'_'+f

	elif entity=='net2net':
		graph=GRAPH_PATH+label+'_'+tolabel+'_'+f
		
	if type=='all':
		types=['net','pak','flw','cpl']
		response=""	
		for i in range(len(types)):
			divid='viz%s'%(i+1)
			response+='#graph\n\n'+  printgraphs(admin,graph+types[i]+'.js',types[i],w,h,divid,filter)

	else:
			graph+=type+'.js'
		
			response='#graph\n\n'+  printgraphs(admin,graph,type,w,h,'viz1',filter)



	return response
# MAIN
cgitb.enable()
form = cgi.FieldStorage()

print "Content-Type: text/html\n\n"
print



if form.has_key('views') and   form.has_key('label') and form.has_key('type') and form.has_key('h') and form.has_key('w') and form.has_key('filter') and form.has_key('entity') :
	type = form.getvalue("type")
	filter=form.getvalue("filter")
	entity=form.getvalue("entity")
	label=form.getvalue("label")
	portlabel=form.getvalue("portlabel")
	tolabel=form.getvalue("tolabel")
	h = form.getvalue("h")
	w = form.getvalue("w")
	views=form.getvalue("views")
	paths=views.split("#")
	
	admin=validate(form)
	if type=='all' or type=='net' or   type=='pak' or type=='flw' or type=='cpl':
		if filter == 'day' or filter=='week' or filter=='month' or filter=='year':
			if entity == 'net2net' or entity == 'port' or entity=='device' or entity=='views':
				if re.match('([a-zA-Z0-9]|-)+$',label)!=None:
					if re.match('([a-zA-Z0-9]|-)+$',portlabel)!=None:
						if re.match('([a-zA-Z0-9]|-)+$',tolabel)!=None:
							if re.match('([0-9]+|default)$',h)!=None:
								if re.match('([0-9]+|default)$',w)!=None:
									if entity=='views':
										if  re.match('([0-9]+)$',views)!=None:
									
											print getviews(admin,type,filter,entity,h,w,portlabel,tolabel,label,views)
										else:
											 print 'ERROR: views is not a valid parameter\n'
									else:
										 print getGraph(admin,type,filter,entity,h,w,portlabel,tolabel,label)
								else:
									 print 'ERROR: w param is not valid\n'
							else:
								print 'ERROR: h param is not valid\n'
						else:
							 print 'ERROR: tolabel param is not valid\n'
					else:
						 print 'ERROR: portlabel param is not valid\n'
				else:
					 print 'ERROR: label param is not valid'
			else:
				 print 'ERROR: entity param not valid'
		else:
			print 'ERROR: filter param not valid'
	else:
		 print 'ERROR: type param not valid'	
else:	

	 print 'Missing Params'


