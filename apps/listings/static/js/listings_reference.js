$(document).ready(function(){
	var prev = "";
	function eventHandlers() {
		$(".for_sale").click(handleForSaleClick);
		$(".housing").click(handleHousingClick);
	}

	function handleForSaleClick(e){
		var val = ($(this).attr("data-id"));
		$("#category").text( "for sale >> " + $(this).html());
		$("#nameTitle").text($(this).html());
		$("#collapseOne").collapse('hide');
		if (prev != val ){
			$('.category_' + prev).hide();
			$(".edit").show();
			$('.category_' + val).show();
			console.log('p '+prev);
			prev = val;
			console.log('d  '+prev);
			console.log(val);

		}
		else{
		prev = val;
		$(".edit").show();
		$('.category_' + val).show();
		}
	}

	function handleHousingClick(e){
		var val = ($(this).attr("data-id"));
		$("#category").text("housing >> " + $(this).html());
		$("#collapseTwo").collapse('hide');
		$("#nameTitle").text($(this).html());
		if (prev != val ){
			$('.category_' + prev).hide();
			$(".edit").show();
			$('.category_' + val).show();
			console.log('p '+prev);
			prev = val;
			console.log('d '+prev);
			console.log(val);
		}
		else{
		prev = val;
		$(".edit").show();
		$('.category_' + val).show();
		}
	}

	eventHandlers();
});

function fileUpload(){
	filepicker.pickAndStore({
		services: ['COMPUTER','URL'],
		mimetype:"image/*",
		multiple: true
		},
		{location:"S3"},
	function(InkBlobs){
		var inky = InkBlobs;
		filePreview(inky);
		}
	);
}

function filePreview(ink){
	var text = ""
	for (var i=0; i<ink.length; i++){ 
		text = ink[i].filename + " sucessfully uploaded."
		var li = $('<li>')
			.text(text)
			.appendTo('#pics');
	}

}


function Edit(){
      $(document).ready(function(){
        $(".listing").hide();
        $(".edit").show();
    });
}

function Preview(){
      $(document).ready(function(){
        $(".edit").hide();
        $(".listing").show();
        $('.l-description').text($('#id_description').val());
		$('.title').text($('#id_title').val());
		$('.l-location').text("(" + $('#id_location').val() + ")");
		$('.l-price').text("$" + $('#id_price').val());
    });
}
