$(function() {
	ZeroClipboard.setDefaults({moviePath: STATIC_URL+'/js/ZeroClipboard.swf'});
	var clip = new ZeroClipboard( $(".clipboard") );
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



