$(function(){

  var search_timeout;
  var form = $('#search-form');

  $("#search-form").submit(function(e) {
    e.preventDefault();
    clearTimeout(search_timeout);
    search();
  });

  $('#search_input').keyup(function(e) {
    clearTimeout(search_timeout);
    search_timeout = setTimeout(search, 300);
  });

  function search() {
    history.pushState({}, "Rocket Search", "?" + form.serialize());
    $.ajax({
      type: "GET",
      url:"ajax/",
      data: form.serializeArray(),
      success:function(data, textStatus, jqXHR) {
        $(".listing-table-body").html(data);
      },
      error: function(jqXHR, textStatus, errorThrown) {
        console.log(textStatus);
      }
    });
  }
});