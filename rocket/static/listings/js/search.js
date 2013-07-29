$(function(){
  var timeout;
  $(".search-form").submit(e) {
    e.preventDefault();
    search();
  }

  $('.search_text').keyup(function(e){
    clearTimeout(timeout);
    timeout = setTimeout(search, 1000);
  });

  function search() {
    $.ajax({
      type: "POST",
      url:"/search/ajax/",
      data: $(this).serialize(),
      success:function(data, textStatus, jqXHR) {
        $(".listing_table").html(data);
      }
    });
  }
});