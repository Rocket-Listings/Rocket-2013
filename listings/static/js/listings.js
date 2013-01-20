$(function() {
	ZeroClipboard.setDefaults({moviePath: '/static/js/ZeroClipboard.swf'});
	var clip = new ZeroClipboard( $(".clipboard") );
	console.log('hello world');
	var currentImageID = window.location.hash;
	var stageFilled = false;
	if(currentImageID) {
		$('.l-gallery .l-thumbnails').each(function(index, element) {
			if($(element).attr('data-id') == currentImageID){
				fillStage(element);
				stageFilled = true;
				return false;
			}
		});
	} 

	if(!stageFilled) { 
		fillStage($('.l-gallery .l-thumbnails img').first());
	}
	console.log('hello');
	$('.l-gallery .l-thumbnails img').click(function(event){
		fillStage($(event.target));

	});

	function fillStage(image) {
		$(".l-gallery .l-stage img").attr('src', image.attr('data-full'));
	}
});