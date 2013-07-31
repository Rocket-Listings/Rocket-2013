$(function() {
	// INIT
	filepicker.setKey('ATM8Oz2TyCtiJiHu6pP6Qz');
	var initialInput = getInput('input');
	var initialSelect = getInput('select');
	if ($("input[name='location']").val() === "") getLocation();

	// BINDINGS
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
	$(".verify-twitter").click(function (e) {
		e.preventDefault();
		$.oauthpopup({
			path: '/users/twitter/',
			callback: getTwitterHandle
		});
	});
	$(".disconnect-twitter").click(function (e) {
		e.preventDefault();
		disconnectTwitter();
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
				$(".propic-url").val("https://s3.amazonaws.com/static.rocketlistings.com/" + NewBlob.key);
				$(".save-all").addClass("propic-enable");
				$(".settings-form").submit();
			},
			function (FPError) {
				console.log(FPError);
			},
			function (percent) {
				console.log(percent);
				if (percent != 100) {
					$(".loading-overlay").removeClass("hide");
				}
			});
		},
		function (FPError) {
			console.log(FPError);
		});
	});
	$("form.settings-form").submit(function() {
		if ((!$(".save-all").hasClass("disabled")) || ($(".save-all").hasClass("propic-enable"))) {
			var csrftoken = getCookie('csrftoken');
			$.ajax({
				data: $(this).serialize(),
				type: $(this).attr('method'),
				url: $(this).attr('action'),
				beforeSend: function(xhr) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				},
				success: function(response) {
					if (response.profile) {
						console.log(response);
						$(".errors").hide();
						$(".save-all").addClass("disabled");
						$(".save-all").removeClass("propic-enable");
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

	// HELPER FUNCTIONS
	function insertNewValues(data) {
		if (data['name'] !== "") {
			$(".name-header").html(data['name']);
		}
		else {
			$(".name-header").html($(".username").html());
		}
		if ($("input[name='propic']").val() !== "") $("img.propic").attr("src", data['propic'] + "?" + new Date().getTime());
		$(".loading-overlay").addClass("hide");
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
	function getLocation() {
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
									//$("form").submit();
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
	}
	function getTwitterHandle () {
		$.ajax({
			type: 'GET',
			url: '/users/twitter/handle/',
			success: function (response) {
				if (response !== "no_oauth_token_or_key") {
					$(".twitter-handle").html(response);
					$(".at").removeClass("muted");
					$(".verify-twitter").addClass("hide");
					$(".disconnect-twitter").removeClass("hide");
				}
			}
		});
	}
	function disconnectTwitter() {
		$.ajax({
			type: 'GET',
			url: '/users/twitter/disconnect/',
			success: function (response) {
				if (response === "success") {
					$(".twitter-handle").html("");
					$(".verify-twitter").removeClass("hide");
					$(".disconnect-twitter").addClass("hide");
					$(".at").addClass("muted");
				}
			}
		});
	}

	// FACEBOOK BINDINGS
	$('.connect-fb').click(function() {
		FB.getLoginStatus(function (response) {
			if (response.status === 'connected') {
				fbProfile();
			}
			else {
				FB.login(function (response) {
					console.log(response);
					if (response.status === 'connected') {
						fbProfile();
					}
					else {
						console.log('User cancelled login action.');
					}
				}, {perms:'email,user_location'});
			}
		});
	});

	$(".disconnect-fb").click(function() {
		FB.api({ method: 'Auth.revokeAuthorization' });
		$.ajax({
			type: 'GET',
			url: '/users/facebook/disconnect/',
			success: function(response) {
				$(".fb-name").text("");
				$(".disconnect-fb").addClass("hide");
				$(".connect-fb").removeClass("hide");
			}
		});
	});

	function fbProfile() {
		data = {}
		FB.api('/me', function (response) {
			data['username'] = response.username,
			data['name'] = response.name,
			data['link'] = response.link
			FB.api('/me/picture?width=200&height=200&type=square', function (response) {
				if (!response.data.is_silhouette) {
					data['picture'] = response.data.url;
				}
				else {
					data['picture'] = "";
				}
				fbPostData(data)
			});
		});
	}

	function fbPostData(data) {
		var csrftoken = getCookie('csrftoken');
		$.ajax({
			data: data,
			type: 'POST',
			url: '/users/facebook/',
			beforeSend: function(xhr) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			},
			success: function(response) {
				$(".fb-name").text(response);
				$(".connect-fb").addClass("hide");
				$(".disconnect-fb").removeClass("hide");
			}
		});
	}

	// PROFILE JS
	// Handle the comment form
	$(".comment-form").submit(function() {
		var csrftoken = getCookie('csrftoken');
		console.log(csrftoken);
		$.ajax({
			data: $(this).serialize(),
			type: $(this).attr('method'),
			url: $(this).attr('action'),
			beforeSend: function(xhr) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			},
			success: function(response) {
				if (response[0]) {
					console.log(response)
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
		var newComment = '<div class="each-comment"><div class="row"><div class="span6"><h5>' + data.title + '</h5></div>';
			newComment += '<div class="span2"><h6>' + data.date_posted  + '</h6></div></div>';
			newComment += '<div class="row"><div class="span7"><p>' + data.comment + '</p></div></div></div>';
		$(".comment-body").append(newComment);
		$(".comment-form-container").hide();
		$(".comment-thanks").show();
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

	// Get cookie for csrf token
	function getCookie(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie != '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	}
});

//  FACEBOOK INIT CODE
window.fbAsyncInit = function() {
  	FB.init({
    	appId      : '279057228903179', // App ID
    	channelUrl : '{% static "/users/channel.html" %}', // Channel File
    	status     : true, // check login status
    	cookie     : true, // enable cookies to allow the server to access the session
    	xfbml      : false  // parse XFBML
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

// Twitter OAUTH popup (@nobuf)
(function($){
    $.oauthpopup = function(options)
    {
        if (!options || !options.path) {
            throw new Error("options.path must not be empty");
        }
        options = $.extend({
            windowName: 'Twitter'
          , windowOptions: 'location=0,status=0,width=800,height=400'
          , callback: function(){ window.location.reload(); }
        }, options);

        var oauthWindow   = window.open(options.path, options.windowName, options.windowOptions);
        var oauthInterval = window.setInterval(function(){
            if (oauthWindow.closed) {
                window.clearInterval(oauthInterval);
                options.callback();
            }
        }, 1000);
    };

    $.fn.oauthpopup = function(options) {
        $this = $(this);
        $this.click($.oauthpopup.bind(this, options));
    };
})(jQuery);
