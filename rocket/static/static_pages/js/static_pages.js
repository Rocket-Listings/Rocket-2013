$(function() {
  

  $('a').click(function(event) {
      var elem = $($(this).data('href'));
      if (elem.length > 0) {
        event.preventDefault();
        elem.siblings().hide();
        elem.show();
        $('.navbar-nav a').removeClass('active');
        var menuItem = $(elem.data('menu'));
        menuItem.addClass('active');
        document.title = elem.data('title');
        var url = menuItem.attr("href"); //update url without changing pages
        history.pushState({page:url}, url, url);
      } 
      if (elem.selector == '#login-partial' || elem.selector == '#register-partial'){
        $('.midline').hide();
      }else{
        $('.midline').show();
      }
            

  });

  // if(chrome.app.isInstalled) {
    // $('#register_submit').removeProp('disabled');
  // }
  $('#add_extension').click(function(event) {
    event.preventDefault();
    chrome.webstore.install("https://chrome.google.com/webstore/detail/knfnlfcnohkkbkiibecjhidafmpgchfe", 
      function() {
        $(this).find('.before').hide();
        $(this).removeClass('btn-warning').addClass('btn-success disabled');
        $(this).find('.after').show();        
        // $('#register_submit').removeProp('disabled');
      }, function() {
        alert("Unfortunately a large part of our site breaks if you don't install this chrome extension");
    });
  });
});