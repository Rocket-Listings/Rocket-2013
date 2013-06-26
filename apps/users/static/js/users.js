$(function() {
	function handleEvents() {
		var prevData = null;
		$(".edit").click(function(e) {
			e.preventDefault();
			prevData = $(this).parent().prev().val();
			$(this).parent().parent().hide();
			$(this).parent().parent().next().show();
			if ($(this).parent().parent().next().find("input")[1]) {
				$(this).parent().parent().next().find("input")[0].focus();
			}
			else{
				$(this).parent().parent().next().find("select")[0].focus();
			}
			$(".edit").replaceWith("<span class='edit muted'>Edit</span>");
			$(".change-password").replaceWith("<span class='muted'>Change password</span>");
			$("table").removeClass("table-hover");
		});
		// $(".unedit").click(function(e) {
		// 	e.preventDefault();
		// 	$(this).parent().parent().hide();
		// 	$(this).parent().parent().prev().show();
		// 	$(".edit").replaceWith("<a class='edit' href='#'>Edit</a>");
		// 	$("table").addClass("table-hover");
		// 	handleEvents();
		// });
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
					console.log(response);
				}
			});
			return false;
		});
	}
	handleEvents();
});