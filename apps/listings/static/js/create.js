$(document).ready(function(){
	function pageLoad() {
		$(".edit").show();
		$(".listing").hide();
	}
	pageLoad();

	$(".preview-btn").click(function() {
		$(".edit").hide();
		$(".listing").show();
		$('.l-description').text($('#id_description').val());
		$('.title').text($('#id_title').val());
		$('.l-location').text("(" + $('#id_location').val() + ")");
		$('.l-price').text("$" + $('#id_price').val());
	});
	$(".edit-btn").click(function() {
		$(".edit").show();
		$(".listing").hide();
	});
});