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
			else if ($(this).parent().parent().next().find("select")[0]) {
				$(this).parent().parent().next().find("select")[0].focus();
			}
			else {
				$(this).parent().parent().next().find("textarea")[0].focus();
			}
			$(".edit").replaceWith("<span class='edit muted'>Edit</span>");
			$(".change-password").replaceWith("<span class='change-password muted'>Change password</span>");
			$("table").removeClass("table-hover");
		});
		$(".edit-all").click(function(e) {
			e.preventDefault();
			$(".edit-all").hide();
			$(".edit").parent().parent().hide();
			$(".in-edit").show();
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
				if (response[0]) {
					$(".in-edit").hide();
					$(".edit").replaceWith("<a class='edit' href='#'>Edit</a>");
					$(".edit").parent().parent().show();
					$(".change-password").replaceWith("<a class='change-password' href='{% url 'auth_password_change' %}'>Change password</a>");
					$("table").addClass("table-hover");
					$(".save-all").hide();
					$(".edit-all").show();
					$(".errors").hide();
					$(".partial-submit").replaceWith("<input class='btn btn-info partial-submit' type='submit' value='Save'>");
					insertNewValues(response[0].fields);
				}
				else {
					var errors = $(".errors"),
						dismissError = '<a href="#" class="close" data-dismiss="alert">&times;</a>';
					//errors.html(dismissError);
					errors.html("");
					for (key in response) {
						errors.append("<strong class='capital'>" + key + ": </strong>" + response[key] + "<br>");
					}
					errors.show();
				}
				handleClickEvents();
			}
		});
		return false;
	});
	function insertNewValues(data) {
		for (key in data) {
			var tag = $("." + key.toString())
			console.log(key, tag.is("td"));
			if (tag.is("td") && (tag.html() !== "Private") && (tag.html() !== "Public")) {
				var tdTag = $("td." + key.toString());
				tdTag.html(data[key]);
				if (tdTag.hasClass("muted")) tdTag.removeClass("muted");
				if ((data[key] === "") || (data[key] === null)) {
					tdTag.addClass("muted");
					if (tdTag.hasClass("name")) tdTag.html("Add a name to your profile");
					if (tdTag.hasClass("phone")) tdTag.html("Add a phone number to your profile");
					if (tdTag.hasClass("bio")) tdTag.html("Add a bio to your profile");
					if (tdTag.hasClass("location")) tdTag.html("Add a default location for your listings");
					if (tdTag.hasClass("default_category")) tdTag.html("Add a default category for your listings");
					if (tdTag.hasClass("default_listing_type")) tdTag.html("Add a default listing type");
				}
			}
			if (tag.is("input") && !tag.is("option")) {
				tag.val(data[key]);
			}
			if (tag.is("textarea")) {
				$("textarea.bio").html(data[key]);
			}
			if (key.toString() === "nameprivate") {
				if (data[key] === true) tag.html("Private");
				else tag.html("Public");
			}
			if (key.toString() === "locationprivate") {
				if (data[key] === true) tag.html("Private");
				else tag.html("Public");
			}
			if (key.toString() === "name") {
				if (data[key] !== "") $("h3.name").html(data[key] + "'s info");
				else {
					var username = $(".username > code").html();
					$("h3.name").html(username + "'s info").removeClass("muted");
				}
			}
		}
	}
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