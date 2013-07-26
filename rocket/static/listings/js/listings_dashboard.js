$(function() {

	$('.table-listings tbody tr').click(function(event) {
		var listingRow = $(this);
		$('.table-listings tbody tr').removeClass('highlight');
		listingRow.addClass('highlight');
		var id = listingRow.data('listing-id');
		$(".message").hide();
		$(".buyer-card").hide();
		var buyers = $(".listing-" + id);
		if(buyers.length) {
			buyers.show();
			buyers.first().click();
			$('.message-form').show();
		} else {
			$('.message-form').hide();
		}
	});

	$('.close').click(function(event){
		$('.dashboard-panel').removeClass("first-visit");
	});

	$('.buyer-card').click(function(event){
		var buyerCard = $(this);
		$('.buyer-card').removeClass('highlight');
		buyerCard.addClass('highlight');
		var id = buyerCard.data('buyer-id');
		$(".message").hide();
		$('.buyer-' + id).show();
	});

	$('.table-listings tbody tr').first().click();

	// AUTOPOST
	$(".share_optn").click(function (e) {
		e.preventDefault();
		if (!$(this).hasClass("disabled")) {
			$.ajax({
				type: 'GET',
				url: $(this).attr('href'),
				success: function (response) {
				}
			});
		}
		$(this).addClass("disabled");
		checkStatus($(this).attr("id"));
		return false;
	});

	function checkStatus(listingid) {
		var timer = setInterval(function () {
			$.ajax({
				type: 'GET',
				url: '/listings/' + listingid + '/status',
				success: function (response) {
					if (response === "Active") {
						clearInterval(timer);
						$("tr[data-listing-id='" + listingid + "'] td.listing-status").html(response);
						$("a#" + listingid).removeClass("disabled");
					}
				}
			});
		}, 3000);
	}
});