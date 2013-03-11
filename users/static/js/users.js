$(function() {
	function getURLParameter(name) {
	    return decodeURI(
	        (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,null])[1]
	    );
	}

	if (getURLParameter('next')) {
		$('.message').show();
	}

});

$(function() {
	$('#table-listings').tablesorter();
  });



