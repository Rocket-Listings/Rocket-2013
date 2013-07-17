{% load static from staticfiles %}

$(function() {
	// SETTINGS JS
	filepicker.setKey('ATM8Oz2TyCtiJiHu6pP6Qz');

	$(".edit").click(function (e) {
		e.preventDefault();
		var field = $(this).parent().prev().children().filter(":first");
		field.focus().val(field.val());
	});
	$("input, textarea, select").focus(function () {
		$(this).parent().parent().addClass("selected");
	})
	.blur(function () {
		$(this).parent().parent().removeClass("selected");
	})
	.keydown(function (e) {
		var keyCode = (e.keyCode ? e.keyCode : e.which);
		if (keyCode === 27) {
			$(this).blur();
		}
	});
	$(".change-propic").click(function (e) {
		e.preventDefault();
		filepicker.pick({
			mimetype: "image/*",
			multiple: false,
			services: ['COMPUTER', 'URL', 'FACEBOOK', 'DROPBOX']
		},
		function (InkBlob) {
			filepicker.convert(InkBlob, {
				width  : 200, 
				height : 200,
				format : 'png',
				fit    : 'crop',
				align  : 'faces'
			},
			{
				location: 'S3',
				path: '/propics/' + $(".username").text() + '.png'
			},
			function (NewBlob) {
				$(".propic-url").val("https://s3.amazonaws.com/test_filepicker/" + NewBlob.key);
				$(".user-info-form").submit();
			},
			function (FPError) {
				console.log(FPError);
			},
			function (percent) {
				if (percent != 100) {
					$(".loading-overlay").show();
				}
			});
		},
		function (FPError) {
			console.log(FPError);
		});
	});
	$(".get-location").click(function (e) {
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
							for (var i = 0; i < results.length; i++) {
								if (results[i].types[0] === "locality") {
									var city = results[i].address_components[0].short_name;
									var state = results[i].address_components[2].short_name;
									$("input[name='location']").val(city + ", " + state);
								}
							}
						}
						else {console.log("No reverse geocode results.")}
					}
					else {console.log("Geocoder failed: " + status)}
				});
			},
			function() {console.log("Geolocation not available.")});
		}
	});
	$("form").submit(function() {
		if (!$("save-all").hasClass("disabled")) {
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
						$(".errors").hide();
						insertNewValues(response);
					}
					else {
						showError(response);
					}
				}
			});
		}
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

	// FACEBOOK ACTIONS
	$('.btn-fb').click(function() {
		FB.getLoginStatus(function (response) {
			if (response.status === 'connected') {
				fbProfileFill();
			}
			else {
				FB.login(function (response) {
					if (response.status === 'connected') {
						fbProfileFill();
					}
					else {
						console.log('User cancelled login action.');
					}
				}, {perms:'email,user_location'});
			}
		});
	});

	function fbProfileFill() {
		FB.api('/me', function (response) {
			$("input[name='name']").val(response.name);
			$("input[name='email']").val(response.email);
			$("input[name='location']").val(response.location.name);
			FB.api('/me/picture?width=200&height=200&type=square', function (response) {
				if (!response.data.is_silhouette) {
					$("input[name='propic-url']").val(response.data.url);
					$('form').submit();
				}
			});
		});
	}

	// PROFILE JS

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
		errors.html("");
		for (key in response) {
			errors.append(" <strong class='capital'>" + key + ": </strong> " + response[key] + "<br>");
		}
		errors.show();
	}
});

//  FACEBOOK INIT CODE
window.fbAsyncInit = function() {
  	FB.init({
    	appId      : '279057228903179', // App ID
    	channelUrl : '{% static "/users/channel.html" %}', // Channel File
    	status     : true, // check login status
    	cookie     : true, // enable cookies to allow the server to access the session
    	xfbml      : true  // parse XFBML
  	});
};

// Load the Facebook SDK asynchronously
(function(d){
	var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
	if (d.getElementById(id)) {return;}
	js = d.createElement('script'); js.id = id; js.async = true;
	js.src = "//connect.facebook.net/en_US/all.js";
	ref.parentNode.insertBefore(js, ref);
}(document));
