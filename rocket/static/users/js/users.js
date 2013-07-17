{% load static from staticfiles %}

$(function() {
	// SETTINGS JS
	var initialInput = getInput('input');
	var initialSelect = getInput('select');
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
	$("input:not(input[type='submit']), textarea").keyup(function() {
		var save = $(".save-all");
		if (inputChanged(getInput('input'))) {
			save.removeClass("disabled");
		}
		else {
			save.addClass("disabled");
		}
	});
	$("select").change(function() {
		var save = $(".save-all");
		if (inputChanged(getInput('select'))) {
			save.removeClass("disabled");
		}
		else {
			save.addClass("disabled");
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
									$("form").submit();
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
						$(".save-all").addClass("disabled");
						$("input, textarea, select").blur();
						initialInput = getInput('input');
						initialSelect = getInput('select');
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
		$("input[name='name']").val(data['name']);
		$("input[name='email']").val(data['email']);
		$("input[name='phone']").val(data['phone']);
		$("input[name='location']").val(data['location']);
		$("input[name='bio']").html(data['bio']);
		if (data['nameprivate'] === true) {
			$("select['nameprivate']").children().filter("option[value='True']").attr('selected', 'true');
			$("select['nameprivate']").children().filter("option[value='False']").attr('selected', 'false');
		}
		else {
			$("select['nameprivate']").children().filter("option[value='True']").attr('selected', 'false');
			$("select['nameprivate']").children().filter("option[value='False']").attr('selected', 'true');
		}
		if (data['locationprivate'] === true) {
			$("select['locationprivate']").children().filter("option[value='True']").attr('selected', 'true');
			$("select['locationprivate']").children().filter("option[value='False']").attr('selected', 'false');
		}
		else {
			$("select['locationprivate']").children().filter("option[value='True']").attr('selected', 'false');
			$("select['locationprivate']").children().filter("option[value='False']").attr('selected', 'true');
		}
		if (data['name'] !== "") {
			$(".name-header").html(data['name']);
		}
		else {
			$(".name-header").html($(".username").html());
		}
		$("img.propic").attr("src", data['propic']);
		$(".loading-overlay").hide();
	}
	function getInput (type) {
		var input  = $("input:not(input[type='submit']), textarea"),
			select = $("select"),
			returnedValues = [];
		if (type === 'input') {
			for (var i = 0; i < input.length; i++) {
				returnedValues[i] = input[i].value;
			}
		}
		else {
			for (var i = 0; i < select.length; i++) {
				returnedValues[i] = select[i].value;
			}
		}
		return returnedValues;
	}
	function inputChanged (newInput) {
		for (var i = 0; i < initialInput.length; i++) {
			if (newInput[i] !== initialInput[i]) {
				return true;
			}
		}
		return false;
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
					$(".propic-url").val(response.data.url);
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
