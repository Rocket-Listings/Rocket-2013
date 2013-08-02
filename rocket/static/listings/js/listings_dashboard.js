$(function() {

	$('.listings-table tbody tr').click(function(event) {
		var listingRow = $(this);
		$('.listings-table tbody tr').removeClass('highlight');
		listingRow.addClass('highlight');
		var id = listingRow.data('listing-id');
		$(".buyer-card").addClass("hide");
		$(".message, .message-form").addClass("hide");
		var buyers = $(".listing-" + id);
		if(buyers.length) {
			buyers.removeClass("hide");
			buyers.first().click();
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
		$(".message, .message-form").addClass("hide");
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

	$(".dashboard-refresh").click(function (e) {
		e.preventDefault();
		$.ajax({
			type: 'GET',
			url: '/listings/dashboard/data/',
			data: {'listing': $(".last-listing").text(),
				   'buyer': $(".last-buyer").text(),
				   'message': $(".last-message").text()},
			success: function (response) {
				insertNewData(response);
			}
		});
	});

	$("form.message-form").each(function() {
		var form = $(this);
		$(this).submit(function() {
			var csrftoken = getCookie('csrftoken');
			$.ajax({
				url: '/listings/dashboard/message/',
				method: 'POST',
				data: form.serialize(),
				beforeSend: function(xhr) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				},
				success: function (response) {
					switch (response.status) {
						case 'success':
							$("#new-message-wrapper").append(Mustache.render($("#new-message").html(), response));
							$('.buyer-' + response.messages.buyer_id).removeClass("hide");
							$('.last-message').text(response.messages.message_id);
							$('.buyer-' + response.messages.buyer_id + ' textarea').val("");
							break;
						case 'err_validation':
							console.log("There was an error sending the message.");
							break;
						case 'err_empty':
							break;
					}
				},
				error: function (response) {
					console.log("There was an error sending the message.");
				}
			});
			return false;
		});
	});

	function insertNewData(data) {
		console.log(data);
		// Update latest ids
		$(".last-listing").text(data.latest[0]);
		$(".last-buyer").text(data.latest[1]);
		$(".last-message").text(data.latest[2]);
	}

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