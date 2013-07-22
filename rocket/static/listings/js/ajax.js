$(window).load(function(){
	searchAjax();
});

$(document).ready(function(){
	var timeout;
	$('.search_text').keyup(function(e){

		if (timeout) {
			clearTimeout(timeout);
			timeout = null;
		}

		if(e.which == 13) {
    		timeout = null;
    		searchAjax();
    	}
    	else {
			timeout = setTimeout(searchAjax, 2000);
		}
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