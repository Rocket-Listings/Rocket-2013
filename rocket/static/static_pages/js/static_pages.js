$(function() {
  
  $( document ).ready(function() {
    var pathname = window.location.pathname;
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

  showHelp();
  if($('#hermes-is-active').length) {
    console.log('installed');
    hermesInstallSuccess();
  }

  $('.hermes-install-btn').click(function(event) {
    event.preventDefault();
    // must be consistent with the link tag in templates/static_pages/index.html
    var hermesURL = "https://chrome.google.com/webstore/detail/knfnlfcnohkkbkiibecjhidafmpgchfe";
    // let's uncomment this when the Chrome extension is updated, for now it's better that the button work multiple times.
    // if (!$('#hermes-is-active').length) {
      chrome.webstore.install(hermesURL, hermesInstallSuccess, hermesInstallFailure);
    // }
  });

  function showHelp() {
    $('.hermes-error').addClass('hide');
    var isOpera = !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0;
    var isChrome = !!window.chrome && !isOpera;
    if (isChrome) {
      $('.hermes-help-chrome').removeClass('hide');
    } else {
      $('.hermes-help-non-chrome').removeClass('hide');
    }
  }
  function hideHelp() {
    $('.hermes-help-chrome').addClass('hide');
    $('.hermes-help-non-chrome').addClass('hide');    
  }
  function hermesInstallSuccess() {
    showHelp();
    $('#hermes-install').removeClass('has-error').addClass('has-success');    
    var hermesInstall = $('#hermes-install');    
    hermesInstall.find('.before').hide();
    hermesInstall.find('.hermes-install-btn')
      .removeClass('btn-warning')
      .addClass('btn-success disabled');
    hermesInstall.find('.after').removeClass('hide');
  }
  function hermesInstallFailure(error) {
    hideHelp();
    $('.hermes-error #error-message').html(error);
    $('.hermes-error').removeClass('hide');
    $('#hermes-install').addClass('has-error');
  }
});