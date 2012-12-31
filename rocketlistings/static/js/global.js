$(function(){
	// Setup fancybox
	$(".fancybox").fancybox();

	// Setup uploader
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
		callbacks: {
			onComplete: function(id, fileName, responseJSON) { // not working
				if(responseJSON.success) {
					alert("success!");
				} else {
					alert('fail!');
				}
			},
			onAllComplete: function(uploads) {
				// uploads is an array of maps
				// the maps look like this: {file: FileObject, response: JSONServerResponse}
				alert("All complete!");
			}
		},
		multiple: true
	});
});