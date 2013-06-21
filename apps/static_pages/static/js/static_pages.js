$(function() {
	$('.homepage-why-pay').popover();

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
});