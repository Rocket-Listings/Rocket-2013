$(function() {

	$('.table-listings tbody tr').click(function(event) {
		var listingID = $(event.target).parent().data('listing-id');
		if(!switch_listing(listingID)) {
			var url = '/listings/' + listingID + '/api/buyers/'
			$.getJSON(url, load_listing_callback);
		}
	});

	$('.table-buyers tbody tr').click(function(event) {
		var buyerID = $(event.target).parent().data('buyer-id');
		var url = '/listings/' + currentListingID + '/api/messages/' + buyerID;
		$.getJSON(url, load_buyer_callback);
	});


	function load_listing_callback(data, textStatus, jqXHR) {
		var listingID = data[0].fields.listing;
		var inner_html = buyers_template(data);
		var html = $('<div class="listing_buyers" style="display:none;"></div>')
			.append(inner_html)
			.attr('id', 'listing_buyers_' + listingID);
		$('#all_listings_buyers').append(html);
		switch_listing(listingID);
	}

	// function load_buyer_callback(data, textStatus, jqXHR) {
	// 	var listingID = data[0].fields.listing;
	// 	var html = $(messages_template(data));
	// 	var html = html.attr('id', 'listing_buyers_' + listingID);
	// 	$('#all_listings_buyers').append(html);
	// 	switch_listing(listingID);
	// }

	function switch_listing(listingID) {
		if(currentListingID === listingID) {
			return true;
		} else {
			var selected = $('#listing_buyers_'+listingID)
			if (selected.length > 0) {
				$('.listing_buyers_'+currentListingID).hide();
				selected.show();
				currentListingID = listingID;
				return true;
			} else {
				return false;
			}
		}
	}

	// function switch_buyer(buyerID) {
	// 	if(currentBuyer != -1) {
	// 		$('.listing_buyers_'+buyerID).hide();
	// 	}
	// 	$('.listing_buyers_'+buyerID).show();
	// }

	var currentListingID = -1;
	var currentBuyer = -1;

	var source = $("#listing_buyers_table_hb").html();
	var buyers_template = Handlebars.compile(source);

	// var source = $("#buyer_message_thread_hb").html();
	// var messages_template = Handlebars.compile(source);
});