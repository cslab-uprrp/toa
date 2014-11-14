$(document).ready(function(){
	$("#updwn").click(function(){
    		$("#main_content").fadeToggle(0);
		var menu_status_btn = $('#chlBtn').text() ;
		$("#chlBtn").text(
			(menu_status_btn == 'HIDE MENU'?'SHOW MENU':'HIDE MENU'));
	}),
    	$("#main_menu").hover(function(){
            	$(this).stop().css({"cursor" : "pointer"}) }),
    	$("#second_menu_btn").click(function(){
    	        $("#axis_menu").fadeToggle(0);}),
    	$("#second_menu_btn").hover(function(){
        	$(this).stop().css({"cursor" : "pointer"})}) ;
    
	$(function(){
	        $( "#datepicker" ).datepicker({ 
				minDate: -2000, maxDate: "0"
			});
	});

	    $(function(){
	        $('#timepicker').timepicker({showLeadingZero: true });
	    });
});

var srcIp = "",dstIp = "",src_pre = "0",dst_pre = "0",time="",inp_date ; // Stores the user input for do the parsing.
var index = 0 ; // variable to go over the flow_record list
var flow_records = [] ; // this list will hold the records of one flow
var particles = []; // stores particles.
var particleSystem = []; // holds all the particles.
var pMaterial = [] ; // This list holds the properties of each particle.
var container;
var projector ;
var camera, scene, renderer;
var cube, plane; 
var targetRotation = 0;
var targetRotationOnMouseDown = 0;
var mouseX = 0;
var mouseXOnMouseDown = 0;
var windowHalfX = window.innerWidth / 2, windowHalfY = window.innerHeight / 2;
var projector = new THREE.Projector(), raycaster = new THREE.Raycaster();
//var MyIFrame = document.getElementById("frm"),frmDoc = (MyIFrame.contentWindow || MyIFrame.contentDocument);
//if (frmDoc.document) frmDoc = frmDoc.document;
//var info = document.createElement( 'div' );
var srcfnList='';
var dstfnList='';

init();
animate();
			
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
		return  'index.cgi?srcIp='+srcIp+'&dstIp='+dstIp+'&src_pre='+src_pre+'&dst_pre='+dst_pre+'&time='+time+'&PARSE=1'+'&date='+inp_date+"&thold="+document.getElementById('opt').value+"&tvalue="+document.getElementById('threshold_size').value+'|'+document.getElementById('unit').value;

	}
	
}
var response;
function dspData(request_type)
{

	if (!validData(request_type))return ;
	clearCube() ;
	
	response=getResponse(getUrl(request_type));
	
	//console.log(response);
	//return ;
	if (parseInt(response)==-1){
		alert('Input_Error');
		return 0;
    }
	
	temp_list = response.split("\n") ; // List containing one connection at each position.
	// We fill the list containing all the traffic data. We iterate the list n-2 to eliminate the last two newlines.
    for (var i = 0 ; i < temp_list.length-2 ; i++) flow_records.push(temp_list[i].split(" ",5)) ;
	buildParticles() ; // We create and add particles inside the cube.

    setInterval(updateParticles,3000) ;
}

