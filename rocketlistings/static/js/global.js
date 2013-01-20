$(function(){
// 	Setup fancybox
//  $(".fancybox").fancybox();
	
//	var listingid = (location.pathname.match(/listings\/\d+/) || "").substring(9) || 0;
	fileNum = 0;
	var uploader = $('#file-uploader').fineUploader({
		debug: true,
		request: {
			endpoint: '/listings/ajax-photo-upload/',
			customHeaders: {
				'X-CSRFToken': $.cookie('csrftoken'),
			}
		},
		validation: {
			allowedExtensions: ['jpg', 'jpeg', 'png', 'gif'],
			sizeLimit: 10485760,
			acceptFiles: 'image/*'
		},
		multiple: true
	}).on('complete', function(event, id, filename, responseJSON){
		//response = $.parseJSON(responseJSON);
		if(responseJSON.success) {
			fileNum--;
			if(fileNum === 0) {
				$('.finish-upload-button').removeClass('disabled');
			} else {
				// error
			}	
		} else {
			// TODO: indicate failure to user
		}
	}).on('submit', function(event, id, filename) {
		$('.finish-upload-button').addClass('disabled');
	    $(this).fineUploader('setParams', {'order':fileNum++, 'listingid':listingid});
  });
});