$(document).ready(function(){
	// $("#myTable").tablesorter({
		
	// 	headers: {
	// 		4: {sorter: false},
	// 		3: { sorter: "shortDate"}
	// 			}


					
	// });

	//var listings = new Array();
	//var listing_number = $(".listing_table tr").length;
	//var listing_name;

	//for (i=0;i<listing_number;i++){
	//	listing_name = $(".listing_table tr:eq("+i+") .bargle").html().toLowerCase().trim();
	//	listings.push(listing_name);
	//}

	//listings = quicksort(listings);
});


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

});

function quicksort(listings) {
	var length = listings.length;
	var smaller;

	if (length > 5){
		var value1 = listings[0];
		var value2 = listings[1];
		var value3 = listings[2];
		var pivot;
		

		if (compareTitles(value1,value2) == 0 && compareTitles(value1,value3) == 1) {
			pivot = value1;
		}
		else if (compareTitles(value1,value2) == 1 && compareTitles(value1,value3) == 0) {
			pivot = value1;
		}
		else if (compareTitles(value2,value1) == 0 && compareTitles(value2,value3) == 1) {
			pivot = value2;
		}
		else if (compareTitles(value2,value1) == 1 && compareTitles(value2,value3) == 0) {
			pivot = value2;
		}
		else if (compareTitles(value3,value1) == 0 && compareTitles(value3,value2) == 1) {
			pivot = value3;
		}
		else if (compareTitles(value3,value1) == 1 && compareTitles(value3,value2) == 0) {
			pivot = value2;
		}


		var list1 = new Array();
		var list2 = new Array();

		var listing_name;
		for (i=0;i<length;i++) {
			listing_name = listings[i];

			smaller = compareTitles(listing_name,pivot);
			if (smaller == 0) {
				list1.push(listing_name);
			}
			else {
				list2.push(listing_name);
			}
		}

		list1 = quicksort(list1);
		list2 = quicksort(list2);

		listings = list1.concat(list2);
	}
	else {
		var min;
		for(i=0;i<length;i++) {
			min=i;
			for(j=i+1;j<length;j++) {
				smaller = compareTitles(listings[i],listings[j]);
				if(smaller == 1){
					min = j;
				}
			}
			if(i != min){
				var temp = listings[i];
				listings[i] = listings[min];
				listings[min] = temp;


			}
		}
	}


	return listings;
}

function compareTitles(value1,value2){
	var smaller;
	var counter = 0;
	var val_length1 = value1.length;
	var val_length2 = value2.length;
	var val_char1 = value1.charCodeAt(counter);
	var val_char2 = value2.charCodeAt(counter);

	while ((val_char1 == val_char2 && val_length1 >= i+1) && val_length2 >= i+1) {
		counter += 1;
		val_char1 = value1.charCodeAt(counter);
		val_char2 = value2.charCodeAt(counter);
	}

	if (val_char1 < val_char2) {
		smaller = 0;
	}
	else if (val_char1 > val_char2) {
		smaller = 1;
	}
	else {
		if (val_length1 > val_length2) {
			smaller =  1;
		}
		else if (val_length1 < val_length2) {
			smaller = 0;
		}
		else {
			smaller = 0;
		}
	}

	return smaller;
}