function CreateCube(width, height, depth,xc,yc,zc)
{
	var width_half = width / 2,
		height_half = height / 2,
		depth_half = depth / 2;
	
	var planes = [] ;
	var cube_color = [yc,xc,zc];

	planes.push(buildPlane( 'z', 'y', - 1, - 1, depth, height, width_half, [cube_color[0], cube_color[1], cube_color[0], cube_color[1]] )); // px
    planes.push(buildPlane( 'z', 'y',   1, - 1, depth, height, - width_half, [cube_color[0], cube_color[1], cube_color[0], cube_color[1]])); // nx
    planes.push(buildPlane( 'x', 'z',   1,   1, width, depth, height_half,[cube_color[1], cube_color[2], cube_color[1], cube_color[2]])); // py
    planes.push(buildPlane( 'x', 'z',   1, - 1, width, depth, - height_half, [cube_color[1], cube_color[2], cube_color[1], cube_color[2]])); // ny
    planes.push(buildPlane( 'x', 'y',   1, - 1, width, height, depth_half,[cube_color[0], cube_color[2], cube_color[0], cube_color[2]])); // pz
    planes.push(buildPlane( 'x', 'y', - 1, - 1, width, height, - depth_half,[cube_color[0], cube_color[2], cube_color[0], cube_color[2]])); // nz
  
	function buildPlane( u, v, udir, vdir, width, height, depth, colors) {
    		var w, ix, iy,
    		gridX =  1,
    		gridY =  1,
    		width_half = width / 2,
    		height_half = height / 2;

    		if ( ( u === 'x' && v === 'y' ) || ( u === 'y' && v === 'x' ) ) w = 'z';
    		else if ( ( u === 'x' && v === 'z' ) || ( u === 'z' && v === 'x' ) ){ 
            		w = 'y';
			gridY = 1;
        	} 
		else if ( ( u === 'z' && v === 'y' ) || ( u === 'y' && v === 'z' ) ) {
        		w = 'x';
       			gridX =  1;
  		}

		var gridX1 = gridX + 1,
		gridY1 = gridY + 1,
		segment_width = width / gridX,
		segment_height = height / gridY;
		var lines = [] ;
		var scope; // Variable to hold the dimensions and properties of each vector.
	

		/*********************first line****************************/
		// Creates the first material for the first two axis.
       	material = new THREE.LineBasicMaterial( { color: colors[0], opacity: 1, linewidth: 1}) ;										 
    	scope = new THREE.Geometry(); // geometry
   		var vector = new THREE.Vector3();
   		vector[ u ] = (0 * segment_width - width_half ) * udir;
   		vector[ v ] = (0 * segment_height - height_half ) * vdir;
   		vector[ w ] = depth;
   		falvector =vector;
   		scope.vertices.push(vector);

   		// We create the second vector and then append it to the vertices of the geometry.
   		vector = new THREE.Vector3();
   		vector[ u ] = (0 * segment_width - width_half ) * udir;
   		vector[ v ] = (1 * segment_height - height_half ) * vdir;
   		vector[ w ] = depth;
   		scope.vertices.push(vector);
       	lines.push(new THREE.Line(scope, material)) ;

       	/********************second line*****************************/
       	// We create a new material for the new geometry.
       	material = new THREE.LineBasicMaterial( { color:colors[1], opacity: 1, linewidth: 1}) ;
        scope = new THREE.Geometry();
       	scope.vertices.push(vector);
       	
   		var vector = new THREE.Vector3();
   		vector[ u ] = (1 * segment_width - width_half ) * udir;
   		vector[ v ] = (1 * segment_height - height_half ) * vdir;
   		vector[ w ] = depth;
   		scope.vertices.push(vector);
       	lines.push(new THREE.Line(scope, material)) ;

       	// Second vector of the second line.
   		material = new THREE.LineBasicMaterial( { color:colors[2], opacity: 1, linewidth: 1}) ;
   		scope = new THREE.Geometry();			  
   		scope.vertices.push(vector);
   		var vector = new THREE.Vector3();
   		vector[ u ] = (1 * segment_width - width_half ) * udir;
  		vector[ v ] = (0 * segment_height - height_half ) * vdir;
  	 	vector[ w ] = depth;
  	 	scope.vertices.push(vector);
  	 	lines.push(new THREE.Line(scope, material)) ;

  	 	/********************third line*****************************/
   		material = new THREE.LineBasicMaterial( { color: colors[3], opacity: 1, linewidth: 1}) ;
   		scope = new THREE.Geometry();
   		scope.vertices.push(vector);
       	scope.vertices.push( falvector ); // we append the first created vector.
       	lines.push(new THREE.Line(scope, material)) ;
       	return lines ;
	}
	return planes ;
}

