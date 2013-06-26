$(function() {

	/* Process the start of the signup */
	function signupStartHandler() {
		var address = $(".start-email").val().replace(/ /g, ""),
			username;
		if ((address != "") && validateEmail(address)) {
			username = address.substring(0, address.indexOf("@"));
		}
		else {
			signupErr("start-signup-error", "Please enter a valid email address.");
			$(".start-email").select();
			$(".start-email").keypress(removeSignupErr);
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

	function removeSignupErr() {
		$(".start-signup-error").html("");
	}

	$(".start-submit").click(signupStartHandler);
	$(".start-email").trigger("focus");

	$('#dot3').dotdotdot({
		after: 'a.more',
		height: '50px',
		watch: true
	})

	function initializeGoogleMaps() {
  	var mapOptions = {
    	zoom: 8,
    	center: new google.maps.LatLng(44.4758, -73.2125),
    	mapTypeId: google.maps.MapTypeId.ROADMAP
  		};
  	var map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);
  	codeAddress();
	}

	google.maps.event.addDomListener(window, 'load', initializeGoogleMaps)


	function codeAddress() {
	console.log(location);
    geocoder.geocode( { 'address': location}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        map.setCenter(results[0].geometry.location);
        var marker = new google.maps.Marker({
            map: map,
            position: results[0].geometry.location
        });
      } else {
        alert("Geocode was not successful for the following reason: " + status);
      }
    })
}


	$("#dot3").bind("click", function() {
		if ($("#dot3").innerHTML = "Read more") {
			var el = $('#dot3'),
    		curHeight = el.height(),
    		autoHeight = el.css('height', 'auto').height();
			el.height(curHeight).animate({height: autoHeight}, 1000);
		} else if ($("#dot3").innerHTML = "Read Less") {
			$(".biodisplay").height(150);
			$("#dot3").innerHTML = "Read more";
		} else
			console.log("Yeahhhh, we got a problem...");
	})


	$(document).ready(function(){
    $('.carousel').carousel({
    });
  })




});