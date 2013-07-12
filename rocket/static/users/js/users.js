$(function() {
	// USER MANAGEMENT JS
	filepicker.setKey('ATM8Oz2TyCtiJiHu6pP6Qz');
	function handleClickEvents() {
		$(".edit").click(function(e) {
			e.preventDefault();
			// Crazy selectors to hide the normal view and show/focus the right input
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
			$(".active").hide();
			$(".inactive").show();
			$("table").removeClass("table-hover");
		});
		$(".edit-all").click(function(e) {
			e.preventDefault();
			$(".active").hide();
			$(".inactive").show();
			$(".partial-submit").hide();
			$(".edit-all").hide();
			$(".save-all").show();
			$(".edit").parent().parent().hide();
			$(".partial-submit").replaceWith("<span class='muted partial-submit'>Edit</span>");
			$(".in-edit").show();
			$("table").removeClass("table-hover");
		});
	}
	$(".change-propic").click(function(e) {
		e.preventDefault();
		filepicker.pick({
			mimetype: "image/*",
			multiple: false,
			services: ['COMPUTER', 'URL', 'FACEBOOK', 'DROPBOX']
		},
		function(InkBlob) {
			filepicker.convert(InkBlob, {
				width: 200, 
				height: 200,
				format: 'png',
				fit: 'crop',
				align: 'faces'
			},
			{
				location: 'S3',
				path: '/propics/' + $(".username").text() + '.png'
			},
			function(NewBlob) {
				$(".propic-url").val(NewBlob.url);
				$(".user-info-form").submit();
			},
			function(FPError) {
				console.log(FPError);
			},
			function(percent) {
				if (percent != 100) {
					$(".loading-overlay").show();
				}
			});
		},
		function(FPError) {
			console.log(FPError);
		});
	});
	$(".get-location").click(function(e) {
		e.preventDefault();
		if (window.navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(function (position) {
				var lat 	 = position.coords.latitude,
					lng 	 = position.coords.longitude,
					latlng 	 = new google.maps.LatLng(lat, lng),
					geocoder = new google.maps.Geocoder();
				geocoder.geocode({'latLng': latlng}, function(results, status) {
					if (status == google.maps.GeocoderStatus.OK) {
						if (results[1]) {
							$(".location").val(results[4].formatted_address);
						}
						else {console.log("No reverse geocode results.")}
					}
					else {console.log("Geocoder failed: " + status)}
				});
			},
			function() {console.log("Geolocation not available.")});
		}
	});
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
				if (response.profile) {
					$(".in-edit").hide();
					$(".edit").parent().parent().show();
					$(".inactive").hide();
					$(".active").show();
					$("table").addClass("table-hover");
					$(".save-all").hide();
					$(".edit-all").show();
					$(".errors").hide();
					$(".partial-submit").replaceWith("<input class='btn btn-info partial-submit' type='submit' value='Save'>");
					insertNewValues(response);
				}
				else {
					showError(response);
				}
				handleClickEvents();
			}
		});
		return false;
	});
	function insertNewValues(data) {
		for (key in data) {
			var tag = $("." + key.toString());
			if ((key !== "nameprivate") && (key !== "locationprivate")  && (key !== "propic")) {
				if (tag.is("td")) {
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
			if (key.toString() === "propic") {
				$(".propic > div.propic-loading-wrapper > img").attr("src", data[key]);
				$(".loading-overlay").hide();
			}
		}
	}

	// Only handles click events for edit-all and edit
	handleClickEvents();

	// PROFILE JS
	// formatting (uses autoellipsis.js)
	//$(".profile-listing-description").ellipsis();

	// Handle the comment form
	$(".comment-form").submit(function() {
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
					insertNewComment(response[0].fields);
					$("input:not(input[type='submit']), textarea").val("");
					$(".errors").hide();
					$(".no-comment").hide();
				}
				else {
					showError(response);
				}
			}
		});
		return false;
	});

	function insertNewComment(data) {
		var newComment = '<tr><td><ul class="inline clearfix"><li><h4>' + data.title + '</h4></li>';
			newComment += '<li><h6>By: ' + data.name + '</h6></li>';
			newComment += '<li><h6 class="muted">' + data.date_posted + '</h6></li></ul>';
			newComment += '<p style="padding-left: 10px">' + data.comment + '</p></td></tr>';
		$(".comment-body").prepend(newComment);
	}

	// Used for comment form and user info AJAX responses
	function showError(response) {
		var errors = $(".errors"),
		dismissError = '<a href="#" class="close" data-dismiss="alert">&times;</a>';
		//errors.html(dismissError);  // Add back in for a dismiss error button, but then need to recreate the ".errors" div
		errors.html("");
		for (key in response) {
			errors.append(" <strong class='capital'>" + key + ": </strong> " + response[key] + "<br>");
		}
		errors.show();
	}
  	window.fbAsyncInit = function() {
  	FB.init({
    	appId      : '279057228903179', // App ID
    	// channelUrl : 'file://localhost/Users/olindavis/Rocket-Listings-Django/apps/users/templates/channel.html', // Channel File
    	status     : true, // check login status
    	cookie     : true, // enable cookies to allow the server to access the session
    	xfbml      : true  // parse XFBML
  	});

  	// Here we subscribe to the auth.authResponseChange JavaScript event. This event is fired
  	// for any authentication related change, such as login, logout or session refresh. This means that
  	// whenever someone who was previously logged out tries to log in again, the correct case below 
  	// will be handled. 
  	FB.Event.subscribe('auth.authResponseChange', function(response) {
  		// Here we specify what we do with the response anytime this event occurs. 
    	if (response.status === 'connected') {
      	// The response object is returned with a status field that lets the app know the current
      	// login status of the person. In this case, we're handling the situation where they 
      	// have logged in to the app.
      	testAPI();
    	} else if (response.status === 'not_authorized') {
      		// In this case, the person is logged into Facebook, but not into the app, so we call
      		// FB.login() to prompt them to do so. 
      		// In real-life usage, you wouldn't want to immediately prompt someone to login 
      		// like this, for two reasons:
      		// (1) JavaScript created popup windows are blocked by most browsers unless they 
      		// result from direct interaction from people using the app (such as a mouse click)
      		// (2) it is a bad experience to be continually prompted to login upon page load.
      	FB.login();
    	} else {
      		// In this case, the person is not logged into Facebook, so we call the login() 
      		// function to prompt them to do so. Note that at this stage there is no indication
      		// of whether they are logged into the app. If they aren't then they'll see the Login
      		// dialog right after they log in to Facebook. 
      		// The same caveats as above apply to the FB.login() call here.
      	FB.login();
    	}
  	});
  	};

  	// Load the SDK asynchronously
  	(function(d){
   		var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
   		if (d.getElementById(id)) {return;}
   		js = d.createElement('script'); js.id = id; js.async = true;
   		js.src = "//connect.facebook.net/en_US/all.js";
   		ref.parentNode.insertBefore(js, ref);
  	}(document));

  	// Here we run a very simple test of the Graph API after login is successful. 
  	// This testAPI() function is only called in those cases. 
  	function testAPI() {
    	console.log('Welcome!  Fetching your information.... ');
    	FB.api('/me', function(response) {
    		console.log('Good to see you, ' + response.name + '.');
    	});
  	}
  	function collect_facebook_info() {
  		
  	}
});