// This function changes the color of the axis of the cube.
function renderCube(){
	var tmpParSys = particleSystem;// We make a copy of the particle system because the cube object will be removed(including particles)
	
	scene.remove(cube) ; // We remove the cube.
	material = new THREE.MeshBasicMaterial( { color: 0xffffff, wireframe: true,  opacity: 0 } )  ;
    material.transparent=true ;
    cube = new THREE.Mesh( new THREE.CubeGeometry( 300, 300, 300), material );
	cube.position.y = 175 ;				
	var xc= parseInt(document.getElementById('z_color_id').value),
	yc=parseInt(document.getElementById('y_color_id').value),
	zc=parseInt(document.getElementById('x_color_id').value);


	var planes = CreateCube(300,300,300,xc,yc,zc) ;
    var pln, lln ;
    pln = planes.length ;
    for(var i = 0; i < pln ; i++){
    	lln = planes[i].length ;
        for(var j = 0; j < lln; j++){
        	cube.add(planes[i][j]) ;
        }
    }    
     
  	particleSystem = tmpParSys ; 
	for (i = 0 ; i < particleSystem.length;i++) cube.add(particleSystem[i]) ;
    scene.add( cube );
}

// This function creates all the materials and elements of the canvas.
function init() {	
	container = document.createElement( 'div' );
	container.id='cube_canvas';
	document.body.appendChild( container );
	scene = new THREE.Scene();
	camera = new THREE.PerspectiveCamera( 90, window.innerWidth / window.innerHeight, 1, 1200 );
	camera.position.y = 150;
	camera.position.z = 400;
	scene.add( camera );

// Cube
	material = new THREE.MeshBasicMaterial( { color: 0xffffff, wireframe: true,  opacity: 0 } )  ;
	//material = new THREE.MeshBasicMaterial( {color: 0x000000,transparent:true,wireframe:true} )  ;
	material.transparent=true ;                                               
	cube = new THREE.Mesh( new THREE.CubeGeometry( 300, 300, 300), material );
	cube.position.y = 175 ;
	

	var planes = CreateCube(300,300,300,0,0,0) ;
	
	var i, j ;
	var pln, lln ;
	pln = planes.length ;
	for(i = 0; i < pln ; i++){
		lln = planes[i].length ;
        	for(j = 0; j < lln; j++){
			cube.add(planes[i][j]) ;
		}
	}	
	// Add cube to the scene
	scene.add( cube );
	// Plane
	plane = new THREE.Mesh( new THREE.PlaneGeometry( 300, 300), new THREE.MeshBasicMaterial( { color: 0xe8e8e8 } ) );
	plane.rotation.x =  -90 * ( Math.PI / 180 );
	scene.add( plane ) ;
	renderer = new THREE.WebGLRenderer();
	renderer.setSize( window.innerWidth, window.innerHeight);
	renderer.setClearColor(0xffffff, 1);
	window.addEventListener( 'resize', onWindowResize, false );
	container.appendChild( renderer.domElement );

}

// This function executes when the windows resize and adjust the elements on the canvas.
function onWindowResize() {
	windowHalfX = window.innerWidth / 2;
	windowHalfY = window.innerHeight / 2;
	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();
	renderer.setSize( window.innerWidth, window.innerHeight );
}

