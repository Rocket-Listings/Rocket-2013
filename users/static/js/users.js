$(function() {
	ZeroClipboard.setDefaults({moviePath: STATIC_URL +'js/ZeroClipboard.swf', 

								trustedDomains: [   'beta.rocketlistings.com', 
                    'rocketlistings.com', 
                    'www.rocketlistings.com', 
                    'rocket-listings.herokuapp.com',
                    'quiet-beyond-7797.herokuapp.com'
                    ]});
	
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



