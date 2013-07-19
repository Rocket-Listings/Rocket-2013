$(document).ready(function(){
	var timeout;
	$('.search_text').keypress(function(){
		if (timeout) {
			clearTimeout(timeout);
			timeout = null;
		}
			
		timeout = setTimeout(searchAjax, 2000)
	});

	$(document).keyup(function(e) {
    	if(e.which == 13) {
    		timeout = null;
        	searchAjax();
    	}
	});

	$(document).keyup(function(e) {
    	if(e.which == 20) {
    		clearTimeout(timeout);
    		timeout = null;
    	}

    	timeout = setTimeout(searchAjax, 2000)
	});
});

function searchSuccess(data, textStatus, jqXHR)
{
	$(".listing_table").html(data);
}

function searchAjax()
{
	$.ajax({
		type: "POST",
		url:"ajax/",
		data: {
			"search_text" : $(".search_text").val(),
			"csrfmiddlewaretoken" : $("input[name=csrfmiddlewaretoken]").val()
		},
		success:searchSuccess
	});
}