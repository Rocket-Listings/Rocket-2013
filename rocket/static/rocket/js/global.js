// Get cookie for csrf token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// $(function(){
// //  $(".fancybox").fancybox();

// 	// menu activation
// 	var url = window.location.url;
// 	var path = window.location.pathname;
// 	var links = $('.action-menu a[href="'+url+'"], .action-menu a[href="'+path+'"]')
// 	links.parent().addClass('active');
// 	links.addClass('active');


// 	var exp = /listings\/\d+/gi;
// 	var listingid = 0;
// 	var listingMatch = location.pathname.match(exp);
// 	if (listingMatch) {
// 		listingMatch[0].substring(9);
// 	}
// 	var fileNum = 0;
// 	var uploader = $('#file-uploader').fineUploader({
// 		debug: true,
// 		request: {
// 			endpoint: '/listings/ajax-photo-upload/',
// 			customHeaders: {
// 				'X-CSRFToken': $.cookie('csrftoken'),
// 			}
// 		},
// 		validation: {
// 			allowedExtensions: ['jpg', 'jpeg', 'png', 'gif'],
// 			sizeLimit: 10485760,
// 			acceptFiles: 'image/*'
// 		},
// 		multiple: true,
// 		dragAndDrop: {
// 			disableDefaultDropzone: true,
// 	//		extraDropzones: [$('.wrap')]
// 		}
// 	}).on('complete', function(event, id, filename, responseJSON){
// 		//response = $.parseJSON(responseJSON);
// 		if(responseJSON.success) {
// 			fileNum--;
// 			if(fileNum === 0) {
// 				$('.finish-upload-button').removeClass('disabled');
// 			} else {
// 				// error
// 			}	
// 		} else {
// 			// TODO: indicate failure to user
// 		}
// 	}).on('submit', function(event, id, filename) {
// 		$('.finish-upload-button').addClass('disabled');
// 		$(this).fineUploader('setParams', {'order':fileNum++, 'listingid':listingid});
//   	});
// });