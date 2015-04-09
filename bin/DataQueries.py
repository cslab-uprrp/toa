import MySQLdb

ONE_DAY       = 86400		# To check how it compares with the behaiviour of the current week
ONE_WEEK      = ONE_DAY * 7	# To check how it compares with the week behaiviour
HALF_HOURS  = 30 * 60		# half an hour to check under and over an instant of time
LAST_INSTANTS = 12   		# To look into same instant of last 3 months
LAST_HOURS    = 4   		# To look into a month of specific day hours

class DataQueries:

	def GetDataRange(self, c, id, start, finish):
			c.execute("""select ioctect, ooctect, ipacks, opacks, iflows, oflows, time_unix from rrd_n where nid=%s and time_unix<='%s' and time_unix>='%s' order by time_unix""" % (id, start, finish))
			return c.fetchall()


	def GetWeekly(self, c, id, now):
		start = now - ONE_WEEK
		return self.GetDataRange(c, id, start, now)

	def GetDayly(self, c, id, now):
		start = now - ONE_DAY
		return self.GetDataRange(c, id, start, now)

	def GetSameTimeInstants(self, c, id, now):
		# To look into a month of specific day hours
		instant = now - ONE_WEEK
		qrange = "%s" % instant
		i = 0
		while i < LAST_INSTANTS:
			instant = instant - ONE_WEEK
			qrange = "%s,%s" % (instant, qrange)
			i+=1

		c.execute("""select ioctect, ooctect, ipacks, opacks, iflows, oflows, time_unix from rrd_n where nid=%s and time_unix in (%s) order by time_unix""" % (id, qrange))

	def GetSameDayTime(self, c, id, now):

		instant = now - ONE_WEEK
		start_i = instant - HALF_HOURS
		finish_i = instant + HALF_HOURS

		i = 0:
		while i < LAST_HOURS:
			c.execute("""select ioctect, ooctect, ipacks, opacks, iflows, oflows, time_unix from rrd_n where nid=%s and time_unix<='%s' and time_unix>='%s' order by time_unix""" % (id, start_i, finish_i))
			start_i = start_i - ONE_WEEK
			finish_i = finish_i - ONE_WEEK
			i+=1












