$(document).ready(function(){
$(".preview-pane").hide();
$(".edit").show();
console.log("hey");


  var category = $(".hidden > select option:selected").html().toLowerCase().trim();
  $("a:contains("+category+")").trigger("click");

  if (category == 'apartment and housing' || category == 'rooms and shared' || category == 'sublets and temporary' 
    || category == 'housing wanted' || category == 'housing swap' || category == 'vacation rentals' 
    || category == 'parking and storage' || category == 'office and commercial' || category == 'real estate for sale') {


    $('#1').removeClass("active");
    $('#2').addClass("active");
    $(".li1").removeClass("active");
    $(".li2").addClass("active");
  }

  var base_category = $("li.active").text().toLowerCase().trim();
  $(".l-category").text(base_category + " > " + category);
});

 
