$(function() {
	function handleClickEvents() {
		$(".edit").click(function(e) {
			e.preventDefault();
			prevData = $(this).parent().prev().val();
			$(this).parent().parent().hide();
			$(this).parent().parent().next().show();
			if ($(this).parent().parent().next().find("input")[1]) {
				$(this).parent().parent().next().find("input")[0].focus();
			}
			else {
				$(this).parent().parent().next().find("select")[0].focus();
			}
			$(".edit").replaceWith("<span class='edit muted'>Edit</span>");
			$(".change-password").replaceWith("<span class='change-password muted'>Change password</span>");
			$("table").removeClass("table-hover");
		});
		$(".edit-all").click(function(e) {
			e.preventDefault();
			$(".edit").parent().parent().hide();
			$(".in-edit").show();
			//$(".uneditable").css({"background-color": "#EDEDED"});
			$(".save-all").show();
			$(".partial-submit").replaceWith("<span class='muted partial-submit'>Edit</span>");
			$("table").removeClass("table-hover");
			$(".edit-all-wrapper").addClass("muted");
			$(".change-password").replaceWith("<span class='change-password muted'>Change password</span>");
		});
	}
	$(".user-info-form").submit(function() {
		var csrftoken = $.cookie('csrftoken');
		$.ajax({
			data: $(this).serialize(),
			type: $(this).attr('method'),
			url: $(this).attr('action'),
			beforeSend: function(xhr) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			},
			success: function(response) {
				console.log(response[0].fields);
				$(".in-edit").hide();
				$(".edit").replaceWith("<a class='edit' href='#'>Edit</a>");
				$(".edit").parent().parent().show();
				$(".change-password").replaceWith("<a class='change-password' href='{% url 'auth_password_change' %}'>Change password</a>");
				$("table").addClass("table-hover");
				$(".save-all").hide();
				$(".partial-submit").replaceWith("<input class='btn btn-info partial-submit' type='submit' value='Save'>");
				handleClickEvents();
			}
		});
		return false;
	});
	handleClickEvents();
});

	/*
	Sorry, had to comment this out right now.  Causing a lot of errors.

	$('#dot3').dotdotdot({
		after: 'a.more',
		height: '50px',
		watch: true
	});

	function initializeGoogleMaps() {
	  	var mapOptions = {
	    	zoom: 8,
	    	center: new google.maps.LatLng(44.4758, -73.2125),
	    	mapTypeId: google.maps.MapTypeId.ROADMAP
	  		},
	  		map = new google.maps.Map($('#map-canvas'), mapOptions);
	  	codeAddress();
	}

	google.maps.event.addDomListener(window, 'load', initializeGoogleMaps);

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
	    });
	}

	$("#dot3").bind("click", function() {
		if ($("#dot3").html() == "Read more") {
			var el = $('#dot3'),
    			curHeight = el.height(),
    			autoHeight = el.css('height', 'auto').height();
			el.height(curHeight).animate({height: autoHeight}, 1000);
		} else if ($("#dot3").html() == "Read Less") {
			$(".biodisplay").height(150);
			$("#dot3").html("Read more");
		} else {
			console.log("Yeahhhh, we got a problem...");
		}
	});

    $('.carousel').carousel({ });
    */