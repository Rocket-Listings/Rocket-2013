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
		$(".edit").show();
	}

	eventHandlers();
});

function FilePickClick(){
  filepicker.pickMultiple({
      mimetypes: ['image/*', 'text/plain'],
      services:['COMPUTER', 'URL'],
    },
    function(InkBlob){
      console.log(JSON.stringify(InkBlob));
    },
    function(FPError){
      console.log(FPError.toString());
    }
  );
};

function fileUpload(){
	filepicker.pickAndStore({
		mimetype:"image/*"},
	    {location:"S3"}, 
	    function(InkBlobs){
	   		console.log(JSON.stringify(InkBlobs));
	});
};
