$('body').scrollspy({ target: '#nav-how' });

$(function() {
  google.maps.visualRefresh = true;
  var mapOptions = {
    center: new google.maps.LatLng(49.5, 60.8), // burlington coords 44.5, -72.8
    zoom: 10,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    disableDefaultUI: true,
    panControl: false,
    zoomControl: false,
    mapTypeControl: false,
    scaleControl: false,
    streetViewControl: false,
    overviewMapControl: false
  };
  var map = new google.maps.Map(document.getElementById("header-map"), mapOptions);
  $("#header-map-overlay").css('visibility', 'visible');

  function getLocationByIP() {
    $.ajax({
      method: 'GET',
      url: 'http://jsonip.appspot.com/',
      success: function(response) {
        $.ajax({
          method: 'GET',
          url: 'https://freegeoip.net/json/' + response.ip,
          success: function(response) {
            gotLocation(response.latitude, response.longitude);
          }
        });
      }
    });
  }

  function gotLocation(lat, lng) {
    map.panTo(new google.maps.LatLng(lat, lng + 0.4));
  }

  getLocationByIP();

  var pathname = window.location.pathname;
    var url = pathname.replace(/(\/)/g,"");
    if (url.length==""){
      $("#what").addClass('nav-highlight');   
    }else{
    $("#" + url).addClass('nav-highlight');
  }

  $('.nav-header').click(function(event) {
      event.preventDefault();         //don't use as normal hyperlinks
      console.log('click');      
      var id = $(this).attr('id');    //find and show relevant partial
      $('.partials').hide();
      $('.' + id).show()
      $('#' + id).addClass('nav-highlight').siblings().removeClass('nav-highlight'); //add/remove nav highlighting
      var url = $(this).attr("href"); //update url without changing pages
      history.pushState({page:url}, url, url);
  });



  /* 
  function handleEvents() {
    var autoValidate = null;
    $(".start-signup").submit(function(e) {
      var address = $(".start-email").val().replace(/ /g, ""),
        username;
      if ((address != "") && validateEmail(address)) {
        $(".username").val(address.substring(0, address.indexOf("@")));
        return true;
      }
      startSignupErr();
      $(".start-email").select();
      return false;
    });
    $(".start-email").keydown(function(e) {
      removeStartSignupErr();
      if (autoValidate != null) clearTimeout(autoValidate);
      autoValidate = setTimeout(function () {
        var address = $(".start-email").val().replace(/ /g, "");
        if (!validateEmail(address)) {
          startSignupErr();
        }
      }, 5000);
    });
  }

  function validateEmail(address) {
    var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;    
    return (regex.test(address));
  }

  function startSignupErr() {
    $(".start-submit").addClass("disable");
    $(".header-signup-button-wrap").addClass("disable");
  }

  function removeStartSignupErr() {
    $(".start-submit").removeClass("disable");
    $(".header-signup-button-wrap").removeClass("disable");
  }

  handleEvents();
   */
});








