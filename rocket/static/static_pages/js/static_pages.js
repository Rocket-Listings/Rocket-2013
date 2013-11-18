$(function() {
  google.maps.visualRefresh = true;
  var mapTypeStyle = [
    {
      "featureType": "poi",
      "elementType": "labels",
      "stylers": [
        { "visibility": "off" }
      ]
    },{
      "featureType": "administrative.neighborhood",
      "elementType": "labels",
      "stylers": [
        { "visibility": "off" }
      ]
    },{
      "featureType": "water",
      "elementType": "labels",
      "stylers": [
        { "visibility": "off" }
      ]
    },{
      "featureType": "transit",
      "elementType": "labels",
      "stylers": [
        { "visibility": "off" }
      ]
    },{
      "featureType": "road.highway",
      "stylers": [
        { "weight": 1.4 }
      ]
    },{
      "featureType": "road",
      "elementType": "labels.text",
      "stylers": [
        { "visibility": "off" }
      ]
    },{
      "featureType": "water",
      "stylers": [
        { "saturation": -44 },
        { "lightness": -18 },
        { "hue": "#00ccff" }
      ]
    },{
      "featureType": "road"  },{
      "featureType": "road.arterial",
      "stylers": [
        { "weight": 1.4 }
      ]
    },{
      "featureType": "road.arterial",
      "elementType": "labels",
      "stylers": [
        { "visibility": "off" }
      ]
    },{
      "featureType": "road.local",
      "elementType": "labels",
      "stylers": [
        { "visibility": "off" }
      ]
    },{
      "featureType": "poi.park",
      "stylers": [
        { "hue": "#33ff00" }
      ]
    },{
    },{
      "featureType": "road.highway",
      "stylers": [
        { "lightness": 33 }
      ]
    }
  ];
  var mapOptions = {
    center: new google.maps.LatLng(44.475, -73.612), // burlington coords 44.5, -72.8
    zoom: 10,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    disableDefaultUI: true,
    draggable: false,
    scrollwheel: false,
    disableDoubleClickZoom: true,
    styles: mapTypeStyle
  };
  var map = new google.maps.Map(document.getElementById("header-map"), mapOptions);
  $("#header-map-overlay").css('visibility', 'visible');

  function getLocationByIP() {
    $.ajax({
      method: 'GET',
      url: 'https://freegeoip.net/json/' + REMOTE_ADDR,
      success: function(response) {
        gotLocation(response.latitude, response.longitude);
      }
    });
  }

  function gotLocation(lat, lng) {
    console.log(lat, lng);
    map.panTo(new google.maps.LatLng(lat, lng - 0.5));
  }

  // getLocationByIP();


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