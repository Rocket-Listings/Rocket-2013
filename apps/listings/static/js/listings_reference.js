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
		var y = $(this).attr("data-id");
		function changeCat() {
			var x = document.getElementById("id_category");
			for (var i=1; i<x.length; i++) {
				if ( x.options[i].text == y) {
					document.getElementById('id_category').value = i;
				}
			}
		}

		changeCat();

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
		mimetype:"image/*"
		},
		{location:"S3"},
	function(InkBlobs){
		var inky = InkBlobs;
		$("#id_pictures").text(inky[0].url);
		image(inky[0].url);
		}
	);
}


function image(url) {
	document.getElementById('image_1').style.display = 'none';
	document.getElementById('image_2').style.display = 'none';
	document.getElementById('image').src= url;
	document.getElementById('images').src= url;
}

