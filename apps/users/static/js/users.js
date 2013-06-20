$(function() {
	console.log("Ready");

	/* Process the start of the signup */
	function signupStartHandler() {
		console.log("click");
		var address = $(".start-email").val().replace(/ /g, ""),
			username;
		if ((address != "") && validateEmail(address)) {
			username = address.substring(0, indexOf("@"));
			signupAnimate();
			console.log("signup success");
		}
		else {
			signupErr("start-signup-error", "Please enter a valid email address");
			console.log("signup error");
		}
		console.log(address);
	}

	function signupAnimate() {
		$(".start-signup").slideUp(400);
		console.log("1")
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

	function removeSignupErr(classSelector) {
		var selector = "." + classSelector;
		$(selector.html(""))
	}

	$(".start-submit").click(signupStartHandler);
});