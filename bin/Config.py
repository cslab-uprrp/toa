#!/usr/bin/python
import os
import sys
import xml.etree.ElementTree as ET
import pwd
#This class is for accesing the value sin the configuration file in the code.
# Warning The class asumes that the order of the tags has not been altered from the original file created at instalation


class Config:
# The constructor initializes all the values by parsing the config.xml file

        name=""
        user=""
        passwd=""
        crontime=""
        logspath=""
        flowspath=""
        graphspath=""

        oldesttime=""
	toapath=""
        def __init__(self, conf_path=None, name = None, user = None, passwd = None, flows_path = None, graphs_path = None, crontime = None, oldest = None, homepath = None):
            


            if name==None:
       	    	
		if conf_path ==None:
                	conf_path = ""
                

			try:
				HOME= pwd.getpwuid(os.stat('.').st_uid).pw_dir
			except:
				HOME=0

			if HOME  and os.path.isfile("/%s/etc/config.xml" % HOME):
				    
                    		conf_path = "/%s/etc/config.xml" % HOME
		

			elif os.path.isfile("/usr/local/etc/config.xml"):
				    
                    		conf_path = "/usr/local/etc/config.xml"
		
                	elif os.path.isfile("/etc/config.xml") :
				    
                    		conf_path = "/etc/config.xml"
		
			elif HOME  and os.path.isfile("/%s/toa/etc/config.xml" % HOME):
				    
                    		conf_path = "/%s/toa/etc/config.xml" % HOME

	    		
                	else:


				print "Content-Type: text/html\n\n"
				print
				    
                    		print """ERROR: Unable to find config.xml file. Try putting it in /home/username/etc, /etc, /usr/local/etc or /home/username/toa/etc (see step 6 of ins
				tructions)"""

                    		sys.exit(1)

		tree = ET.parse(conf_path)
           	 	
                config=tree.getroot()# gets the first tag
            	
                data=config[0] # the first child of the root tag

        		#values related to the database
        		
                self.name=data[0].text #name for the db
        		
                auth=data[1]#list of childrencontaining user and pass
        		
                self.user=auth[0].text #username
        		
                self.passwd=auth[1].text #password
        		
                #### end of values related to the database


                logs=config[1] #tag containing the logpath as a child
        		
                self.logspath=logs[0].text #log path
        
                flows=config[2] # tag containing the path of flow files as child
        		
                self.flowspath=flows[0].text
        
                graphs=config[3]#tag containing the graph paths as childs
        		
                self.graphspath=graphs[0].text 
        
                cron=config[4]#graph containing the crontime as childs

                self.crontime=cron[0].text #the first (and for now only) child is the timei

                otime=config[5]
		
                self.oldesttime=otime[0].text
		
		home=config[6]
		self.toapath=home[0].text

            else:

                self.dbname = name

                self.user = user

                self.passwd = passwd

                self.flows = flows_path

                self.graphs = graphs_path

                self.crontime = crontime

                self.oldesttime = oldest

		self.toapath = homepath
        #the following function return the values when used inside the code
			
        def getUser(self):

            return str(self.user).strip();

        def getPassword(self):

            return str(self.passwd).strip()

        def getDBName(self):

            return str(self.name).strip()

        def getFlowsPath(self):
                
            return str(self.flowspath).strip()

        def getGraphsPath(self):

            return str(self.graphspath).strip()

        def getCronTime(self):

            return int(str((self.crontime)).strip())
        
        def getLogsPath(self):

            return str(self.logspath).strip();

        def getOldesttime(self):
		
            return int(str(self.oldesttime).strip())      
        
	def getToaPath(self):

            return str(self.toapath).strip();



