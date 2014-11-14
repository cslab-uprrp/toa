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



def  printgraphs():


   	graph=GRAPH_PATH+'/p2p_graph.js'
   	file=open(graph,'r')
   	graphdata=file.read()
   	response="""
		        var labelType, useGradients, nativeTextSupport, animate;

                        (function() {
                        var ua = navigator.userAgent,
                        iStuff = ua.match(/iPhone/i) || ua.match(/iPad/i),
                        typeOfCanvas = typeof HTMLCanvasElement,
                        nativeCanvasSupport = (typeOfCanvas == 'object' || typeOfCanvas == 'function'),
                        textSupport = nativeCanvasSupport
                        && (typeof document.createElement('canvas').getContext('2d').fillText =='function');
                        labelType = (!nativeCanvasSupport || (textSupport && !iStuff))? 'Native' : 'HTML';
                        nativeTextSupport = labelType == 'Native';
                        useGradients = nativeCanvasSupport;
                        animate = !(iStuff || !nativeCanvasSupport);})();

                        var Log = {
                        elem: false,
                        write: function(text){
                        if (!this.elem)
                        this.elem = document.getElementById('log');
                        this.elem.innerHTML = text;
                        this.elem.style.left = (500 - this.elem.offsetWidth / 2) + 'px';
                                                }


                                };



	"""


	response+= graphdata

	response+="""
 
  var sb = new $jit.Sunburst({
    injectInto: 'infovis',
    Node: {
      overridable: true,
      type: useGradients? 'gradient-multipie' : 'multipie'
    },
    Edge: {
      overridable: true,
      type: 'hyperline',
      lineWidth: 2,
      color: '#0000FF'
    },
    Label: {
      type: nativeTextSupport? 'Native' : 'SVG'
    },
    NodeStyles: {
      enable: true,
      type: 'Native',
      stylesClick: {
       "color": "#E25D33",
      },
      stylesHover: {
       "color": "#E25D33",
      }, 
    },
          Tips: {
                enable: true,
                      onShow: function(tip, node) {
                                      var count = 0;
                                              node.eachAdjacency(function() { count++; });
                                                                      tip.innerHTML = "<div class='tip-title'> All Octects: " + node.getData('All_Octects') +'<br/> All Packets: ' + node.getData('All_Packets')+'<br/> Al Flows: ' +node.getData('All_Flows')+ "</div>"
                                                                                + "<div class='tip-text'><b>connections:</b> " + (count -1)  + "</div>"; 
                                                                                      }
                                                                                          },

    Events: {
      enable: true,
      type: 'Native',

      
      onClick: function(node) {
              if(!node) return;
                                      var html = "<h4>" + node.name + "</h4><b> connections:</b><ul><li>",
                                                  list = [];
                                                it=0;
                                                          node.eachAdjacency(function(adj){
                                                                 if (it!=0){
                                                                list.push(adj.nodeTo.name);
                                                                           list.push('Octects: '+adj.getData('Octects'));
                                                                                    list.push('Packets: '+adj.getData('Packets'));
                                                                                             list.push('Flows: '+adj.getData('Flows')+'<br/><br/>');
                                                                                             }
                                                                it++;
                                                                                                     

                                                                                                             });

                $jit.id('inner-details').innerHTML = html + list.join('</li><li>') + '</li></ul>';

                  }
	

    },
    levelDistance: 190,
    onCreateLabel: function(domElement, node){
 
 
     var labels = sb.config.Label.type;
      if (labels === 'HTML') {
        domElement.innerHTML = node.name;
      } else if (labels === 'SVG') {
        domElement.firstChild.appendChild(document.createTextNode(node.name));
      }
    },
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
  sb.loadJSON(json);
  sb.refresh();




	"""

   	response+="\n\n"
   	file.close()	
   	return response

# MAIN
cgitb.enable()
form = cgi.FieldStorage()

print "Content-Type: text/html\n\n"
print

print printgraphs()



