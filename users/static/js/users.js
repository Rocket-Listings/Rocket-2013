$(function() {
	ZeroClipboard.setDefaults({moviePath: STATIC_URL +'js/ZeroClipboard.swf', 

								trustedDomains: ['http://quiet-beyond-7797.herokuapp.com/'], 
								allowScriptAccess: 'always'});
	
	var clip = new ZeroClipboard( $(".clipboard") )
	clip.on( 'mousedown', function(client){ $(this).addClass("active"); })
	clip.on( 'mouseup', function(client){ $(this).removeClass("active"); });
/*	function getURLParameter(name) {
		return decodeURI(
			(RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,null])[1]
		);
	}

	if (getURLParameter('next')) {
		$('.message').show();
	}*/

	$('#table-listings').tablesorter();
});



