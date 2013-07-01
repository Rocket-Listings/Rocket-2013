$(document).ready(function(){

	$('.l-description').text($('#id_description').val());
	$('.title').text($('#id_title').val());
	$('.l-location').text("(" + $('#id_location').val() + ")");
	$('.l-price').text("$" + $('#id_price').val());

	var prev = "";
	function eventHandlers() {
		$("a", ".tab-pane").click(handleClick);
	}

	function handleClick(e) {
		var val = ($(this).data("id"));
		$("a", ".tab-pane").addClass("unselected");
		$("a", ".tab-pane").removeClass("selected");
		$(this).removeClass("unselected");
		$(this).addClass("selected");
		$("#nameTitle").text($(this).html());
		$("#listingType").text("Public");	
		$("#id_pictures").text("True");
		if (prev != val ){
			$('.category_' + prev).hide();
			$('.category_' + val).show();
			prev = val;
		}
		else{
		prev = val;
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
		console.log(inky[0].url)
		image(inky[0].url);
		}
	);
}


function image(url) {
	var img = document.createElement("IMG");
	img.src = url;
	document.getElementById('image').appendChild(img);
}