// This function resets the elements of the cube to 're-display' the points.
function clearCube()
{

	// Here we remove all the points contained in the cube.
	for (var p = particles.length-1 ; p >= 0 ; p--){
       	cube.remove(particleSystem[p]);
		pMaterial.splice(p,1);
		particles.splice(p,1);
		particleSystem.splice(p,1);
	}

	while(flow_records.length!=0) flow_records.pop() ; 
	index = 0 ; // index reset
	renderer.render(scene, camera) ;
}	
function scroll(evt){evt.preventDefault;}
// Event Listener to show input results and manipulate the cube.		
function keyDown(event){
	var aeId=document.activeElement.id;
	if (aeId=='srcIp'||aeId=='dstIp'){
		if (document.getElementById(aeId).value == "") {
			document.getElementById(emId(aeId)).style.display='none';
			document.getElementById(document.activeElement.id).parentNode.removeAttribute('class','control-group error');
		}	
		var html = "The Ip " + '"' + document.getElementById(aeId).value + '" is not a valid input.';
        	document.getElementById(emId(aeId)).innerHTML=html ;
	}
}

function keyPress(event){ 
	if (event.keyCode==32) event.returnValue=false;
}

// This function shrinks the size of the particles.
function updateParticles(){
	for(var p = pMaterial.length -1; p >= 0; p--){
		pMaterial[p].size -= 2 ;
		if (pMaterial[p].size == 0){
			cube.remove(particleSystem[p]);
			pMaterial.splice(p,1);
			particles.splice(p,1);
			particleSystem.splice(p,1); 
		}
	}
	buildParticles() ;
	renderer.render(scene, camera) ;
}

// Ajax request: This function request data to the server.
function getResponse (url){	
	var xmlhttp = new XMLHttpRequest(); // a http object to execute the request.
	xmlhttp.open("POST",url,false); // We define the kind of request.
	xmlhttp.send(); // The request is sent to the server side.	
	return xmlhttp.responseText ; // We return the server response.
}

function pcolor() { 
	return ((parseInt(flow_records[index][4]) == 1) ? 0xff0000 : 0x1371ff);
}
			
// This function creates a set of points to display them in the cube.		
function buildParticles(){	

	var src_prefix = parseInt(src_pre) ;
	var dst_prefix = parseInt(dst_pre) ;
	if (flow_records.length==0) return ; // The function ends if the list containing the data is empty.	
	var time_index=0;
	//var vertex = new THREE.Vector3();
	var ratepos;
	// Now, we are going to display all the points that have the same unix time of time_index.
	while (time_index != 500) {	
		particles.push(new THREE.Geometry()) ;
		
		// We create the points properties and add it to a list of materials.
		pMaterial.push(new THREE.ParticleBasicMaterial({color:((parseInt(flow_records[index][4]) == 1) ? 0xff0000 : 0x1371ff) , size:6}));
		
		var vertex = new THREE.Vector3();
		ratepos = parseFloat(flow_records[index][2])/Math.pow(2,32-dst_prefix);
		vertex.x = (ratepos-Math.floor(ratepos)) * 300-150;
		vertex.y = ( parseFloat(flow_records[index][3])*300.0)/65536.0 - 150;
		ratepos=parseFloat(flow_records[index][1])/Math.pow(2,32-src_prefix);
        vertex.z =  (ratepos-Math.floor(ratepos)) * 300-150;
        particles[particles.length-1].vertices.push(vertex) ;

		// We add the particle to a new particle system.
		particleSystem.push(new THREE.ParticleSystem(particles[particles.length-1], pMaterial[pMaterial.length-1])) ;
                    	
		// We add the particle system that we have created to the cube. Note that we use the last element of the particleSystem
		// which contain the newest particle added to the system. 
		
		cube.add(particleSystem[particleSystem.length-1]) ;
		index++ ; // We update the global index.
		time_index++;
		// if the index is egual to the length of the list containing all the traffic info, means that all the points were displayed.
		if (index == flow_records.length) {
			index = 0 ; // We reset the index to continue displaying points.
			break ; 
		}
		
	}

}
					

document.addEventListener( 'mousedown', onDocumentMouseDown, false );
document.addEventListener("keyup",keyDown,false);
document.addEventListener("keypress",keyPress,false);
document.addEventListener( 'touchstart', onDocumentTouchStart, false );

