var counter = 0;
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
		mimetype:"image/*",
		multiple: "true"
		},
		{location:"S3"},
	function(InkBlobs){
		var inky = InkBlobs;
		console.log(inky)
		photoLog(inky);
		}
	);
}

function photoLog(ink) {
	var html = [];
	var number = ink.length + counter;
	for (var i=counter; i<number; i++) {
		html.push("<input type = 'hidden' name='", i, "' value='", ink[i-counter].url, "'>");
	}
	$('#picsyo').append(html.join(''));
	image(ink);
	images(ink);
	counter++;
	$('#final_countdown').attr('value', counter);
}

function image(ink) {
	var html = [];
	for (var i=0; i<ink.length; i++) {
		html.push("<img src ='", ink[i].url, "'>");
	}
	$('#image').append(html.join(''));

}

function images(ink) {
	var html = [];
	for (var i=0; i<ink.length; i++) {
		html.push("<div class='item'><img src ='", ink[i].url, "'></div>");
	}
	$('#images').append(html.join(''));

}