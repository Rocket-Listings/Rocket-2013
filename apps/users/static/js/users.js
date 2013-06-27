$(function() {
	function handleEvents() {
		var prevData = null;
		$(".edit").click(function(e) {
			e.preventDefault();
			prevData = $(this).parent().prev().val();
			$(this).parent().parent().hide();
			$(this).parent().parent().next().show();
			if ($(this).parent().parent().next().find("input")[1]) {
				$(this).parent().parent().next().find("input")[0].focus();
			}
			else{
				$(this).parent().parent().next().find("select")[0].focus();
			}
			$(".edit").replaceWith("<span class='edit muted'>Edit</span>");
			$(".change-password").replaceWith("<span class='muted'>Change password</span>");
			$("table").removeClass("table-hover");
		});
		$(".user-info-form").submit(function() {
			var csrftoken = $.cookie('csrftoken');
			$.ajax({
				data: $(this).serialize(),
				type: $(this).attr('method'),
				url: $(this).attr('action'),
				beforeSend: function(xhr) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				},
				success: function(response) {
					console.log(response[0].fields);
				}
			});
			return false;
		});
	}


var map;
function initialize() {
  	var mapOptions = {
    	zoom: 8,
    	center: new google.maps.LatLng(-34.397, 150.644),
    	mapTypeId: google.maps.MapTypeId.ROADMAP
  	};
  	map = new google.maps.Map(document.getElementById('map-canvas'),
     mapOptions);
};

var geocoder = new google.maps.Geocoder();
var address = "Burlington, Vt";
geocoder.geocode( { 'address': address}, function(results, status) {
	if (status == google.maps.GeocoderStatus.OK) {
		latitude = results[0].geometry.location.lat();
		longitude = results[0].geometry.location.lng();
		var myLatlng = new google.maps.LatLng(latitude,longitude);
		var marker = new google.maps.Marker({
    		position: myLatlng,
		});
		marker.setMap(map);
		console.log(longitude);
		console.log(latitude);
    };
});

google.maps.event.addDomListener(window, 'load', initialize);


});