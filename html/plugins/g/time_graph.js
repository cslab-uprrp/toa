//document.addEventListener("keypress",check_text,false)
// var pattern=/(^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){1,3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})$)|(^(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})$)/g;
var file_name ='';//"ft-v05.2013-03-12.000000-0400";
var labelType, useGradients, nativeTextSupport, animate;

var inp_date= '',time='',srcIp = "",dstIp = "",src_prefix = "0",dst_prefix = "0",json ;
(function() {
  var ua = navigator.userAgent,
	  iStuff = ua.match(/iPhone/i) || ua.match(/iPad/i),
	  typeOfCanvas = typeof HTMLCanvasElement,
	  nativeCanvasSupport = (typeOfCanvas == 'object' || typeOfCanvas == 'function'),
	  textSupport = nativeCanvasSupport 
		&& (typeof document.createElement('canvas').getContext('2d').fillText == 'function');
  //I'm setting this based on the fact that ExCanvas provides text support for IE
  //and that as of today iPhone/iPad current text support is lame
  labelType = (!nativeCanvasSupport || (textSupport && !iStuff))? 'Native' : 'HTML';
  nativeTextSupport = labelType == 'Native';
  useGradients = nativeCanvasSupport;
  animate = !(iStuff || !nativeCanvasSupport);
})();

var Log = {
  elem: false,
  write: function(text){
	if (!this.elem) 
	  this.elem = document.getElementById('log');
	this.elem.innerHTML = text;
	this.elem.style.left = (500 - this.elem.offsetWidth / 2) + 'px';
  }
};

function validData(request_type){
	if (request_type == 1){
		time= document.getElementById('timepicker').value;
		inp_date=document.getElementById('datepicker').value;
		if (inp_date.length==0||time.length==0) return 0;
	}
	srcIp=document.getElementById('srcIp').value;
	dstIp=document.getElementById('dstIp').value;	
	src_pre=document.getElementById('src_pre').value ;
	dst_pre=document.getElementById('dst_pre').value ;
	if (srcIp.length == 0)srcIp = "null" ;
	if (dstIp.length == 0)dstIp = "null";
	if (src_pre%8!=0||src_pre<0||src_pre>32||dst_pre%8!=0||dst_pre<0||dst_pre>32)return 0 ;
	
	return 1;
}

function getUrl(request_type){
	//if !(typeof request_type == "number" && (request_type >= 0 && request_type <= 1){
	if (request_type==0){
		return 'index.cgi?fromtoa='+inp_date+'&PARSE=1';
	}

	else if (request_type==1){
		return  'index.cgi?srcIp='+srcIp+'&dstIp='+dstIp+'&src_pre='+src_pre+'&dst_pre='+dst_pre+'&time='+time+'&PARSE=1'+'&date='+inp_date;

	}
	
}

