$(function() {

	$("document").ready(function() {
        $('.table-listings tbody tr td.clickable:first').trigger('click'); 
        
        
}); 

	$('.table-listings tbody tr td.clickable').click(function(event) {
		var listingID = $(event.target).parent().data('listing-id');
		console.log(listingID);
			if(!switch_listing(listingID)) {
				var url = '/listings/' + listingID + '/api/buyers/'
				$.getJSON(url, load_listing_callback);
		}

	});

	$('.table-listings tbody tr').click(function(event) {
    	$(this).addClass('highlight').siblings().removeClass('highlight');
});


	$('#listings').on('click', 'button', function(event){
		var buyerID = $(event.target).parent().data('buyer-id');
		console.log('buyerclick');
		if(!switch_buyer(curListingID, buyerID)) {
			//console.log('switch buyer false');			
			var url = '/listings/' + curListingID + '/api/messages/' + buyerID + '/'
			
			$.getJSON(url, load_buyer_callback);
		}
	});

	function load_listing_callback(data, textStatus, jqXHR) {
		var listingID = data[0].fields.listing;
		data.listingID = listingID;
		var html = buyers_template(data);
		$('#listings').append(html);
		switch_listing(listingID);

	}

	function load_buyer_callback(data, textStatus, jqXHR) {
		var buyerID = data[0].fields.buyer;
		console.log(buyerID);
		data.buyerID = buyerID;
		var html = messages_template(data);
		$('#listing_' + curListingID + ' .buyers_').append(html);
		console.log('#listing_' + curListingID + ' .buyers_');
		switch_buyer(curListingID, buyerID);
	}

	function switch_listing(listingID) {
		if(curListingID !== listingID) {
			var nextListing = $('#listing_' + listingID);
			if (nextListing.length > 0) {
				$('#listing_' + curListingID).hide();
				nextListing.show();
				curListingID = listingID;
				return true;
			} else {
				return false;
			}
		} else {
			return true;
		}
	}

	function switch_buyer(listingID, buyerID) {
		if(curBuyerID !== buyerID) {
			var nextBuyer = $('#listing_' + curListingID + ' #buyer_' + buyerID);
			//console.log(nextBuyer);
			if (nextBuyer.length > 0) {
				$('#listing_' + curListingID + ' #buyer_' + curBuyerID).remove();
				$('#listing_' + curListingID).hide();

				$('#listing_' + listingID).show();
				$('#listing_' + listingID + ' #buyer_' + buyerID).show();
				nextBuyer.show();
				curBuyerID = buyerID;
				//console.log('swtich_buyer function true');
				return true;
			} else {
				return false;
			}
		} else {
			//console.log('swtich_buyer function true');
			return true;
		}
	}

	$(document).on("click", ".deleteModal", function () {
     var listingID = $(this).data('listing.id');
     $(".modal").val( 'listing.id' );
});

    


	var curListingID = -1;
	var curBuyerID = -1;

	var buyers_template = Handlebars.compile($("#listing_buyers_table_hb").html());
	var messages_template = Handlebars.compile($("#buyer_messages_thread_hb").html());
	var nobuyers_template = Handlebars.compile($("#buyer_messages_thread_hb").html());


});