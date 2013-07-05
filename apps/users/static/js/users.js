$(function(response) {
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
							errors.append(" <strong class='capital'>" + key + ":</strong>" + response[key] + "<br>");
						}
						errors.show();
					}
					handleClickEvents();
				}
			});
			return false;
		})
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
			if (key.toString() === "name") {`
				if (data[key] !== "") $("h3.name").html(data[key] + "'s info");
				else {
					var username = $(".username > code").html();
					$("h3.name").html(username + "'s info").removeClass("muted");
				}
			}
		}
	}
	$('.comment-data-form').submit(function(){
		var csrftoken = $.cookie('csrftoken');
		$.ajaxSetup{
			data: $(this).serialize(),
			type: $(this).attr('method'),
			url: $(this).attr('action'),
    		crossDomain: false, // obviates need for sameOrigin test
    		beforeSend: function(xhr, settings) {
        		if (!csrfSafeMethod(settings.type)) 
            		xhr.setRequestHeader("X-CSRFToken", csrftoken);
    		},
    		success: function(response){
    			$('.comment-data-form').reset();
    		}
		
		}
	}

	// $(document).ready(function() {
	// 	var OSX = {
	// 		container: null,
	// 		init: function () {
	// 			$("input.comment-button, a.comment-button").click(function (e) {
	// 				e.preventDefault();	
	// 				$("#comment-form").modal({
	// 					overlayId: 'comment-form-overlay',
	// 					containerId: 'comment-form-container',
	// 					closeHTML: null,
	// 					minHeight: 80,
	// 					opacity: 65, 
	// 					position: ['0',],
	// 					overlayClose: true,
	// 					onOpen: OSX.open,
	// 					onClose: OSX.close
	// 				});
	// 			});
	// 		},
	// 		open: function (d) {
	// 			var self = this;
	// 			self.container = d.container[0];
	// 			d.overlay.fadeIn('slow', function () {
	// 				$("#comment-form", self.container).show();
	// 				var title = $("#comment-form-title", self.container);
	// 				title.show();
	// 				d.container.slideDown('slow', function () {
	// 					setTimeout(function () {
	// 						var h = $("#comment-data", self.container).height()
	// 							+ title.height()
	// 							+ 40; // padding
	// 						d.container.animate(
	// 							{height: h + 20}, 
	// 							200,
	// 							function () {
	// 								$("div.close", self.container).show();
	// 								$("#comment-data", self.container).show();
	// 							}
	// 						);
	// 					}, 10000);
	// 				});
	// 			})
	// 		},
	// 		close: function (d) {
	// 			var self = this; // this = SimpleModal object
	// 			d.container.animate(
	// 				{top:"-" + (d.container.height() + 20)},
	// 				500,
	// 				function () {
	// 					self.close(); // or $.modal.close();
	// 				}
	// 			);
	// 		}
	// 	};
	// 	OSX.init();
	// })
	$(".comments-list li:even").css("background-color", "#FFEED2")
	$(".comments-list li:odd").css("background-color", "#FFF8EC")
	handleClickEvents()
});
