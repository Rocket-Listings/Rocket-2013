$(function() {
	google.maps.visualRefresh = true;
	var mapOptions = {
		center: new google.maps.LatLng(44.5, -72.8), // burlington coords
		zoom: 10,
		mapTypeId: google.maps.MapTypeId.ROADMAP,
		disableDefaultUI: true,
		panControl: false,
		zoomControl: false,
		mapTypeControl: false,
		scaleControl: false,
		streetViewControl: false,
		overviewMapControl: false
	};
	var map = new google.maps.Map(document.getElementById("header-map"), mapOptions);
	$("#header-map-overlay").css('visibility', 'visible');

	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(gotLocation, noLocation);
	} else {
		console.log("Error: Old or non-compliant browser.");
	}

	function gotLocation(pos) {
		map.panTo(new google.maps.LatLng(pos.coords.latitude, pos.coords.longitude + 0.4));
	}
	function noLocation(error) { 
		console.log( "Maps error: " + error.code); 
	}
});
