$(function() {
  
  $( document ).ready(function() {
    var pathname = window.location.pathname;
    console.log(pathname);
    if (pathname == '/' || pathname == '/manage/' || pathname == '/trust/' || pathname == '/profile/'){
      $('.midline').show();
    }else{
      $('.midline').hide();
    }
  });

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
      if (elem.selector == '#login-partial' || elem.selector == '#register-partial' || elem.selector == '#about-partial' || elem.selector == '#pricing-partial'){
        $('.midline').hide();
      }else{
        $('.midline').show();
      }

      if (elem.selector == '#manage-partial'){
        $('.manage').addClass('active');
      }

      // if (elem.selector == '#login-partial'){
      //   $('.midline').hide();
      // }else{
      //   $('.midline').show();
      // }
            

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

  var isOpera = !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0;
  var isChrome = !!window.chrome && !isOpera;

  if (isChrome == false) {
    $('#chrome-extension-button').html("<span class = 'help-block'>It looks like you don't have Chrome installed. To autopost to craigslist from Rocket please <a href = 'https://www.google.com/intl/en/chrome/browser/'> install the Chrome browser.</a></span>");
  }
});