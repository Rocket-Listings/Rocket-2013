$(document).ready(function(){
	
	function pageLoad() {
		$(".edit").show();
		$(".preview-pane").hide();
	}
	pageLoad();

	$(".preview-btn").click(function() {
		$(".edit").hide();
		$(".preview-pane").show();
		$('.l-description').text($('#id_description').val());
		$('.title').text($('#id_title').val());
		$('.l-location').text("(" + $('#id_location').val() + ")");
		$('.l-price').text("$" + $('#id_price').val());
		var category = $(".hidden > select option:selected").html();
  		var base_category = $("li.active").text().toLowerCase().trim();
  		$(".l-category").text(base_category + " > " + category);

	});
	$(".edit-btn").click(function() {
		$(".edit").show();
		$(".preview-pane").hide();
	});
	$('#wrapper').affix()
		
  	});






//var msie6 = $.browser == 'msie' && $.browser.version < 7;

//		if (!msie6) {
//			var top = $('#wrapper').offset().top - parseFloat($('#wrapper').css('margin-top').replace(/auto/, 0));
//			console.log(top)
//	  		$(window).scroll(function() {
	  			//what the y position of the scroll i
//	  			var y = $(window).scrollTop();
//	  			if (y >= top) {
//	  				$('#wrapper').addClass('fixed');
//	  			} else {
//	  				$('#wrapper').removeClass('fixed');
//	  			}
//	  		});
//		}
