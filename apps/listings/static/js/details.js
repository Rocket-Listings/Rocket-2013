$(document).ready(function(){
  var category = $('.hidden').text().toLowerCase().trim();
  $("a:contains("+category+")").trigger("click");

  if (category == 'apartment / housing' || category == 'rooms / shared' || category == 'sublets / temporary' 
    || category == 'housing wanted' || category == 'housing swap' || category == 'vacation rentals' 
    || category == 'parking / storage' || category == 'office / commercial' || category == 'real estate for sale') {

    $('#1').removeClass("active");
    $('#2').addClass("active");
    $("#tab1").removeClass("active");
    $("tab2").addClass("active");
  }

  var base_category = $("li.active").text().toLowerCase().trim();
  $(".l-category").text(base_category + " > " + category);
});

function Edit(){
      $(document).ready(function(){
        $(".preview-pane").hide();
        $(".edit").show();
    });
}

function Preview(){
  $(".edit").hide();
  $(".preview-pane").show();
  $('.l-description').text($('#id_description').val());
	$('.title').text($('#id_title').val());
	$('.l-location').text("(" + $('#id_location').val() + ")");
	$('.l-price').text("$" + $('#id_price').val());
  var category = $('.hidden').text().toLowerCase().trim();
  var base_category = $("li.active").text().toLowerCase().trim();
  $(".l-category").text(base_category + " > " + category);

}