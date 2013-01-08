$(function(){

	// Setup uploader
	// pulled from number in url, if no matches then listingid is sent as 0.
	// first 'or' is because match returns null if no match, which causes an error on substring
	var listingid = (location.pathname.match(/listings\/\d+/) || "").substring(9) || 0;
	fileNum = 0;

	$('#file-uploader').fineUploader({
		debug: true,
		request: {
			endpoint: '/listings/ajax-photo-upload/',
			customHeaders: { 'X-CSRFToken': $.cookie('csrftoken') },
			params: {
				'order': function() {
					return fileNum++;
				},
				'listingid':listingid
			}
		},
		validation: {
			allowedExtensions: ['jpg', 'jpeg', 'png', 'gif'],
			sizeLimit: 10485760,
			acceptFiles: 'image/*'
		},
		multiple: true
	}).on('complete', function(event, id, fileName, responseJSON) {
		if(filecount === 1) {
			if(responseJSON.success) {
				//alert("success!");
			} else {
				//alert('fail!');
			}
		} else {
			filecount--;
		}
	});

/*	$('.drag-and-drop').on('click', function(event) {
		event.preventDefault();
		uploader.addFiles($('input[name="file"]'));
	});*/
});