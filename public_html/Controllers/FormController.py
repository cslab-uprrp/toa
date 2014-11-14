def AddNetworkForm(uid, sid, remote, errors):

	print "<form action='../../Controllers/AddNetwork.cgi' method='post'>"

	print "<center><div class='row'>"

	print "<div class='col-md-3 col-md-offset-3'>"

	print "<div class='input-group input-group-lg'>"

	print "<span class='input-group-addon'><i class='glyphicon glyphicon-tag'></i></span>"

	print "<input class='form-control' type='text' name='Label' value='' placeholder='Network Label'/>"

	print "</div>"

	print "</div>"

	print "<div class='col-md-3'>"

	print "<div class='input-group input-group-lg'>"

	print "<select class='form-control' name='Type'><option value='interface'>Interface</option>"

	print "<option value='as'>As</option><option value='network'>Network</option></select>"

	print "</div>"

	print "</div>"

	print "</div>"

	print "<br>"

	print "<div class='row'>"

	print "<div class='col-md-3 col-md-offset-3'>"

	print "<div class='input-group input-group-lg'>"

	print "<span class='input-group-addon'>I/F</span>"

	print "<input class='form-control' type='text' name='InterfaceId' value='' placeholder='Interface Id'/>"

	print "</div>"

	print "</div>"

	print "<div class='col-md-3'>"

	print "<div class='input-group input-group-lg'>"

	print "<span class='input-group-addon'>AS</span>"

	print "<input class='form-control' type='text' name='ASNumber' value='' placeholder='AS Number'/>"

	print "</div></div></div>"

	print "<br>"

	print "<div class='row'>"

	print "<div class='col-md-3 col-md-offset-3'>"

	print "<div class='input-group input-group-lg'>"

	print "<span class='input-group-addon'><i class='glyphicon glyphicon-sort-by-attributes-alt'></i></span>"

	print "<input class='form-control' type='text' name='MinBytes' value='' placeholder='Min Bytes Size'/>"

	print "</div></div>"

	print "<div class='col-md-3'>"

	print "<div class='input-group input-group-lg'>"

	print "<span class='input-group-addon'><i class='glyphicon glyphicon-sort-by-attributes'></i></span>"

	print "<input class='form-control' type='text' name='MaxBytes' value='' placeholder='Max Bytes Size'/>"

	print "</div></div></div>"

	print "<br>"

	print "<div class='row'>"

	print "<div class='col-md-4 col-md-offset-3'>"

	if "'Network Added.'" in errors:

		print "<p class='text-success'>"

		for error in errors:

			if error != None:

				print error.strip('\'\'')

		print "</p>"

	else:

		print "<p class='text-danger'>"

		for error in errors:

			print error.strip('\'\'')

		print "</p>"

	print "</div>"

	print "<div class='col-md-2'>"

	print "<button class='btn btn-default btn-lg pull-right add-device-button'>Add Network</button>"

	print "</div></div>"

	print "<input type='hidden' name='uid' value='%s'/>"%(uid) 

	print "<input type='hidden' name='sid' value='%s'/>"%(sid)

	print "<input type='hidden' name='remote' value='%s'/>"%(remote) 

	print "</form>"


