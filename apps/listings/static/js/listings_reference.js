var pictureCounter = 0;
var categoryChange = 0;

$(document).ready(function(){
	$('.l-description').text($('#id_description').val());
	$('.title').text($('#id_title').val());
	$('.l-location').text("(" + $('#id_location').val() + ")");
	$('.l-price').text("$" + $('#id_price').val());

	//this variable is to hold the result if the category housing swap or wanted or neither
	var is_housing = 0;

	var prev = "";
	var val = "";

	function eventHandlers() {
		$("a", ".tab-pane").click(handleClick);
		$(".edit_button").click(handleEditClick);
		$(".preview_button").click(handlePreviewClick);
	}

	function handleClick(e) {
		prev = val;
		val = $(this).html();

		function changeCat() {
			var id = document.getElementById("id_category");
			for (var i=1; i<id.length; i++) {
				if ( id.options[i].text == val) {
					document.getElementById('id_category').value = i;
				}
			}
		}

		changeCat();
		catChange = 1;

		if (val == "housing swap"){
			is_housing = 1;
		}
		else if (val == "housing wanted"){
			is_housing = 2;
		}
		else {
			is_housing = 0;
		}

 		string = val.split(" ");
 		val = string[0];

 		$('#final_category').attr('value', val);

 		var specs = $('.table_' + val + ' input').length;

		$("a", ".tab-pane").addClass("unselected");
		$("a", ".tab-pane").removeClass("selected");
		$(this).removeClass("unselected");
		$(this).addClass("selected");
		$("#nameTitle").text($(this).html());
		$("#listingType").text("Public");

		$('.category_' + prev, ".preview-pane").hide();
		$('.category_' + prev, ".edit").hide();	
		
		if ((prev != val || val == "housing") && specs != 0){
			
			if (is_housing == 1) {
				$(".edit .category_" + val + ":eq(0)").show();
			}
			else if (is_housing == 2) {
				$(".edit .category_" + val + ":eq(1)").show();
			}
			else {
				$('.category_' + val, ".edit").show();
			}
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

		if (is_housing == 1){
			$(".preview-pane .category_" + val +":eq(0)").show();
			var specs = $('.table_' + val + ':eq(0) input').length;

			for (var i=0;i<specs;i++){
				var spec_value = $('.table_' + val + ':eq(0) input:eq('+i+')').val();
				$('.table_preview_' + val + ':eq(0) input:eq('+i+')').val(spec_value);
			}
		}
		else if (is_housing == 2) {
			$(".preview-pane .category_" + val +":eq(1)").show();
			var specs = $('.table_' + val + ':eq(1) input').length;

			for (var i=0;i<specs;i++){
				var spec_value = $('.table_' + val + ':eq(1) input:eq('+i+')').val();
				$('.table_preview_' + val + ':eq(1) input:eq('+i+')').val(spec_value);
			}
		}
		else {
			$('.category_' + val, ".preview-pane").show();
			var specs = $('.table_' + val + ' input').length;

			for (var i=0;i<specs;i++){
				var spec_value = $('.table_' + val + ' input:eq('+i+')').val();
				$('.table_preview_' + val + ' input:eq('+i+')').val(spec_value);
			}
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
		var filepickerObject = InkBlobs;
		photoLog(filepickerObject);
		editImage(filepickerObject);
		previewImages(filepickerObject);
		}
	);
}

function photoLog(object) {
	var html = [];
	var length = object.length;
	var number = length + pictureCounter;
	for (var i=pictureCounter; i<number; i++) {
		html.push("<input type = 'hidden' name='", i, "' value='", object[i-pictureCounter].url, "'>");
	}
	$('#pictureData').append(html.join(''));
	pictureCounter = pictureCounter + length;
	$('#final_countdown').attr('value', pictureCounter);
}

function editImage(object) {
	var html = [];
	for (var i=0; i<object.length; i++) {
		html.push("<img src ='", object[i].url, "'>");
	}
	$('#image').append(html.join(''));

}

function previewImages(object) {
	var html = [];
	for (var i=0; i<object.length; i++) {
		html.push("<div class='item'><img src ='", object[i].url, "'></div>");
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