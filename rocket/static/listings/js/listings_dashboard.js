$(function() {

	$('.table-listings tbody tr').click(function(event) {
		var listingRow = $(this);

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

	$('.buyer-card').click(function(event){
		var buyerCard = $(this);
		$('.buyer-card').removeClass('highlight');
		buyerCard.addClass('highlight');
		var id = buyerCard.data('buyer-id');
		$(".message").hide();
		$('.buyer-'  + id).show();
	});

	$('.table-listings tbody tr').first().click();
	$(document).ready(function(){
		$('.share_optn').tooltip({
  			container: 'body'
			});
		$('.edit_optn').tooltip();
		$('.trash_optn').tooltip();
	});

	// AUTOPOST
	$(".share_optn").click(function (e) {
		e.preventDefault();
		$.ajax({
			type: 'GET',
			url: $(this).attr('href'),
			success: function (response) {
			}
		});
		return false;
	});
});