$(function() {

	$('.table-listings tbody tr').first().click();

	$('.table-listings tbody tr').click(function(event) {
		var listingRow = $(this);
		listingRow.addClass('highlight').siblings().removeClass('highlight');
		var id = listingRow.data('listing-id');
		$(".message").hide();
		$(".buyer-card").hide();
		$(".listing-" + id).show();	
	});

	$('.buyer-card').click(function(event){
		var buyerCard = $(this);
		$('.buyer-card').removeClass('highlight');	
		buyerCard.addClass('highlight');
		var id = buyerCard.data('buyer-id');
		console.log(id);
		$(".message").hide();
		$('.buyer-'  + id).show();
	});
});
