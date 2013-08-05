$(function() {
	// Toggle the checkboxes
	$(".check-all").click(function () {
		if (this.checked) {
			$(".check-one").prop('checked', true);
		}
		else {
			$(".check-one").prop('checked', false);
		}
	});

	// Scroll messages to bottom
	$.fn.scrollBottom = function() {
		$(this).scrollTop($(this)[0].scrollHeight);
	}

	$('.listings-body ul').click(function () {
		var listingRow = $(this),
			id = listingRow.data('listing-id'),
			buyers = $(".listing-" + id);
		$('.listings-body ul').removeClass('highlight');
		listingRow.addClass('highlight');
		$(".message").addClass("hide");
		$(".buyer-card").addClass("hide");
		if(buyers.length) {
			buyers.removeClass("hide");
			buyers.first().click();
			$('.message-form-wrapper').removeClass("hide");
			$('.messages-body').scrollBottom();
		} else {
			$('.message-form-wrapper').addClass("hide");
		}
	});

	$('.buyer-card').click(function(event){
		var buyerCard = $(this),
			id = buyerCard.data('buyer-id');
		$('.buyer-card').removeClass('highlight');
		buyerCard.addClass('highlight');
		$(".message").addClass("hide");
		$('.buyer-' + id).removeClass("hide");
		$('.messages-body').scrollBottom();
	});

	$('.close').click(function(event){
		$('.dashboard-panel').removeClass("first-visit");
	});

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
	    var exp = /((([A-Za-z]{3,9}:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]+|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w-_]*)?\??(?:[-\+=&;%@.\w_]*)#?(?:[\w]*))?)/gi;
	    return text.replace(exp, "<a href='$1'>$1</a>"); 
	}
	
	$(".message-content").each(function() {
		$(this).html(linkToClickable($(this).text()));
	});

	$('.listings-body ul').first().click();
});