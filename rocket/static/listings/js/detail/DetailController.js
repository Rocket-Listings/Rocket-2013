$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
  }
});

$(function() {
  var json = listingJSON;
  var spec_set = json.spec_set, 
      listingphoto_set = json.listingphoto_set;

  delete json.spec_set;
  delete json.listingphoto_set;  
  delete json.user;

  var listing = new Listing(json),
      specs = new SpecList(spec_set, {
        listing: listing
      }),
      photos = new PhotoList(json.listingphoto_set);

  var models = {
    listing: listing,
    specs: specs,
    photos: photos
  }
  var views = {
    preview: new PreviewView(models),
    specEdit: new SpecEditView({ collection: specs, listing: listing  }),
    photoEdit: new PhotoEditView({ collection: photos, listing: listing }),
    listingEdit: new ListingEditView({ model: listing }),
    sidebarView: new SidebarView(models)
  };
});