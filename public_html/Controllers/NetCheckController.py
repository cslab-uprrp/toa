def checkAlpha(self, str):
	        
    m = re.match("[A-Za-z]+[A-Za-z0-9\-_]*[A-Za-z0-9]$", str)
	        
    if m:
	                
        if not str == m.group():
	                        
            Exit()
	    
        else:
	                
            Exit()
	
            pass


def Exit(self):
	        
    sys.exit(0)


def CheckDeviceInfo(self,form):
        	
    asn = "NULL"
        	
    int = "NULL"
      
    minb = form.getvalue("MinBytes")

    maxb = form.getvalue("MaxBytes")
 
	# REMEMBER INPUT VALIDATION
        	
    try:
        
        label = form.getfirst("Label")
                	
        tom = form.getfirst("Type")
        	
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
        	        
            int = self.CheckShort(form, "InterfaceNumber")
        
        if form.has_key("as"):
        	
            asn = self.CheckShort(form, "ASNumber")

        return label, tom, asn, int, minb, maxb




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

def CheckIP(self,form, key):
        	
    if not form.has_key(key):
        
        Exit()
        	
    addrv = form.getfirst(key)
        	
    m = re.match("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$|^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$|^[0-9]{1,3}\.[0-9]{1,3}$|^[0-9]{1,3}$", addrv)
        	
    if m:
        	       
        if not addrv == m.group():
        	                
            self.Exit()
        	        
            addr = m.group().split(".")
        	        
            for a in addr:
        	                
                a = int(a)
        	                
                if a < 0 or a > 255:
        	                        
                    self.Exit()
        	
        else:
        	        
            self.Exit()
	
        return addrv
	

def CheckIDs(self,form, key):

    if not form.has_key(key):
        
        Exit()

    ids = form.getvalue(key)
        	
    for i in ids:
        	        
        try:
        	
            i = int(i)
        	        
        except:
        	                
            Exit()
        
    return ids
