$(window).load(function(){
  search();
});

$(document).ready(function(){
  var timeout;

  function eventHandlers() {
    $("#search_button").click(handleClick);
  }

  function handleClick(e) {
    timeout = null;
    search();
  }

  $('.search_text').keyup(function(e){

    if (timeout) {
      clearTimeout(timeout);
      timeout = null;
    }

    if(e.which == 13) {
        timeout = null;
        search();
      }
      else {
      timeout = setTimeout(search, 1000);
    }
  });

  eventHandlers();
});

  function search() {
    $.ajax({
      type: "POST",
      url:"ajax/",
      data: {
        "search_text" : $(".search_text").val(),
        "csrfmiddlewaretoken" : $("input[name=csrfmiddlewaretoken]").val()
      },
      success:function(data, textStatus, jqXHR) {
        $(".listing_table").html(data);
      }
    });
  }
