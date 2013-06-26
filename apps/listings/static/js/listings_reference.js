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
			prev = val;

		}
		else{
		prev = val;
		$(".edit").show();
		$('.category_' + val).show();
		}
	}

	function handleHousingClick(e){
		$("#category").text("housing >> " + $(this).html());
		$("#collapseTwo").collapse('hide');
		$(".edit").show();
		$("#nameTitle").text($(this).html());
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
		text = text + ink[i].filename + " sucessfully uploaded.  "
	}
	$("#pics").text( text );
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
    });
}