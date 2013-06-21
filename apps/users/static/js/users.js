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
});