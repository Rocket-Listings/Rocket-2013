$(document).ready(function(){

	function eventHandlers() {
		$(".for_sale").click(handleForSaleClick);
		$(".housing").click(handleHousingClick);
	}

	function handleForSaleClick(e){
		$("#category").text( "for sale >> " + $(this).html());
		$("#collapseOne").collapse('hide');
		$(".edit").show();

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