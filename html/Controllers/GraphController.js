function GraphView(label, type, filter, entity, portlabel, tolabel, width, height, admin, vgraphs, uid, sid, remote){

    var xmlhttp;

    var url = ""

    if(admin){

        url = "../GraphViews/MasterGrapherView.cgi?uid="+uid+"&sid="+sid+"&remote="+remote+"&label="+label+"&entity="+entity+"&type="+type+"&filter="+filter+"&portlabel="+portlabel+"&tolabel="+tolabel+"&w="+width+"&h="+height+"&views="+vgraphs

    }

    else{

        url = "Views/GraphViews/MasterGrapherView.cgi?uid="+uid+"&sid="+sid+"&remote="+remote+"&label="+label+"&entity="+entity+"&type="+type+"&filter="+filter+"&portlabel="+portlabel+"&tolabel="+tolabel+"&w="+width+"&h="+height+"&views="+vgraphs

    }

    if (window.XMLHttpRequest){// code for IE7+, Firefox, Chrome, Opera, Safari
                                
        xmlhttp = new XMLHttpRequest();
    
    }

    else{// code for IE6, IE5
                                                                  
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");

    }
                                                                                 
    xmlhttp.onreadystatechange=function(){
                                                                                                          
        if (xmlhttp.readyState==4 && xmlhttp.status==200){

            if(entity.match("device")){

                if(admin){

                    document.getElementById("content").innerHTML = "<br><br><br><center><div class='btn-group'><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'day', 'device', 'default', 'default', 'default', 'default', 1)\">Day</a><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'week', 'device', 'default', 'default', 'default', 'default', 1)\">Week</a><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'month', 'device', 'default', 'default', 'default', 'default', 1)\">Month</a><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'year', 'device', 'default', 'default', 'default', 'default', 1)\">Year</a></div><br><br><br>";

                }

                else{

                    document.getElementById("content").innerHTML = "<br><br><br><center><div class='btn-group'><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'day', 'device', 'default', 'default', 'default', 'default')\">Day</a><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'week', 'device', 'default', 'default', 'default', 'default')\">Week</a><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'month', 'device', 'default', 'default', 'default', 'default')\">Month</a><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'year', 'device', 'default', 'default', 'default', 'default')\">Year</a></div><br><br><br>";

                }


            }
            
            else if(entity == "port"){

                if(admin){

                    document.getElementById("content").innerHTML = "<br><br><br><center><div class='btn-group'><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'day', 'port', "+portlabel+", 'default', 'default', 'default', 1)\">Day</a><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'week', 'port', "+portlabel+", 'default', 'default', 'default', 1)\">Week</a><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'month', 'port', "+portlabel+", 'default', 'default', 'default', 1)\">Month</a><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'year', 'port', "+portlabel+", 'default', 'default', 'default', 1)\">Year</a></div><br><br><br>";                

                }

                else{

                    document.getElementById("content").innerHTML = "<br><br><br><center><div class='btn-group'><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'day', 'port', "+portlabel+", 'default', 'default', 'default')\">Day</a><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'week', 'port', "+portlabel+", 'default', 'default', 'default')\">Week</a><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'month', 'port', "+portlabel+", 'default', 'default', 'default')\">Month</a><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'year', 'port', "+portlabel+", 'default', 'default', 'default')\">Year</a></div><br><br><br>";                

                }

            }

            else if(entity == "net2net"){

                if(admin){

                    document.getElementById("content").innerHTML = "<br><br><br><center><div class='btn-group'><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'day', 'net2net', 'default', '"+tolabel+"', 'default', 'default', 1)\">Day</a><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'week', 'net2net', 'default', '"+tolabel+"', 'default', 'default', 1)\">Week</a><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'month', 'net2net', 'default', '"+tolabel+"', 'default', 'default', 1)\">Month</a><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'year', 'net2net', 'default', '"+tolabel+"', 'default', 'default', 1)\">Year</a></div><br><br><br>";

                }

                else{

                    document.getElementById("content").innerHTML = "<br><br><br><center><div class='btn-group'><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'day', 'net2net', 'default', '"+tolabel+"', 'default', 'default')\">Day</a><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'week', 'net2net', 'default', '"+tolabel+"', 'default', 'default', 1)\">Week</a><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'month', 'net2net', 'default', '"+tolabel+"', 'default', 'default', 1)\">Month</a><a class='btn btn-default btn-lg btn-graph-filter' onclick=\"GraphView('"+label+"', 'all', 'year', 'net2net', 'default', '"+tolabel+"', 'default', 'default', 1)\">Year</a></div><br><br><br>";

                }

            }

            var response = xmlhttp.responseText;

            var graphs = response.split("#graph");

            var title = "";

            if(type != "views"){

                if(entity == "device"){

                    title = label+" Interface Graphs by "+filter.charAt(0).toUpperCase() + filter.slice(1);

                    views = 'default';

                }

                else if(entity == "port"){

                    title = label+" Port "+portlabel+" Graphs by "+filter.charAt(0).toUpperCase() + filter.slice(1);

                    views = 'default';

                }

                else if(entity == "net2net"){

                    title = label+" to "+tolabel+" Graphs by "+filter.charAt(0).toUpperCase() + filter.slice(1);

                    views = 'default';

                }

                document.getElementById("content").innerHTML += "<div class='col-md-6 col-md-offset-3'><h1 class='pull-left'>"+title+"</h1></div>";

            }

            src = document.createElement('script');

            types = new Array('net', 'pak', 'flw', 'cpl');

            fltr = '';

            switch(filter){

                case 'day':

                    fltr = '1d';

                    break;

                case 'week':

                    fltr = '1w';

                    break;

                case 'month':

                    fltr = '1m';

                    break;

                case 'year':

                    fltr = '1a';

                    break;

            }

            tlabl = ''

            if(tolabel != 'default'){

                tlabl = "_"+tolabel;

            }

            else if(portlabel != 'default'){

                tlabl = "-p"+portlabel;

            }

            for(i=1; i<graphs.length;i++){

                if(admin == 1){

                    if(entity == "views"){

                        document.getElementById("viewer-body").innerHTML += "<div class='thumbnail graph-thumb-viewer col-md-6'><div class='graph' id='view"+i+"'></div></div></center>";

                        src.innerHTML += graphs[i]; 

                    }

                    else{

                        document.getElementById("content").innerHTML += "<div class='container-fluid'><div class='thumbnail graph-thumb col-md-6 col-md-offset-3'><div class='popover right fade in' id='viz"+i+"-popover' onclick='$(this).draggable();'> <h3 class='popover-title plugin-header'>Select Plugin <button type='button' class='close pull-right plugin-close' onclick=\"$('.popover').css('display', 'none');\" aria-hidden='true'>&times;</button></h3><div class='popover-content'><select id = 'APP_FILTER' class='form-control'><option value='cube'>Cube</option><option value='graph'>Graph</option></select><br><button id='viz"+i+"submit' class='btn btn-default btn-md pull-right btn-feature-bar' type='button'>Use Plugin</button><br><br></div></div><div class='graph' id='viz"+i+"'></div><div class='caption'><a onclick=\"AddListener('"+label+tlabl+"_"+fltr+types[i-1]+".js')\" href=# class='btn btn-default btn-lg btn-add-graph pull-right' data-toggle='modal' data-target='#AddGraphModal'>Add to View <i class='glyphicon glyphicon-plus'></i></a></div></div></div></center>";
                        
                        src.innerHTML += graphs[i];

                    }  

                }

                else{

                    document.getElementById("content").innerHTML += "<div class='thumbnail graph-thumb col-md-6 col-md-offset-3'><div class='graph' id='viz"+i+"'></div></div></center>";

                    src.innerHTML += graphs[i];

                }

            }

            document.body.appendChild(src);
                
        }
                                                                                                                                                                                  
    }

    if(entity == "views" && vgraphs == ""){                                                                            

        document.getElementById("viewer-body").innerHTML = "<br><br><br><center><h1>No Graphs in View<h1></center><br><br><br>";

    }

    else{

        xmlhttp.open("GET",url,true);

        xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");

        xmlhttp.send();

    }

}