function parseData(request_type)
{

	if (!validData(request_type))return ;
	
	var response=getResponse(getUrl(request_type));
	
	if (parseInt(response)==-1){
		alert('Input_Error');
		return 0;
    }

	json = JSON.parse(response);

	document.body.style.cursor = "wait";

	// init ForceDirected
	var fd = new $jit.ForceDirected({
			//id of the visualization container
			injectInto: 'infovis',
			//Enable zooming and panning
			//by scrolling and DnD
			Navigation: {
				enable: true,
				//Enable panning events only if we're dragging the empty
				//canvas (and not a node).
				panning: 'avoid nodes',
				zooming: 10 //zoom speed. higher is more sensible
			},
			
		// Change node and edge styles such as
			// color and width.
			// These properties are also set per node
			// with dollar prefixed data-properties in the
			// JSON structure.
			Node: {overridable: true},
			Edge: {
				overridable: true,
				color: '#23A4FF',
				lineWidth: 0.7
			},
			//Native canvas text styling
			Label: {
				type: labelType, //Native or HTML
				size: 10,
				style: 'bold'
			},
			//Add Tips
			Tips: {
				enable: true,
				onShow: function(tip, node) {
					//count connections
					var count = 0;
					node.eachAdjacency(function() { count++; });
					//display node info in tooltip
					tip.innerHTML = "<div class=\"tip-title\">" + node.name + "</div>"
					+ "<div class=\"tip-text\"><b>connections:</b> " + count + "</div>";
				}
			},
			// Add node events
			Events: {
				enable: true,
				type: 'Native',
				//Change cursor style when hovering a node
				onMouseEnter: function() {
					fd.canvas.getElement().style.cursor = 'move';
				},
				onMouseLeave: function() {
					fd.canvas.getElement().style.cursor = '';
				},
				//Update node positions when dragged
				onDragMove: function(node, eventInfo, e) {
					var pos = eventInfo.getPos();
					node.pos.setc(pos.x, pos.y);
					fd.plot();
				},
				//Implement the same handler for touchscreens
				onTouchMove: function(node, eventInfo, e) {
					$jit.util.event.stop(e); //stop default touchmove event
					this.onDragMove(node, eventInfo, e);
				},
				//Add also a click handler to nodes
				onClick: function(node) {
					if(!node) return;
					// Build the right column relations list.
					// This is done by traversing the clicked node connections.
					var html = "<b><br><span>Ip address: </span>" + node.name + " <br><br><span>Connected to:</span></b><ol><li>",
					list = [];
					node.eachAdjacency(function(adj){
						list.push(adj.nodeTo.name);
					});
					//append connections information
					$jit.id('inner-details').innerHTML = html + list.join("</li><li>") + "</li></ol>";
				}
			},
			
		//Number of iterations for the FD algorithm
			iterations: 200,
			//Edge length
			levelDistance: 130,
			// Add text to the labels. This method is only triggered
			// on label creation and only for DOM labels (not native canvas ones).
		onCreateLabel: function(domElement, node){
	  // Create a 'name' and 'close' buttons and add them
	  // to the main node label
	  var nameContainer = document.createElement('span'),
		  closeButton = document.createElement('span'),
		  style = nameContainer.style;
	  nameContainer.className = 'name';
	  nameContainer.innerHTML = node.name;
	  closeButton.className = 'close';
	  closeButton.innerHTML = 'x';
	  domElement.appendChild(nameContainer);
	  domElement.appendChild(closeButton);
	  style.fontSize = "0.8em";
	  style.color = "#ddd";
	  //Fade the node and its connections when
	  //clicking the close button
	  closeButton.onclick = function() {
		node.setData('alpha', 0, 'end');
		node.eachAdjacency(function(adj) {
		  adj.setData('alpha', 0, 'end');
		});
		fd.fx.animate({
		  modes: ['node-property:alpha',
				  'edge-property:alpha'],
		  duration: 500
		});
	  };
	  //Toggle a node selection when clicking
	  //its name. This is done by animating some
	  //node styles like its dimension and the color
	  //and lineWidth of its adjacencies.
	  nameContainer.onclick = function() {
		//set final styles
		fd.graph.eachNode(function(n) {
		  if(n.id != node.id) delete n.selected;
		  n.setData('dim', 7, 'end');
		n.eachAdjacency(function(adj) {
			adj.setDataset('end', {
			  lineWidth: 0.4,
			  color: '#23a4ff'
			});
		  });
		});
		if(!node.selected) {
		  node.selected = true;
		  node.setData('dim', 17, 'end');
		  node.eachAdjacency(function(adj) {
			adj.setDataset('end', {
			  lineWidth: 3,
			  color: '#36acfb'
			});
		  });
		} else {
		  delete node.selected;
		}
		//trigger animation to final styles
		fd.fx.animate({
		  modes: ['node-property:dim',
				  'edge-property:lineWidth:color'],
		  duration: 500
		});
		// Build the right column relations list.
		// This is done by traversing the clicked node connections.
		var html = "<h4>" + node.name + "</h4><b> connections:</b><ul><li>",
			list = [];
		node.eachAdjacency(function(adj){
		  if(adj.getData('alpha')) list.push(adj.nodeTo.name);
		});
		//append connections information
		$jit.id('inner-details').innerHTML = html + list.join("</li><li>") + "</li></ul>";
	  };
	}, 
		// Change node styles when DOM labels are placed or moved.
			onPlaceLabel: function(domElement, node){
				var style = domElement.style;
				var left = parseInt(style.left);
				var top = parseInt(style.top);
				var w = domElement.offsetWidth;
				style.left = (left - w / 2) + 'px';
				style.top = (top + 10) + 'px';
				style.display = '';
			}
	});//fd object end

	// load JSON data.
	fd.loadJSON(json);
	// compute positions incrementally and animate.
	fd.computeIncremental({
			iter: 40,
			property: 'end',
			onStep: function(perc){
				Log.write(perc + '% loaded...');
			},
			onComplete: function(){
				Log.write('');
				document.body.style.cursor="default";
				fd.animate({
					modes: ['linear'],
					transition: $jit.Trans.Elastic.easeOut,
					duration: 2500
				});
			}
	});
  // end
}


function check_text(){
		var key = event.keyCode ;
		/*8 = backspace;46 = "."*/
		if (key == 46 && document.activeElement.id!="conn_num"){
		//      if (document.activeElement.length =
				if (pattern.test(document.activeElement.value)){
						//alert(document.activeElement.value);
						event.returnValue = true;
				}
				else event.returnValue=false;
				return;
		}

		if (key==8){
				event.returnValue=true;
				return true;
		}
		/*48 = number 0; 57 = number 9*/
		if ((key< 48 || key >57)){
				event.returnValue=false; //This will apply function to all input box.
				//return false;
		}
}
$(document).ready(function(){
		$("#cp_title").click(function(){
				$("#updwn").fadeToggle(0);
				//$('#settings').animate({backgroundColor: '#FFFFFF'}, 'slow');
				/*var menu_status_btn = $('#cp_title').text() ;
				$("#cp_title").text(
				(menu_status_btn == 'HIDE'?'SHOW':'HIDE'));*/
		}),
		$(function() {
				$( "#c_p" ).draggable();
		}),
		$("#cp_title").hover(function(){
				$(this).stop().css({"cursor" : "pointer"}) }),
		$(function(){
			$( "#datepicker" ).datepicker({ 
				minDate: -2000, maxDate: "0"
			});
		}),

		$(function(){
			$('#timepicker').timepicker({showLeadingZero: true });
		});

});



function getResponse(url){
	var xmlhttp = new XMLHttpRequest(); // a http object to execute the request.
	xmlhttp.open("POST",url,false); // We define the kind of request.
	xmlhttp.send(); // The request is sent to the server side.	
	return xmlhttp.responseText ; // We return the server response.
}


window.onload = function(){
	$('#axis_menu').hide(0);
	document.getElementById('srcIp').focus();
	inp_date = document.getElementById('flow_date').value ;

	if (inp_date.length == 19 || inp_date.length == 8){
		parseData(0);
	}
};