function onDocumentMouseDown( event ) {
	var vector = new THREE.Vector3( ( event.clientX / window.innerWidth ) * 2 - 1, - ( event.clientY / window.innerHeight ) * 2 + 1, 0.5 );
	projector.unprojectVector( vector, camera );
	raycaster.set( camera.position, vector.sub( camera.position ).normalize() );
	var intersects = raycaster.intersectObjects( scene.children );
	if ( intersects.length > 0 ){
		event.preventDefault() ;
		document.addEventListener( 'mousemove', onDocumentMouseMove, false );
		document.addEventListener( 'mouseup', onDocumentMouseUp, false );
		//document.addEventListener( 'mouseout', onDocumentMouseOut, false );
	}
	mouseXOnMouseDown = event.clientX - windowHalfX;
	targetRotationOnMouseDown = targetRotation;
}

// Detects when the mouse click over the cube and try to move it.
function onDocumentMouseMove( event ) {
	mouseX = event.clientX - windowHalfX;
	targetRotation = targetRotationOnMouseDown + ( mouseX - mouseXOnMouseDown ) * .003;
}

// **Detects when the user click the cube and 'drag the cube up' and move the mouse out of the cube.
function onDocumentMouseUp( event ) {
	document.removeEventListener( 'mousemove', onDocumentMouseMove, false );
	document.removeEventListener( 'mouseup', onDocumentMouseUp, false );
	document.removeEventListener( 'mouseout', onDocumentMouseOut, false );
}

// **Detects when the user quits the mouse over the cube.
function onDocumentMouseOut( event ) {
	document.removeEventListener( 'mousemove', onDocumentMouseMove, false );
	document.removeEventListener( 'mouseup', onDocumentMouseUp, false );
	document.removeEventListener( 'mouseout', onDocumentMouseOut, false );
}

// ** Detects when the user click the cube.
function onDocumentTouchStart( event ) {
	if ( event.touches.length == 1 ) {
		event.preventDefault();
		mouseXOnMouseDown = event.touches[ 0 ].pageX - windowHalfX;
		targetRotationOnMouseDown = targetRotation;
	}
}

function onDocumentTouchMove( event ) {

	if ( event.touches.length == 1 ) {
		event.preventDefault();
		mouseX = event.touches[ 0 ].pageX - windowHalfX;
		targetRotation = targetRotationOnMouseDown + ( mouseX - mouseXOnMouseDown );
	}
}


function animate() {
	requestAnimationFrame( animate );
	render();
	/*stats.update();*/
}
					
function render() {
	// Note:if you multiply ( targetRotation - cube.rotation.y ) by any number, it will allow the cube to mantain sppining after you move it.								
	plane.rotation.z = cube.rotation.y += ( targetRotation - cube.rotation.y ) ; 
	if ( camera.position.z == 828 ) camera.position.z -=8;
	renderer.render( scene, camera );
						
}

function getIpOctet(ip,octet_numbers){
	if (ip.lengt=0||octet_numbers>4||octet_numbers<0)return ""
	ip=ip.split('.'),newIp="",ip_index=0;
	for(i=0;i<octet_numbers;i++){
		newIp+=ip[i]+(ip_index!=octet_numbers-1?".":"");
		ip_index+=1;
	}
	return newIp;
}

function emId (aeId){return (aeId=='srcIp'?'s_em':'d_em');}
window.onload = function(){
	$('#axis_menu').hide(0);
	document.getElementById('srcIp').focus();
	document.getElementById('s_em').style.display='none';
	document.getElementById('x_Axis').style.backgroundColor = 'black';
	document.getElementById('y_Axis').style.backgroundColor = 'black';
	document.getElementById('z_Axis').style.backgroundColor = 'black';
	inp_date = document.getElementById('flow_date').value ;
	
	if (inp_date.length == 19 || inp_date.length == 8){
		//console.log(inp_date);
		dspData(0);
	}
	
}

