$(document).ready(function(){
  $(".edit").hide();
  $(".preview-pane").show();
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

  var is_housing = 0;

  if (category == "housing swap"){
    is_housing = 1;
  }
  else if (category == "housing wanted"){
    is_housing = 2;
  }
  else {
    is_housing = 0;
  }

  string = category.split(" ");
  category = string[0];

  var specs = $(".specifications p").length;

  if (is_housing == 1) {
    $(".preview-pane .category_" + category +":eq(0)").show();
    for (var i=0;i<specs;i++)  {
      var spec_value = $('.specifications:eq('+i+')').val();
      $('.table_preview_' + category + ':eq(0) input:eq('+i+')').val(spec_value);
      $('.table_' + category + ':eq(0) input:eq('+i+')').val(spec_value);
    }

  }

  else if (is_housing == 2) {
    $(".preview-pane .category_" + category +":eq(1)").show();
    for (var i=0;i<specs;i++){
      var spec_value = $('.specifications:eq('+i+')').val();
      $('.table_preview_' + category + ':eq(1) input:eq('+i+')').val(spec_value);
      $('.table_' + category + ':eq(1) input:eq('+i+')').val(spec_value);
    }

  }

  else {
      $('.category_' + category, ".preview-pane").show();
    for (var i=0;i<specs;i++){
      var spec_value = $('.specifications p:eq('+i+')').html();
      $('.table_preview_' + category + ' input:eq('+i+')').val(spec_value);
      $('.table_' + category + ' input:eq('+i+')').val(spec_value);
    }

  }
});