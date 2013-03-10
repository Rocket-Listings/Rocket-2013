$(function() {
	ZeroClipboard.setDefaults({moviePath: STATIC_URL+'js/ZeroClipboard.swf'});
	var clip = new ZeroClipboard( $(".clipboard") );

	var photoId = parseInt((window.location.hash || "").substring(1));
	if(photoId) {
		if($($('.l-thumbnails img')[photoId]).attr('data-id') == photoId) {
			fillStage($($('.l-thumbnails img')[photoId]));
		} else {
			$('.l-thumbnails img').each(function(index, element) {
				if($(element).attr('data-id') == photoId){
					fillStage($(element));
					return false; // break iteration
				}
			});
		}
	}

	$('.l-thumbnails img').click(function(event){
		fillStage($(event.target));
	});

	function fillStage(image) {
		$(".l-stage img").attr('src', image.attr('data-full'));
		id = image.attr('data-id');
		window.location.hash = image.attr('data-id');
	}

	var cl_embed = $('.cl-embed');
	if(cl_embed) {
		cl_embed.click(function(e) {
			cl_embed.select();
		});
	}
});