
$(function() {

	$(document).ready(function(){
		$('.table-listings tbody tr td:first').click();
	 });		

	$('.table-listings tbody tr').click(function(event) {
		$(this).addClass('highlight').siblings().removeClass('highlight');
		var listingID = $(event.target).parent().data('listing-id');
		console.log(listingID);
		$(".message").hide();
		$(".buyer_card").hide();
		$(".listingID_" + listingID).show();	
	});

	$('.table-buyers').click(function(event){
		$('.table-buyers').removeClass('highlight');	
		$(this).addClass('highlight')
		var buyerID = $(event.target).parent().data('buyer-id');
		$(".message").hide();
		$('.buyer_'  + buyerID).show();
			
	});
});
