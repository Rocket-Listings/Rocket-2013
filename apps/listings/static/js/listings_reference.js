$(document).ready(function(){

	function eventHandlers() {
		$(".for_sale").click(handleForSaleClick);
		$(".housing").click(handleHousingClick);
	}

	function handleForSaleClick(e){
		$("#category").text( "for sale >> " + $(this).html());
		$("#collapseOne").collapse('hide');
	}

	function handleHousingClick(e){
		$("#category").text("housing >> " + $(this).html());
		$("#collapseTwo").collapse('hide');
	}

	eventHandlers();
});