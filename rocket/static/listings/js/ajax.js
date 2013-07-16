$(document).ready(function(){	
	$('.search_text').keyup(function(){

		$.ajax({
			type: "POST",
			url:"ajax/",
			data: {
				"search_text" : $(".search_text").val(),
				"csrfmiddlewaretoken" : $("input[name=csrfmiddlewaretoken]").val()
			},
			success:searchSuccess,
			dataType: 'html'
		});

	});


	function searchSuccess(data, textStatus, jqXHR) {
		$(".listing_table").html(data);
	}
});

$(function(){
	
	$('.search_text').keyup(function(){

		$.ajax({
			type: "POST",
			url:"ajax/",
			data: {
				"search_text" : $(".search_text").val(),
				"csrfmiddlewaretoken" : $("input[name=csrfmiddlewaretoken]").val()
			},
			success:searchSuccess,
			dataType: 'html'
		});

	});
});

function searchSuccess(data, textStatus, jqXHR)
{
	$(".listing_table").html(data);
}