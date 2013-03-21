$(function() {
	ZeroClipboard.setDefaults({moviePath: STATIC_URL +'js/ZeroClipboard.swf', 
								trustedDomains: ['s3.amazonaws.com'], 
								allowScriptAccess: 'always'});
	var clip = new ZeroClipboard( $(".clipboard") );
/*	function getURLParameter(name) {
		return decodeURI(
			(RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,null])[1]
		);
	}

	if (getURLParameter('next')) {
		$('.message').show();
	}*/

	// $('#table-listings').tablesorter({ cssHeader: 'table-header'});
});



