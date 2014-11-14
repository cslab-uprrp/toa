import MySQLdb

from FlowQueries import *
from Config import Config
class QueryBuilder:

	def IntRangeO(self, c, id, rangea, rangeb):
		c.execute("""select ioctect, ooctect, time_unix from rrd_n where nid=%s and time_unix<'%s' and time_unix>'%s' order by time_unix""" % (id, rangea, rangeb))
		return  c.fetchall()
		
	def IntRangeP(self, c, id, rangea, rangeb):
		c.execute("""select ipacks, opacks, time_unix from rrd_n where nid=%s and time_unix<'%s' and time_unix >'%s' order by time_unix""" % (id, rangea, rangeb))
		return  c.fetchall()
		
	def IntRangeF(self, c, id, rangea, rangeb):
		c.execute("""select iflows, oflows, time_unix from rrd_n where nid=%s and time_unix<'%s' and time_unix>'%s' order by time_unix""" % (id, rangea, rangeb))
		return  c.fetchall()

	def IntRangeAll(self, c, id, rangea, rangeb):
		c.execute("""select ioctect,ooctect,ipacks,opacks,iflows,oflows, time_unix from rrd_n where nid=%s and time_unix<'%s' and time_unix>'%s' order by time_unix""" % (id, rangea, rangeb))


		return  c.fetchall()
		
	def PortRangeO(self, c, id, rangea, rangeb):
		c.execute("""select ioctect, ooctect,   time_unix from rrd_port where pid=%s and time_unix<'%s' and time_unix>'%s' order by time_unix""" % (id, rangea, rangeb))
		return  c.fetchall()
		
	def PortRangeP(self, c, id, rangea, rangeb):
		c.execute("""select ipacks, opacks,   time_unix from rrd_port where pid=%s and time_unix<'%s' and time_unix>'%s' order by time_unix""" % (id, rangea, rangeb))
		return  c.fetchall()
		
	def PortRangeF(self, c, id, rangea, rangeb):
		c.execute("""select iflows, oflows,   time_unix from rrd_port where pid=%s and time_unix<'%s' and time_unix>'%s' order by time_unix""" % (id, rangea, rangeb))
		return  c.fetchall()

	def PortRangeAll(self, c, id, rangea, rangeb):
		c.execute("""select ioctect,ooctect,ipacks,opacks,iflows,oflows,time_unix  from rrd_port where pid=%s and time_unix <'%s' and time_unix >'%s' order by time_unix """ % (id, rangea, rangeb))
		return  c.fetchall()
		
	def ToNetRangeO(self, c, id,  rangea, rangeb):
		fromandto=GetFromandTo(c,id)
                reverseid=GetReverseNet2Net(c,fromandto[0],fromandto[1])
                reverseid=reverseid[0]#Make sure there is a reverse connection in the database, otherwise this will fail
		c.execute("""select ioctect,time_unix from rrd_to_net where nn_id=%s and time_unix <'%s' and time_unix > '%s' order by time_unix"""%(id,rangea,rangeb))
                input=c.fetchall()
		c.execute("""select ioctect,time_unix from rrd_to_net where nn_id=%s and time_unix <'%s' and time_unix > '%s' order by time_unix"""%(reverseid,rangea,rangeb))
                output=c.fetchall()
                return self.normalize(input,output,rangeb,rangea)
		
	def ToNetRangeP(self, c, id,  rangea, rangeb):
		fromandto=GetFromandTo(c,id)
                reverseid=GetReverseNet2Net(c,fromandto[0],fromandto[1])
                reverseid=reverseid[0]
		c.execute("""select ipacks,time_unix from rrd_to_net where nn_id=%s and time_unix <'%s' and time_unix > '%s' order by time_unix"""%(id,rangea,rangeb))
                input=c.fetchall()
		c.execute("""select ipacks,time_unix from rrd_to_net where nn_id=%s and time_unix <'%s' and time_unix > '%s' order by time_unix"""%(reverseid,rangea,rangeb))
                output=c.fetchall()
                return self.normalize(input,output,rangeb,rangea)
		
	def ToNetRangeF(self, c, id,  rangea, rangeb):
		fromandto=GetFromandTo(c,id)
                reverseid=GetReverseNet2Net(c,fromandto[0],fromandto[1])
                reverseid=reverseid[0]
		c.execute("""select iflows,time_unix from rrd_to_net where nn_id=%s and time_unix <'%s' and time_unix > '%s' order by time_unix"""%(id,rangea,rangeb))
                input=c.fetchall()
		c.execute("""select iflows,time_unix from rrd_to_net where nn_id=%s and time_unix <'%s' and time_unix > '%s' order by time_unix"""%(reverseid,rangea,rangeb))
                output=c.fetchall()
                return self.normalize(input,output,rangeb,rangea)
	def ToNetRangeAll(self, c, id,  rangea, rangeb):
		fromandto=GetFromandTo(c,id)
                reverseid=GetReverseNet2Net(c,fromandto[0],fromandto[1])
                reverseid=reverseid[0]
		c.execute("""select ioctect,ipacks,iflows,time_unix from rrd_to_net where nn_id=%s and time_unix <'%s' and time_unix > '%s' order by time_unix"""%(id,rangea,rangeb))
                input=c.fetchall()
		c.execute("""select ioctect,ipacks,iflows,time_unix from rrd_to_net where nn_id=%s and time_unix <'%s' and time_unix > '%s' order by time_unix"""%(reverseid,rangea,rangeb))
                output=c.fetchall()
                return self.normalizeall(input,output,rangeb,rangea)
        
        def normalizeall (self,input,output,rangeb,rangea):# Currently disabled
        #VERIFICAR WHILE DEBIDO A QUE LOS QUIERIES SON < y no <=
            config=Config()
            INCREMENT=config.getCronTime()
            start=rangeb
            end=rangea
            join = [[0 for i in range(7)] for j in range(((end-start)/300)-1)]
            c1=c2=x=0
            start =( start - start%INCREMENT) + INCREMENT # CHANGE TO INCREMENT
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


        def normalize (self,input,output,rangeb,rangea):
            #VERIFICAR WHILE DEBIDO A QUE LOS QUIERIES SON < y no <=
            config=Config()
            INCREMENT=config.getCronTime()
            start=rangeb
            end=rangea
            join = [[0 for i in range(3)] for j in range(((end-start)/INCREMENT)-1)]
            c1=c2=x=0
            start =( start - start%INCREMENT) + INCREMENT
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
