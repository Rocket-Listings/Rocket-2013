$(document).ready(function(){
	var prev = "";
	function eventHandlers() {
		$(".for_sale").click(handleForSaleClick);
		$(".housing").click(handleHousingClick);
	}

	function handleForSaleClick(e){
		var val = ($(this).attr("data-id"));

		$("#category").text( "for sale >> " + $(this).html());
		$("#collapseOne").collapse('hide');
		if (prev != val ){
			$('.category_' + prev).hide();
			$('.category_' + val).show();

			console.log('v'+val);
			console.log('p'+prev);
			prev = val;
			console.log('p'+prev);

		}
		else{
		prev = val;
		console.log(prev);
		console.log(val);
		$('.category_' + val).show();
	}
	}

	function handleHousingClick(e){
		$("#category").text("housing >> " + $(this).html());
		$("#collapseTwo").collapse('hide');
	}

	eventHandlers();
});