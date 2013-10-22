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
        $('.navbar-nav li a').removeClass('active');
        var menuItem = $(elem.data('menu'));
        menuItem.addClass('active');
        document.title = elem.data('title');
        var url = menuItem.attr("href"); //update url without changing pages
        history.pushState({page:url}, url, url);
      } 
  });

  // if(chrome.app.isInstalled) {
    // $('#register_submit').removeProp('disabled');
  // }
  $('#add_extension').click(function(event) {
    event.preventDefault();
    chrome.webstore.install("https://chrome.google.com/webstore/detail/hermes/knfnlfcnohkkbkiibecjhidafmpgchfe", 
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