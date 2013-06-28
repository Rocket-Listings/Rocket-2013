$(document).ready(function(){
  var category = $('.hidden').val().toLowerCase().trim();
  $(":contains("+category+")").addClass("selected");

  if (category == 'apartment / housing' || category == 'rooms / shared' || category == 'sublets / temporary' 
    || category == 'housing wanted' || category == 'housing swap' || category == 'vacation rentals' 
    || category == 'parking / storage' || category == 'office / commercial' || category == 'real estate for sale') {

    $('#1').removeClass("active");
    $('#2').addClass("active");
    $("#tab1").removeClass("active");
    $("tab2").addClass("active");
  }
});



function Edit(){
      $(document).ready(function(){
        $(".listing").hide();
        $(".edit").show();
    });
}

function Preview(){
      $(document).ready(function(){
        $(".edit").hide();
        $(".listing").show();
        $('.l-description').text($('#id_description').val());
		    $('.title').text($('#id_title').val());
		    $('.l-location').text("(" + $('#id_location').val() + ")");
		    $('.l-price').text("$" + $('#id_price').val());
    });
}