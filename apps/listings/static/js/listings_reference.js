var counter = 0;
var catChange = 0;
$(document).ready(function(){

	$('.l-description').text($('#id_description').val());
	$('.title').text($('#id_title').val());
	$('.l-location').text("(" + $('#id_location').val() + ")");
	$('.l-price').text("$" + $('#id_price').val());

	var prev = "";
	function eventHandlers() {
		$("a", ".tab-pane").click(handleClick);
		$(".edit_button").click(handleEditClick);
		$(".preview_button").click(handlePreviewClick);
	}

	function handleClick(e) {
		var y = $(this).html();
		function changeCat() {
			var x = document.getElementById("id_category");
			for (var i=1; i<x.length; i++) {
				if ( x.options[i].text == y) {
					document.getElementById('id_category').value = i;
				}
			}
		}

		changeCat();
		catChange = 1;

		var val = $(this).html();

		if (val == 'apartment and housing' || val == 'rooms and shared' || val == 'sublets and temporary' 
    	|| val == 'housing wanted' || val == 'housing swap' || val == 'vacation rentals' 
    	|| val == 'parking and storage' || val == 'office and commercial' || val == 'real estate for sale') {

			val = "housing";
 		}
 		string = val.split(" ");
 		first_word = string[0];
 		console.log(first_word);

		$("a", ".tab-pane").addClass("unselected");
		$("a", ".tab-pane").removeClass("selected");
		$(this).removeClass("unselected");
		$(this).addClass("selected");
		$("#nameTitle").text($(this).html());
		$("#listingType").text("Public");	
		$("#id_pictures").text("True");
		if (prev != first_word ){
			$('.category_' + prev, ".edit").hide();
			$('.category_' + first_word, ".edit").show();
			prev = first_word;
		}
		else{
		prev = first_word;
		$('.category_' + first_word, ".edit").show();
		}
	}

	function handlePreviewClick(e) {
		$(".edit").hide();
		$(".preview-pane").show();
		$('.l-description').text($('#id_description').val());
		$('.title').text($('#id_title').val());
		$('.l-location').text("(" + $('#id_location').val() + ")");
		$('.l-price').text("$" + $('#id_price').val());
		var category = $(".hidden > select option:selected").html();
  		var base_category = $("li.active").text().toLowerCase().trim();
  		$(".l-category").text(base_category + " > " + category);

  		$('.category_' + prev, ".preview-pane").hide();
		$('.category_' + prev, ".preview-pane").show();

		var specs = $('.table_' + prev + ' input').length;

		for (var i=0;i<specs;i++){
			var spec_value = $('.table_' + prev + ' input:eq('+i+')').val();
			$('.table_preview_' + prev + ' input:eq('+i+')').val(spec_value);
		}
  	}

	function handleEditClick(e) {
		$(".edit").show();
		$(".preview-pane").hide();
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
		photoLog(inky);
		image(inky);
		images(inky);
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
	counter= counter + ink.length;
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


function validateForm() {
	if (catChange===0) {
		alert("Please select a Category");
	}
	else if (document.getElementById('id_title').value==="") {
		alert("Please Fill in a Title");
	}
	else if (document.getElementById('id_price').value==="") {
		alert("Please Fill in a Price");
	}
	else if (document.getElementById('id_location').value==="") {
		alert("Please Fill in a Location");
	}
	else if (document.getElementById('id_description').value==="") {
		alert("Please Fill in a Description");
	}
	else {
		document.getElementById('primaryButton').click();
	}

	function pageLoad() {
		$(".edit").show();
		$(".preview-pane").hide();
	}
	pageLoad();

	
	
		
}