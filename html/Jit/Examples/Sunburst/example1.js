var labelType, useGradients, nativeTextSupport, animate;




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


			function init(){

  			//init data
  			var json = [
      			//"root" node is invisible
				{
				"id" : "root" ,
				"name" :"" ,
				"data" :{
				"$type": "none" 
				},"adjacencies": [
				{
					"nodeTo": "1",
					"data": {
					'$type': 'none'
						}
		  			},{
					"nodeTo": "2",
					"data": {
					'$type': 'none'
						}
		  			},{
					"nodeTo": "3",
					"data": {
					'$type': 'none'
						}
		  			},{
					"nodeTo": "4",
					"data": {
					'$type': 'none'
						}
		  			},{
					"nodeTo": "7",
					"data": {
					'$type': 'none'
						}
		  			},{
					"nodeTo": "10",
					"data": {
					'$type': 'none'
						}
		  			},{
					"nodeTo": "11",
					"data": {
					'$type': 'none'
						}
		  			},{
					"nodeTo": "12",
					"data": {
					'$type': 'none'
						}
		  			},{
					"nodeTo": "13",
					"data": {
					'$type': 'none'
						}
		  			}]
			},{
        				"id": "1",
 				       "name": "RUM",
        				"data": {
          					"$angularWidth" :10,
	 					 "$color" : "6502",
	  					"$height": 50
        					},
					"adjacencies":[   {  
             						"nodeTo": "2",  
             						"data": {  
               						"$color": "#DF0101",  
               						"$lineWidth": 4  
             							}								  
           						
           						} ,{
             						"nodeTo": "3",  
             						"data": {  
               						"$color": "#DF0101",  
               						"$lineWidth": 4  
             							}								  
           						
           						} ,{
             						"nodeTo": "4",  
             						"data": {  
               						"$color": "#DF0101",  
               						"$lineWidth": 4  
             							}								  
           						
           						}  		] 
				},{
        				"id": "2",
 				       "name": "RCM",
        				"data": {
          					"$angularWidth" :10,
	 					 "$color" : "6502",
	  					"$height": 50
        					},
					"adjacencies":[   {  
             						"nodeTo": "1",  
             						"data": {  
               						"$color": "#DF0101",  
               						"$lineWidth": 4  
             							}								  
           						
           						} ,{
             						"nodeTo": "3",  
             						"data": {  
               						"$color": "#DF0101",  
               						"$lineWidth": 4  
             							}								  
           						
           						}  		] 
				},{
        				"id": "3",
 				       "name": "RRP",
        				"data": {
          					"$angularWidth" :10,
	 					 "$color" : "6502",
	  					"$height": 50
        					},
					"adjacencies":[  		] 
				},{
        				"id": "4",
 				       "name": "CAYEY",
        				"data": {
          					"$angularWidth" :10,
	 					 "$color" : "6502",
	  					"$height": 50
        					},
					"adjacencies":[  		] 
				},{
        				"id": "7",
 				       "name": "FIU",
        				"data": {
          					"$angularWidth" :10,
	 					 "$color" : "6502",
	  					"$height": 50
        					},
					"adjacencies":[  		] 
				},{
        				"id": "10",
 				       "name": "HPCf",
        				"data": {
          					"$angularWidth" :10,
	 					 "$color" : "6502",
	  					"$height": 50
        					},
					"adjacencies":[  		] 
				},{
        				"id": "11",
 				       "name": "CUH",
        				"data": {
          					"$angularWidth" :10,
	 					 "$color" : "6502",
	  					"$height": 50
        					},
					"adjacencies":[  		] 
				},{
        				"id": "12",
 				       "name": "PSM",
        				"data": {
          					"$angularWidth" :10,
	 					 "$color" : "6502",
	  					"$height": 50
        					},
					"adjacencies":[  		] 
				},{
        				"id": "13",
 				       "name": "AO",
        				"data": {
          					"$angularWidth" :10,
	 					 "$color" : "6502",
	  					"$height": 50
        					},
					"adjacencies":[  		] 
				} ];//end
  //init Sunburst
  alert("bla")
  var sb = new $jit.Sunburst({
    //id container for the visualization
    injectInto: 'infovis',
    //Change node and edge styles such as
    //color, width, lineWidth and edge types
    Node: {
      overridable: true,
      type: useGradients? 'gradient-multipie' : 'multipie'
    },
    Edge: {
      overridable: true,
      type: 'hyperline',
      lineWidth: 2,
      color: '#777'
    },
    //Draw canvas text. Can also be
    //'HTML' or 'SVG' to draw DOM labels
    Label: {
      type: nativeTextSupport? 'Native' : 'SVG'
    },
    //Add animations when hovering and clicking nodes
    NodeStyles: {
      enable: true,
      type: 'Native',
      stylesClick: {
        'color': '#33dddd'
      },
      stylesHover: {
        'color': '#dd3333'
      },
      duration: 700
    },
    Events: {
      enable: true,
      type: 'Native',
      //List node connections onClick
      onClick: function(node, eventInfo, e){
        if (!node) return;
        var html = "<h4>" + node.name + " connections</h4><ul><li>", ans = [];
        node.eachAdjacency(function(adj){
          // if on the same level i.e siblings
            if (adj.nodeTo._depth == node._depth) {
              ans.push(adj.nodeTo.name);
            }
          });
        $jit.id('inner-details').innerHTML = html + ans.join("</li><li>") + "</li></ul>";
      }
    },
    levelDistance: 190,
    // Only used when Label type is 'HTML' or 'SVG'
    // Add text to the labels. 
    // This method is only triggered on label creation
    onCreateLabel: function(domElement, node){
 
     var labels = sb.config.Label.type;
      if (labels === 'HTML') {
        domElement.innerHTML = node.name;
      } else if (labels === 'SVG') {
        domElement.firstChild.appendChild(document.createTextNode(node.name));
      }
    },
    // Only used when Label type is 'HTML' or 'SVG'
    // Change node styles when labels are placed
    // or moved.
    onPlaceLabel: function(domElement, node){
      var labels = sb.config.Label.type;
      if (labels === 'SVG') {
        var fch = domElement.firstChild;
        var style = fch.style;
        style.display = '';
        style.cursor = 'pointer';
        style.fontSize = "0.8em";
        fch.setAttribute('fill', "#fff");
      } else if (labels === 'HTML') {
        var style = domElement.style;
        style.display = '';
        style.cursor = 'pointer';
        if (node._depth <= 1) {
          style.fontSize = "0.8em";
          style.color = "eddd";
        } 
        var left = parseInt(style.left);
        var w = domElement.offsetWidth;
        style.left = (left - w / 2) + 'px';
      }
    }
  });
  // load JSON data.
  sb.loadJSON(json);
  // compute positions and plot.       
  sb.refresh();
  //end
}
