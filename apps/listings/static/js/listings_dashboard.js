$(function() {

	$('.table-listings tbody tr').click(function(event) {
		var listingID = $(event.target).parent().data('listing-id');
		var url = '/listings/' + listingID + '/api/buyers/'
		$.getJSON(url, load_buyers_callback);
	});

	function load_buyers_callback(data, textStatus, jqXHR) {
		var listingID = data[0].fields.listing;
		var template_html = template(data);
		var html = '<div class="listing_buyers" id="listing_buyers_' + listingID + '">' + template_html + '</div>';
		$('#all_listings_buyers').append(html);
	}

	var source = $("#listing_buyers_table_hb").html();
	var template = Handlebars.compile(source);
});