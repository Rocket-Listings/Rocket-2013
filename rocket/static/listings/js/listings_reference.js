var pictureCounter = 0; /* Keeps track of the number of pictures */
var categoryChange = 0; /* Checks to see if a category has been seleced for validation purposes*/

$(document).ready(function(){
	$(".edit").show();
  	$(".preview-pane").hide();
	$('.l-description').text($('#id_description').val());
	$('.title').text($('#id_title').val());
	$('.l-location').text("(" + $('#id_location').val() + ")");
	$('.l-price').text("$" + $('#id_price').val());

	//this variable is to hold the result if the category housing swap or wanted or neither
	var is_housing = 0; /* Way to differetiate housing swap and housing wanted*/

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
		/* val = the category selected in the tab */

		function changeCat() {
			var id = document.getElementById('id_category');
			for (var i=1; i<id.length; i++) {
				if ( id.options[i].text == val) {
					/* Finds the value of the matching category and then selects the correct option value */
					document.getElementById('id_category').value = i;
				}
			}
		}
		/* changes the option selected for listing*/
		changeCat();
		/* Set catCahnge to 1 to satisfy validation */
		categoryChange = 1;

		/* Housing swap and housing wanted share the same first name thus we need to differnetiate the two */
		if (val == "housing swap"){
			is_housing = 1;
		}
		else if (val == "housing wanted"){
			is_housing = 2;
		}
		else {
			is_housing = 0;
		}

		/* Split the into an array of words and set val equal to the first word*/
		string = val.split(" ");
		val = string[0];

		/* Set final_category id to the first word of the category selected inorder to pass into the view.py */
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
			$(".preview-pane .category_" + val).show();
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
	/* function needs more work inorder to better save photos in s3 */
	filepicker.pickAndStore({
		services: ['COMPUTER','URL'],
		mimetype:"image/*",
		multiple: "true"
		},
		{location:"S3"},
	function(InkBlobs){
		var filepickerObject = InkBlobs;
		photoLog(filepickerObject); /* Logs photos for storing in database */
		editImage(filepickerObject); /* Preview images on edit page */
		}
	);
}

function photoLog(object) {
	/* creat a blank html object where all of the picture urls are going to go*/
	var html = [];

	/* finds the number of photos in the upload object */
	var length = object.length;

	/* If someone uploads to the database more than once without a page load we need to make sure the url is put in the correct index */
	var number = length + pictureCounter;

	for (var i=pictureCounter; i<number; i++) {
		/* push an input with the name (the index of the image uploaded) and the value being the url */
		html.push("<input type = 'hidden' name='", i, "' value='", object[i-pictureCounter].url, "'>");
	}
	/* push the html to pictureData so the view.py can retrieve the information */
	$('#pictureData').append(html.join(''));

	/* increment counter in case someone decides to add more pictures */
	pictureCounter = pictureCounter + length;

	/* Set or increment the final_countdown id to keep track of the number of pictures uploaded */
	$('#final_countdown').attr('value', pictureCounter);
}

function editImage(object) {
	/* creat a blank html object where all of the picture urls are going to go*/
	var html = [];
	for (var i=0; i<object.length; i++) {
		/* push images with the source equal to the picture urls */
		html.push("<img src ='", object[i].url, "'>");
	}
	/* push the html to image so user can view image */
	$('#image').append(html.join(''));

}


function validateForm() {
	if (categoryChange===0) {
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