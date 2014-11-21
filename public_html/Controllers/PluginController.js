function getApp(flowDate,uid,sid,remote){
	
	var selection = document.getElementById('APP_FILTER').value;

	var url = '';
	
	if (selection == 'cube')

		url = "../../plugins/cube/?fromtoa="+flowDate+"&PARSE=0&uid="+uid+"&sid="+sid+"&remote="+remote;
	else if (selection == "graph")

		url = "../../plugins/graph/?fromtoa="+flowDate+"&PARSE=0&uid="+uid+"&sid="+sid+"&remote="+remote;

	else return ;

	window.open(url,"_blank");

}