def EditNetworkForm(nid, device, uid, sid, remote, errors):

	print "<form action='../../Controllers/SaveNetwork.cgi' method='post'>"

	print "<center><div class='row'>"

	print "<div class='col-md-3 col-md-offset-3'>"

	print "<div class='input-group input-group-lg'>"

	print "<span class='input-group-addon'><i class='glyphicon glyphicon-tag'></i></span>"

	print "<input class='form-control' type='text' name='Label' value='%s' placeholder='Network Label'/>"%(device[0])

	print "</div>"

	print "</div>"

	print "<div class='col-md-3'>"

	print "<div class='input-group input-group-lg'>"

	print "<select class='form-control' name='Type'>"

	if device[3] == "interface":

		print "<option value='interface' selected='selected'>Interface</option>"

	else:

		print "<option value='interface'>Interface</option>"

	if device[3] == "as":

		print "<option value='as' selected='selected'>As</option>"

	else:

		print "<option value='as'>As</option>"

	if device[3] == "network":

		print "<option value='network' selected='selected'>Network</option></select></td>"

	else:

		print "<option value='network'>Network</option></select></td>"

	print "</select>"

	print "</div>"

	print "</div>"

	print "</div>"

	print "<br>"

	print "<div class='row'>"

	print "<div class='col-md-3 col-md-offset-3'>"

	print "<div class='input-group input-group-lg'>"

	print "<span class='input-group-addon'>I/F</span>"

	print "<input class='form-control' type='text' name='InterfaceId' value='%s' placeholder='Interface Id'/>"%(device[1])

	print "</div>"

	print "</div>"

	print "<div class='col-md-3'>"

	print "<div class='input-group input-group-lg'>"

	print "<span class='input-group-addon'>AS</span>"

	print "<input class='form-control' type='text' name='ASNumber' value='%s' placeholder='AS Number'/>"%(device[2])

	print "</div></div></div>"

	print "<br>"

	print "<div class='row'>"

	print "<div class='col-md-3 col-md-offset-3'>"

	print "<div class='input-group input-group-lg'>"

	print "<span class='input-group-addon'><i class='glyphicon glyphicon-sort-by-attributes-alt'></i></span>"

	print "<input class='form-control' type='text' name='MinBytes' value='%s' placeholder='Min Bytes Size'/>"%(device[4])

	print "</div></div>"

	print "<div class='col-md-3'>"

	print "<div class='input-group input-group-lg'>"

	print "<span class='input-group-addon'><i class='glyphicon glyphicon-sort-by-attributes'></i></span>"

	print "<input class='form-control' type='text' name='MaxBytes' value='%s' placeholder='Max Bytes Size'/>"%(device[5])

	print "</div></div></div>"

	print "<br>"

	print "<div class='row'>"

	print "<div class='col-md-4 col-md-offset-3'>"

	print "<p class='text-danger'>"

	for error in errors:

		print error.strip('\'\'')

	print "</p>"

	print "</div>"

	print "<div class='col-md-2'>"

	print "<button class='btn btn-default btn-lg pull-right add-device-button'>Save Network</button>"

	print "</div></div>"

	print "<input type='hidden' name='nid' value='%s'/>"%(nid) 

	print "<input type='hidden' name='uid' value='%s'/>"%(uid) 

	print "<input type='hidden' name='sid' value='%s'/>"%(sid)

	print "<input type='hidden' name='remote' value='%s'/>"%(remote) 

	print "</form>"


def AddPortsForm(nid, uid, sid, remote):

	print "<form action='../../Controllers/AddPort.cgi' method='post'>"

	print "<center><div class='row'>"

	print "<div class='col-md-3 col-md-offset-4'>"

	print "<div class='input-group input-group-lg'>"

	print "<span class='input-group-addon'><i class='glyphicon glyphicon-tag'></i></span>"

	print "<input class='form-control' type='text' name='Port' value='' placeholder='Port Number'/>"

	print "</div>"

	print "</div>"

	print "<div class='col-md-1'>"

	print "<button class='btn btn-default btn-lg pull-right add-device-button'>Add Port</button>"

	print "</div>"

	print "<input type='hidden' name='nid' value='%s'/>"%(nid) 

	print "<input type='hidden' name='uid' value='%s'/>"%(uid) 

	print "<input type='hidden' name='sid' value='%s'/>"%(sid)

	print "<input type='hidden' name='remote' value='%s'/>"%(remote) 

	print "</div>"

	print "</form>"

def AddNet2NetForm(nid, uid, sid, remote, devices):

	print "<center><form action='../../Controllers/AddNet2Net.cgi' method='post'>"

	print "<select name='Device'>"

	for d in devices:

		print "<option value='%s'>%s</option>"%(d[0], d[1])

	print "</select>"

	print "<button class='btn btn-inverse' id='add-n2n-button'>Add Net2Net</button></td>"

	print "<input type='hidden' name='nid' value='%s'/>"%(nid) 

	print "<input type='hidden' name='uid' value='%s'/>"%(uid) 

	print "<input type='hidden' name='sid' value='%s'/>"%(sid)

	print "<input type='hidden' name='remote' value='%s'/>"%(remote) 

	print "</form><br>"

