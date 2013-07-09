$(function() {
	/* Handle events */
	function handleEvents() {
		var autoValidate = null;
		$(".start-signup").submit(function(e) {
			var address = $(".start-email").val().replace(/ /g, ""),
				username;
			if ((address != "") && validateEmail(address)) {
				$(".username").val(address.substring(0, address.indexOf("@")));
				return true;
			}
			startSignupErr();
			$(".start-email").select();
			return false;
		});
		$(".start-email").keydown(function(e) {
			removeStartSignupErr();
			if (autoValidate != null) clearTimeout(autoValidate);
			autoValidate = setTimeout(function () {
				var address = $(".start-email").val().replace(/ /g, "");
				if (!validateEmail(address)) {
					startSignupErr();
				}
			}, 5000);
		});
	}

	function validateEmail(address) {
		var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;	
		return (regex.test(address));
	}

	function startSignupErr() {
		$(".start-submit").addClass("disable");
		$(".header-signup-button-wrap").addClass("disable");
	}

	function removeStartSignupErr() {
		$(".start-submit").removeClass("disable");
		$(".header-signup-button-wrap").removeClass("disable");
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
