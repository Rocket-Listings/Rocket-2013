$(function() {

	/* Handle events */
	function handleEvents() {
		$(".start-submit").click(signupStartHandler);
		$(".start-email").keypress(function(e) {
			if ((e.keyCode || e.which) == '13') {
				e.preventDefault();
				$(".start-submit").click();
			}
		});
	}

	/* Process the start of the signup */
	function signupStartHandler(e) {
		e.preventDefault();
		var address = $(".start-email").val().replace(/ /g, ""),
			username;
		if ((address != "") && validateEmail(address)) {
			$(".username").val(address.substring(0, address.indexOf("@")));
			$(".start-signup").submit();
		}
		else {
			signupErr("start-signup-error", "Please enter a valid email address.");
			$(".start-email").select();
			$(".start-email").keypress(function(e) {
				if ((e.keyCode || e.which) != '13') {
					removeStartSignupErr();
				}
			});
		}
	}

	function validateEmail(address) {
		var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
		if (regex.test(address)) return true;
		else return false;
	}

	function signupErr(classSelector, msg) {
		var selector = "." + classSelector;
		$(selector).html(msg);
	}

	function removeStartSignupErr() {
		$(".start-signup-error").html("&nbsp;");
	}

	handleEvents();

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
