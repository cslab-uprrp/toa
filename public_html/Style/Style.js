$(document).ready(function(){

	$('div#menu_content').hide();

	$('div#port_menu').hide();

	$('div#port_net_menu_container').hide();

	$("#p").toggle(function(){

		$("#port_menu").fadeIn();

	}, function(){

		$("#port_menu").fadeOut();

	});

	$("div#top_menu_button").toggle(function(){

		$("div#menu_content").fadeIn("fast");

		$("div#menu_content").animate({width:'100px', height:'520px'}, "slow");

	},function(){

		$("div#menu_content").fadeOut("slow");

		$("div#menu_content").animate({width:'0px', height:'0%'}, "slow");

		$('#port_net_menu_container').fadeOut();

	});

	$("div#bottom_menu_button").toggle(function(){

		$("div#port_net_menu_container").fadeOut();

		$("div#menu_content").fadeIn("fast");

		$("div#menu_content").animate({width:'400px', height:'520'}, "slow");

	},function(){

		$("div#menu_content").fadeOut("slow");

		$("div#menu_content").animate({width:'0px', height:'0%'}, "slow");

		$('#port_net_menu_container').fadeOut();

	});

});