def AddNetBlockForm(nid, uid, sid, remote):

	print "<center><form action='../../Controllers/AddBlock.cgi' method='post'>"

	print "<input type='text' name='FIP' value='' placeholder='From (IP Address)'/> <input type='text' name='TIP' value='' placeholder='To (IP Address)'/> <button class='btn btn-inverse' id='add-netblock-button'>Add NetBlock</button>"

	print "<input type='hidden' name='nid' value='%s'/>"%(nid) 

	print "<input type='hidden' name='uid' value='%s'/>"%(uid) 

	print "<input type='hidden' name='sid' value='%s'/>"%(sid)

	print "<input type='hidden' name='remote' value='%s'/>"%(remote) 

	print "</form><br>"


def AddViewForm(uid, sid, remote, errors):

	print "<form action='../../Controllers/AddView.cgi' method='post'>"

	print "<div class='row'>"

	print "<div class='col-md-3 col-md-offset-3'>"

	print "<div class='input-group input-group-lg'>"

	print "<span class='input-group-addon'><i class='glyphicon glyphicon-tag'></i></span>"

	print "<input class='form-control' type='text' name='view_name' value='' placeholder='View Name'/>"

	print "</div>"

	print "</div></div><br><br><div class='row'>"

	print "<div class='col-md-5 col-md-offset-3'>"

	print "<textarea name='view_description' class='form-control' placeholder='View Description' rows='7'></textarea>"

	print "</div>"

	print "</div>"

	print "<br>"

	print "<div class='row'>"

	print "<div class='col-md-4 col-md-offset-3'>"

	errors = errors.strip("[' | ']").split(",")

	if "View Added" in errors:

		print "<p class='text-success'>"

		for error in errors:

			if error != None:

				print error.strip(" '|' ")

		print "</p>"

	else:

		print "<p class='text-danger'>"

		if '[' not in errors:

			for error in errors:

				print error.strip(" '|' ")

		print "</p>"

	print "</div>"

	print "<div class='col-md-2'>"

	print "<button class='btn btn-default btn-lg pull-right add-view-button'>Add View</button>"

	print "</div></div>"

	print "<input type='hidden' name='uid' value='%s'/>"%(uid) 

	print "<input type='hidden' name='sid' value='%s'/>"%(sid)

	print "<input type='hidden' name='remote' value='%s'/>"%(remote)
	
	print "</form>"


def EditViewForm(uid, sid, remote, graphs, ViewName, view_graphs, gnum):

	print "<center><div id='Forms'><form action='../../Controllers/EditView.cgi' method='post'>"

	print "<table>"

	print "<tr><td><input type='text' name='ViewName' value='%s' placeholder='View Name'/></td><td>&nbsp;</td>"%(ViewName)

	print "<td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td>"

	print "<td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td>"

	print "<td><select name='Graph' id='Graph'>"

	for g in graphs:

		print "<option value='%s'>%s</option>"%(g[0], g[1])

	print "</select></td>"

	print "<td><div id='AddGraphButton' onclick='AddGraph()'>Add Graph</div></td>"

	print "</tr>"

	print "</table>"

	print "<table id='graphs_preview'></table>"

	print "<input type='hidden' id='graph_ids' name='graphs' value='%s'/>"%(view_graphs)

	print "<input type='hidden' id='gnumber' name='gnumber' value='%s'/>"%gnum 

	print "<input type='hidden' name='uid' value='%s'/>"%(uid) 

	print "<input type='hidden' name='sid' value='%s'/>"%(sid)

	print "<input type='hidden' name='remote' value='%s'/>"%(remote)

	print "<button id='SaveViewButton'>Save</button>"
	
	print "</form>"



