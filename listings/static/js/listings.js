$(function() {
	ZeroClipboard.setDefaults({moviePath: '/static/js/ZeroClipboard.swf'});
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
});


$(function() {
	$('#table-offers').tablesorter();
  });




$(function(){
	$('.content').hide();
    });

$(function(){
	$('.bottom').hide();
    });

$(function(){
		var firstId = $('.buyer-tiles:first').data('buyerid');
		$('.buyer-tiles[data-buyerid="'+firstId+'"]').click();
		$('.content[data-buyerid="'+firstId+'"]').show();
		$('.bottom[data-buyerid="'+firstId+'"]').show();
    });


$(function(){
		$('.buyer-tiles').click(function(){
			var buyerid = $(event.target).data('buyerid');
			$('.content').hide();
			$('.content[data-buyerid="'+buyerid+'"]').show();
			$('.bottom').hide();
			$('.bottom[data-buyerid="'+buyerid+'"]').show();
	});
});