function CleanViewer(){

    document.getElementById("viewer-body").innerHTML = "";

}

function AddListener(path){

    document.getElementById("GraphAdder").onclick = function(){AddGraphToView(path);};

}

function AddGraphToView(path){

    view = document.getElementById("views");

    vid = view.options[view.selectedIndex].value;

    var xmlhttp;

    if (window.XMLHttpRequest){// code for IE7+, Firefox, Chrome, Opera, Safari
                                
        xmlhttp = new XMLHttpRequest();
    
    }

    else{// code for IE6, IE5
                                                                  
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");

    }
                                                                                 
    xmlhttp.onreadystatechange=function(){
                                                                                                          
        if (xmlhttp.readyState==4 && xmlhttp.status==200){

            alert(xmlhttp.responseText);
                
        }
                                                                                                                                                                                  
    }

    xmlhttp.open("GET","../../Controllers/AddGraph2View.cgi?vid="+vid+"&graph_name="+path,true);
                     
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");

    xmlhttp.send();

}

function CustomGraphView(uid, sid, remote){

    try{

        label = document.getElementById("network");

        label = label.options[label.selectedIndex].value;

        types = document.getElementsByName("ftype");

        for(i=0; i<types.length;i++){

            if(types[i].checked){

                graphtype = types[i].value;

                break;

            }

        }

        checkbox = document.getElementsByName("checkboxoptions");

        checkbox_marked = ""

        for(i=0; i<checkbox.length;i++){

            if(checkbox[i].checked){

                checkbox_marked += "&checkbox_marked="+checkbox[i].value;

            }

        }

        d1 = document.getElementById("calendar1").value;

        d2 = document.getElementById("calendar2").value;

    }catch(e){

        label = 0;

        checkbox_marked = '';

        graphtype = '';

        d1 = '';

        d2 = '';

    }

    var xmlhttp;
    
    if (window.XMLHttpRequest){
      
        xmlhttp=new XMLHttpRequest();
      
    }
    
    else{
      
      xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
      
    }
    
    xmlhttp.onreadystatechange=function(){

        if (xmlhttp.readyState==4 && xmlhttp.status==200){

            var response = xmlhttp.responseText;

            var graphs = response.split("#graph");

            if(graphs.length > 1){

                src = document.createElement('script');

                document.getElementById("content").innerHTML = "<br><br><div class='col-md-6 col-md-offset-3'><h1 class='pull-left'>Custom Query Result</h1></div>"

                for(i=1; i<graphs.length;i++){

                    document.getElementById("content").innerHTML += "<div class='thumbnail graph-thumb col-md-6 col-md-offset-3'><div class='graph' id='viz"+i+"'></div></div></center>";

                    src.innerHTML += graphs[i];

                }

                document.body.appendChild(src);

            }

            else{

                document.getElementById("custom-query-status").innerHTML = response;

            }

        }
      
    }

    xmlhttp.open("GET","../GraphViews/CustomQueriesGrapher.cgi?uid="+uid+"&sid="+sid+"&remote="+remote+"&id="+label+"&graphtype="+graphtype+checkbox_marked+"&d1="+d1+"&d2="+d2,true);
    
    xmlhttp.send();

}

function P2PGraph(){

    var xmlhttp;

    var src = document.createElement('script');
    
    if (window.XMLHttpRequest){
      
        xmlhttp=new XMLHttpRequest();
      
    }
    
    else{
      
      xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
      
    }
    
    xmlhttp.onreadystatechange=function(){

        if (xmlhttp.readyState==4 && xmlhttp.status==200){

            //console.log(xmlhttp.responseText);

            src.innerHTML = xmlhttp.responseText;

        }

        document.body.appendChild(src);
      
    }

    xmlhttp.open("GET","Views/GraphViews/P2PView.cgi",true);
    
    xmlhttp.send();

}
