$(document).ready(function(){
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
		prev = val;
		$(".edit").show();
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
