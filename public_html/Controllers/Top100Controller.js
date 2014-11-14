/********************************************************
                                                        *
Gets top 100 with entity being Network, Port or Net2Net *
and type being Octects, Packets or Flows.               *
                                                        *
Entity Mapping:                                         *
                                                        *
    Network = net, Port = port, Net2Net = net2net       *
                                                        *
Type Mapping:                                           *
                                                        *
    Octects = oct, Packets = pak, Flows = flow          *
                                                        *
*********************************************************/

function GetTop100(entity, type, id, uid, sid, remote){

    //var validator = ['net | ports | net2net', 'oct | pak | flow'];

    var xmlhttp;
    
    if (window.XMLHttpRequest){
      
        xmlhttp=new XMLHttpRequest();
      
    }
    
    else{
      
      xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
      
    }
    
    xmlhttp.onreadystatechange=function(){

        if (xmlhttp.readyState==4 && xmlhttp.status==200){

            temp = xmlhttp.responseText;

            var top = temp.split("#top100");

            if(top.length > 1){

                topHTML = "<br><br><div class='row top100'><div class='col-md-6 col-md-offset-3'><h1>Top 100<span class='col-md-2 badge pull-right alert-warning'><h4>Packets</h4></span> <span class='badge pull-right alert-success col-md-2'><h4>Octects</h4></span> <span class='badge pull-right alert-info col-md-2 col-md-offset-1'><h4>Flows</h4></span></h1><br><ul class='list-group'>";

                for(i=1; i < top.length; i++){

                    tmp = top[i].split(" ");

                    topHTML += "<li class='list-group-item top100-entry'>"+tmp[1]+"<span class='badge alert-warning'>"+tmp[4]+"</span><span class='badge pull-right alert-success'>"+tmp[3]+"</span><span class='badge pull-right alert-info'>"+tmp[2]+"</span></li>"

                }

                topHTML += "</ul></div></div>";

            }

            else{

                topHTML = "<br><br><div class='row top100'><div class='col-md-6 col-md-offset-3'><h1>"+top[0]+"</h1></div></div>";

            }

            document.getElementById("content").innerHTML = topHTML;
            
        }
      
    }
    
    if((entity.match('ports') || entity.match('net') || entity.match('net2net')) && (type.match('oct') || type.match('pak') || type.match('flow')) && id.match('^[1-9][0-9]*$')){

        xmlhttp.open("GET","../MenuViews/Top100.cgi?uid="+uid+"&sid="+sid+"&remote="+remote+"&entity="+entity+"&type="+type+"&id="+id.toString(),true);
    
        xmlhttp.send();

    }

}
