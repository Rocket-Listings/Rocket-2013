MVP Site Features TODO

- Drag and drop photos anywhere to upload, triggering modal
	- Go from modal to listings/create, to fill out info
	- go from listings/create to login/registration, if not already logged in.
	- go finally to listing view, where modal pops up onload with HTML.

- Listing detail needs to look great, so does listing embed html. responsive.
- Listing detail slideshow needs to work, complete with thumbnails, medium images, lightbox large images, and fullsize.
- Listing deletion and editing needs to work
- Login redirects need to work
- Grid listings view needs to work
- listing browsing pagination needs to work
- listing categories page, browse by category
- listing search
- memcached for thumbnails and listings templates
- amazon S3 for images
- MOD_WSGI apache setup
- User info and profile pic

Brian:

Change Date-time format to be shorter (ie. instead of Mar. 3, 2015, 2:29pm make it 03/03/12 2:29pm. That will make the listings_overview table fit)