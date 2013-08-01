$(function() {

	$('.listings-table tbody tr').click(function(event) {
		var listingRow = $(this);
		$('.listings-table tbody tr').removeClass('highlight');
		listingRow.addClass('highlight');
		var id = listingRow.data('listing-id');
		$(".buyer-card").addClass("hide");
		var buyers = $(".listing-" + id);
		if(buyers.length) {
			buyers.removeClass("hide");
			buyers.first().click();
			$('.message-form').removeClass("hide");
		} else {
			$('.message-form').addClass("hide");
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
		console.log(id);
		$(".message").addClass("hide");
		$('.buyer-' + id).removeClass("hide");
	});

	$('.listings-table tbody tr').first().click();

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

	function linkToClickable(text) {
	    var exp = /(\b(https?):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
	    return text.replace(exp,"<a href='$1'>$1</a>"); 
	}
	$(".buyer, .seller").each(function() {
		$(this).html(linkToClickable($(this).html()));
	});
});