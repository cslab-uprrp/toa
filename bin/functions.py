import time 

def OutaTime(time_s, ranged):

	tdate=time_s.split(" ")
	date=tdate[0].split("-")
	times=tdate[1].split(":")
	a = (int(date[0]), int(date[1]), int(date[2]), int(times[0]), int(times[1]), int(times[2]), 0, 0, 0) 



	if ranged == "24h":
		t = time.mktime(a)-86400
		return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))
		
	if ranged == "1s":
		t = time.mktime(a)-604800
		return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))

	if ranged == "1m":
		t = time.mktime(a)-2629743
		return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))

	if ranged == "1a":
		t = time.mktime(a)-31556926
		return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))


def gen_header(title):
	content="""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/	xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
<title>%s</title>
</head>

<body>
<h2>Graphic Interface for  %s</h2>

<script type="text/javascript" src="http://www.google.com/jsapi"></script>
""" % (title, title)
	return content

def gen_footer():
	content="""</body>
</html>"""
	return content
	

