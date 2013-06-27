$(document).ready(function(){
	var prev = "";
	function eventHandlers() {
<<<<<<< HEAD
		//$(".for_sale").click(handleForSaleClick);
		//$(".housing").click(handleHousingClick);
		$("a", ".tab-pane").click(handleClick);
=======
		$(".for_sale").click(handleForSaleClick);
		$(".housing").click(handleHousingClick);
		$('.show-container').click(handleShowClick);
>>>>>>> ee710fa8eb4d07bafe340a3e2231ccccc9d594d1
	}

	function handleClick(e) {
		var val = ($(this).data("id"));
		$("a", ".tab-pane").addClass("unselected");
		$("a", ".tab-pane").removeClass("selected");
		$(this).removeClass("unselected");
		$(this).addClass("selected");
		$("#nameTitle").text($(this).html());
<<<<<<< HEAD
=======

		$("#collapseOne").collapse('hide');
		
>>>>>>> ee710fa8eb4d07bafe340a3e2231ccccc9d594d1
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
<<<<<<< HEAD
			prev = val;
=======
		prev = val;
		$(".edit").show();
		$('.category_' + val).show();
		}
		$('.accordion-toggle').hide();
		$('.show-container').show();
		
	}

	function handleHousingClick(e){
		var val = ($(this).attr("data-id"));
		$("#category").text("housing >> " + $(this).html());
		$("#collapseTwo").collapse('hide');
		$("#nameTitle").text($(this).html());
		if (prev != val ){
			$('.category_' + prev).hide();
>>>>>>> ee710fa8eb4d07bafe340a3e2231ccccc9d594d1
			$(".edit").show();
			$('.category_' + val).show();
		}
		$('.accordion-toggle').hide();
		$('.show-container').show();
	}

	function handleShowClick(e){
		$('.accordion-toggle').show();
		$("#category").text("Repick your category");
		$('.show-container').hide();
	}

	// function handleForSaleClick(e){
	// 	var val = ($(this).data("id"));
	// 	$('.for_sale').addClass("unselected");
	// 	$('.housing').addClass("unselected");
	// 	$('.for_sale').removeClass("selected");
	// 	$('.housing').removeClass("selected");
	// 	$(this).removeClass("unselected");
	// 	$(this).addClass("selected");
	// 	$("#category").text( "for sale >> " + $(this).html());
	// 	$("#nameTitle").text($(this).html());
	// 	$("#collapseOne").collapse('hide');
	// 	if (prev != val ){
	// 		$('.category_' + prev).hide();
	// 		$(".edit").show();
	// 		$('.category_' + val).show();
	// 		console.log('p '+prev);
	// 		prev = val;
	// 		console.log('d  '+prev);
	// 		console.log(val);
	// 	}
	// 	else{
	// 	prev = val;
	// 	$(".edit").show();
	// 	$('.category_' + val).show();
	// 	}
	// }

	// function handleHousingClick(e){
	// 	var val = ($(this).attr("data-id"));
	// 	$('.for_sale').addClass("unselected");
	// 	$('.housing').addClass("unselected");
	// 	$('.for_sale').removeClass("selected");
	// 	$('.housing').removeClass("selected");
	// 	$(this).removeClass("unselected");
	// 	$(this).addClass("selected");
	// 	$("#category").text("housing >> " + $(this).html());
	// 	$("#collapseTwo").collapse('hide');
	// 	$("#nameTitle").text($(this).html());
	// 	if (prev != val ){
	// 		$('.category_' + prev).hide();
	// 		$(".edit").show();
	// 		$('.category_' + val).show();
	// 		console.log('p '+prev);
	// 		prev = val;
	// 		console.log('d '+prev);
	// 		console.log(val);
	// 	}
	// 	else{
	// 	prev = val;
	// 	$(".edit").show();
	// 	$('.category_' + val).show();
	// 	}
	// }

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
		image(inky[0].url);

		}
	);
}

function filePreview(ink){
	$("#id_pictures").text(ink[0].url);
	var text = ""
	for (var i=0; i<ink.length; i++){ 
		text = ink[i].filename + " sucessfully uploaded."
		var li = $('<li>')
			.text(text)
			.appendTo('#pics');
	}
}

function image(url) {
	var img = document.createElement("IMG");
	img.src = url;
	document.getElementById('image').appendChild(img);
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
