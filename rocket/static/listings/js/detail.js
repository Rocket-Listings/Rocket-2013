$(function() {
  var ListingEditView = Backbone.View.extend({
    el: '#info-fieldset',
    events: {
      // "change input": "changed",
      "keyup .title":   "renderPageTitle",
      "change .title":  "changed",
      "change .price":  "changed",
    },
    initialize: function(options) {
      this.categoryEditView = new CategoryEditView(options);
      this.locationEditView = new LocationEditView(options);

      _.bindAll(this, 'changed');
    },
    changed: function(e) {
      var input = $(e.currentTarget);
      this.model.save(input.attr('name'), input.val(), {patch: true});
    },
    renderPageTitle: function(e) {
      var title = $(e.currentTarget).val();
      if (title.length > 0) {
        $('.listing-title').text(title);
        $('#preview-btn').removeAttr('disabled');
      } else {
        $('.listing-title').text("Create a listing");
        $('#preview-btn').attr('disabled', 'disabled');
      }
    }
  });

  var CategoryEditView = Backbone.View.extend({
    el: '#category-fieldset',
    events: {
      "click .tab-pane .cat": "changed"
    },
    initialize: function(options) {
      _.bindAll(this, 'changed');
      this.render();
      // this.parseToModel();
    },
    changed: function(e) {
      var elem = $(e.currentTarget);
      var nextCat = elem.data('id');
      var prevCat = this.model.get('category');
      this.render(nextCat, prevCat);
      this.model.save('category', nextCat, { patch: true });

    },
    // parseToModel: function() {
    //   this.model.set('category', $('#id_category').val());
    //   this.render();
    // },
    render: function(nextCat, prevCat) {
      if (!nextCat) {
        var nextCat = this.model.get('category');
      }
      if (prevCat) {
        $('.tab-pane .cat[data-id="{0}"]'.format(prevCat)).removeClass('selected');
      }
      var cat = $('.tab-pane .cat[data-id="{0}"]'.format(nextCat));
      cat.addClass('selected');
      // cat.siblings().removeClass('selected');
      // switch to tab
      $('.nav-tabs a[href="#{0}"]'.format(cat.parent('.tab-pane').attr('id'))).tab('show');
    }
  });

  var LocationEditView = Backbone.View.extend({
    el: '#marketplace-location-fieldset',
    events: {
      "change #id_location": "changed",
      "click #location-btn": "getLocationByBrowser",
    },
    initialize: function() {
      $(".form-select").select2();
      $(".form-select").show();
      _.bindAll(this, 'mapResize', 'changed');
      this.geocoder = new google.maps.Geocoder();
      this.render();
      $('.edit-btn').on('shown.bs.tab', this.mapResize);
    },
    changed: function(e) {
      var input = $(e.currentTarget);
      this.model.save(input.attr('name'), input.val(), { patch: true });
    },
    render: function() {
      var val = $('#id_location').val();
      if (val.length > 0) {
        this.geocode(val);
      } else {
        this.getLocationByIP();
      }
    },

    mapInit: function(latlng, zoom) {
      if (this.map) {
        this.map.panTo(latlng);
      } else {
        google.maps.visualRefresh = true;
        var mapOptions = {
          center: latlng || new google.maps.LatLng(49.5, 60.8), // burlington coords 44.5, -72.8
          zoom: zoom || 13,
          mapTypeId: google.maps.MapTypeId.ROADMAP,
          disableDefaultUI: true,
          draggable: false,
          scrollwheel: false,
          disableDoubleClickZoom: true,
          styles: this.mapTypeStyle
        };
        this.map = new google.maps.Map(document.getElementById("location-map"), mapOptions);
      }
    },

    mapResize: function(e) {
      google.maps.event.trigger(this.map, 'resize');
    },

    toggleLoading: function(str) {
      // console.log(str);
      this.$('.loading-spinner').toggle();
    },

    getLocationByBrowser: function(e) {
      this.toggleLoading('getLocationByBrowser start');
      var that = this;
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
          var lat = position.coords.latitude;
          var lng = position.coords.longitude;
          var latlng = new google.maps.LatLng(lat, lng);
          that.mapInit(latlng, 14);
          that.toggleLoading('getLoctationByBrowser stop success');
          that.reverseGeocode(latlng);
        }, that.mapError, { enableHighAccuracy: true });
      } else {
        that.toggleLoading('getLoctationByBrowser stop no navigator.geoLocation');
        this.mapError("Error: Old or non-compliant browser.");
      }
    },

    geocode: function(address) {
      this.toggleLoading();
      var that = this;
      this.geocoder.geocode({'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
          var latlng = results[0].geometry.location;
          that.mapInit(latlng, 12);
          that.toggleLoading('geocode stop success');
        } else {
          that.toggleLoading('geocode stop geocoder status not ok');
          that.mapError('Geocode was not successful for the following reason: ' + status);
        }
      });
    },

    reverseGeocode: function(latlng) {
      var that = this;
      var lat = latlng.lat();
      var lng = latlng.lng();
      /*$.ajax({
        method: 'GET',
        url: 'http://api.geonames.org/findNearestAddressJSON?lat={0}&lng={1}&username=rocketlistings'.format(lat, lng),
        success: function(response) {
          var addr = response.address;
          console.log(addr);
          that.$('#id_location').val([addr.streetNumber, addr.street, addr.placaename, addr.adminCode1].join(' ')).trigger('change');
        }
      });*/
      this.geocoder.geocode({'latLng': latlng}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
          if (results[0]) {
            that.$('#id_location').val(results[0].formatted_address).trigger('change');
          } else {
            that.mapError('No results found');
          }
        } else {
          that.mapError('Geocoder failed due to: ' + status);
        }
      });
    },

    getLocationByIP: function() {
      var that = this;
      $.ajax({
        method: 'GET',
        url: 'http://jsonip.appspot.com/',
        success: function(response) {
          $.ajax({
            method: 'GET',
            url: 'https://freegeoip.net/json/' + response.ip,
            success: function(response) {
              var latlng = new google.maps.LatLng(response.latitude, response.longitude);
              that.mapInit(latlng, 12);
              that.toggleLoading();
              that.reverseGeocode(latlng);
            },
            error: function(jqXHR, textStatus, errorThrown) {
              console.log('freegeoip error');
              console.log(textStatus);
            }
          });
        },
        error: function(jqXHR, textStatus, errorThrown) {
          console.log('jsonip error');
          console.log(textStatus);
        }
      });
    },

    mapError: function(error) {
      this.toggleLoading();
      console.log("Maps error");
      console.log(error);
    },
    mapTypeStyle: [
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
    ]
  });

  var SpecEditView = Backbone.View.extend({
    el: '#spec-fieldset',
    template: Mustache.compile($('#spec-edit-template').html()),
    events: {
      "change input": "parseToCollection",
      "change .description":  "changed"
    },
    initialize: function(options) {
      this.parseToCollection();
      this.listenTo(this.model, 'change:category', this.switchCategory);
      _.bindAll(this, "changed");
      this.defaults = $.parseJSON(this.$('#initial-specs').html());
      this.switchCategory(this.model);
    },
    changed: function(e) {
      var input = $(e.currentTarget);
      this.model.save(input.attr('name'), input.val(), { patch: true });
    },
    parseToCollection: function() {
      var specs = $('.spec-data').map(function(index, input) {
        return new Spec({
          id: input.data('id'),
          name: input.attr('name'),
          value: input.val(),
        });
      });
      this.collection.set(specs.get());
      return this;
    },
    switchCategory: function(model) {
      var cat = model.get('category');
      var catName = $('.cat[data-id="{0}"]'.format(cat)).html(); // workaround
      var specNames = this.defaults[catName];
      if (!specNames) {
        return;
      }
      var total = parseInt(this.$('#id_spec_set-TOTAL_FORMS').val());
      var initial = parseInt(this.$('#id_spec_set-INITIAL_FORMS').val());
      var specs = _.map(specNames, function(name, _index) {
        return {
          index: total + _index,
          name: name,
          value: ""
        };
      });
      var context = { 'specs': specs };
      this.$('#id_spec_set-TOTAL_FORMS').val(total+specNames.length);
      this.$('#spec-row').html(this.template(context));
    }
  });

  var PhotoEditView = Backbone.View.extend({
    el: '#photo-fieldset',
    events: {
      "click .toggle-view": "toggleView"
    },
    picker_options: {
      mimetype:"image/*",
      multiple: true,
      container: 'fp-container',
      services: ['COMPUTER', 'URL', 'FACEBOOK', 'DROPBOX']
    },
    store_options: {
      location:"S3",
      path: '/photos/',
      access: 'public'
    },
    initialize: function(options) {
      filepicker.setKey('ATM8Oz2TyCtiJiHu6pP6Qz');
      filepicker.pickAndStore(this.picker_options, this.store_options, _.bind(this.onSuccess, this), this.onError);
      _.bindAll(this, 'updateOrder');
      this.bindSortable();
      // want to compile these after enabling UI functionality
      this.template = Mustache.compile(this.$('#photo-thumbnail-template').html());
      // this.parseToCollection();
    },
    // parseToCollection: function() {
    //   var form = $('.listing-form:first').serializeObject();
    //   var total = parseInt(form['listingphoto_set-TOTAL_FORMS']);
    //   var photolist = [];
    //   for (var i = 0; i < total; i++) {
    //     var key = 'listingphoto_set-{0}-'.format(i);
    //     console.log(form);
    //     photolist.push(new Photo({
    //       url: form[key + 'url'],
    //       key: form[key + 'key'],
    //       index: i,
    //       // listing: form[key + 'listing'],
    //       order: form[key + 'ORDER'],
    //       id: form[key + 'id'],
    //       markedDelete: form[key + 'DELETE'] || false
    //     }));
    //   }
    //   this.collection.set(photolist); // {merge: true});
    //   this.render();
    //   return this;
    // },
    render: function() {
      if (this.collection.length > 0) {
        var context = { 'photos': this.collection.toJSON() };
        console.log(context);
        var thumbnails = this.template(context);
        this.$('#photos').append(thumbnails);
        this.bindSortable();
        this.$('.photo-view').fadeIn();
        this.$('.upload-view').hide();
      } else {
        this.$('.photo-view').hide();
        this.$('.upload-view').show();
      }
    },
    onSuccess: function(InkBlobs) {
      // update management form
      // var totalInput = this.$('#id_listingphoto_set-TOTAL_FORMS');
      // var total = parseInt(totalInput.val());
      // totalInput.val(total + InkBlobs.length);
      // var initial = parseInt(this.$('#id_listingphoto_set-INITIAL_FORMS').val());
      // prepare view context variables
      var total = 0,
          initial = 0;
      var photos = [];
      _.each(InkBlobs, function(blob, index) {
        photos.push(new Photo({
          index: initial + index,
          order: initial + index,
          url: blob.url,
          key: blob.key,
          src: "http://static.rocketlistings.com/" + blob.key,
          markedDelete: false
        }));
      });
      this.collection.set(photos);
      this.render();
    },
    onError: function(type, message) {
      console.log('('+type+') '+ message);
    },
    toggleView: function(e) {
      if (e) {
        e.preventDefault();
      }
      $('.upload-view').toggle();
      $('.photo-view').toggle();
    },
    updateOrder: function(e, ui) {
      var that = this;
      this.$('.sortable div').each(function(_index, item) {
        var id = $(item).data('id');
        that.collection.get(id).set('order', _index);
      });
    },
    bindSortable: function() {
      this.$('.sortable').sortable()
        .unbind('sortupdate')
        .bind('sortupdate', this.updateOrder);
    }
  });

  var PreviewView = Backbone.View.extend({
    el: '#preview-container',
    template: Mustache.compile($('#preview-template').html()),
    events: {
      "click .preview-thumbnails img": "fillStage"
    },
    initialize: function(options) {
      this.listing = options.listing;
      this.photos = options.photos;
      this.specs = options.specs;

      this.render();

      this.listenTo(this.listing, 'change add remove', this.render);
      this.listenTo(this.specs, 'change add remove', this.render);
      this.listenTo(this.photos, 'change add remove', this.render);

      _.bindAll(this, 'publish');
      $('.publish-btn').click(this.publish);
    },
    render: function(changedModel) {
      var context = {
        listing: this.listing.toJSON(),
        photos: this.photos.toJSON(),
        specs: this.specs.toJSON(),
        has_specs: this.specs.length > 0
      };
      if (this.photos.length > 0) {
       context.first_photo = this.photos.at(0).toJSON();
      }
      this.$el.html(this.template(context));
    },
    publish: function(e) {
      console.log('publish');
    },
    fillStage: function(e) {
      e.preventDefault();
      var photo = $(e.currentTarget);
      var src = photo.attr('data-full') || photo.attr('src');
      this.$(".preview-stage img").attr('src', src);
      window.location.hash = photo.attr('data-id');
      return this;
    }
  });

  // models are split up by their corresponding django form
  var Listing = Backbone.Model.extend({
    urlRoot: '/listings/api/'
  });
  var Spec = Backbone.Model.extend({});
  var SpecList = Backbone.Collection.extend({
    model: Spec
  });
  var Photo = Backbone.Model.extend({});
  var PhotoList = Backbone.Collection.extend({
    model: Photo,
    comparator: 'order'
  });

  // number after /listing/
  var listingId = parseInt(window.location.pathname.split('/listings/')[1].split('/')[0]);
  // we don't want all the input fields
  var form = $('.listing-form:first').serializeObject();
  var listing = new Listing({
    id: listingId,
    title: form.title || null,
    category: form.category || null,
    price: form.price || null,
    description: form.description || null,
    location: form.location || null,
    market: form.market || null,
    CL_link: null,
    CL_view: null,
  });
  var specs = new SpecList;
  var photos = new PhotoList;

  var specEditView = new SpecEditView({ collection: specs, model: listing  });
  var photoEditView = new PhotoEditView({ collection: photos });
  var listingEditView = new ListingEditView({ model: listing });

  var previewView = new PreviewView({ listing: listing, specs: specs, photos: photos });

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
    }
  });

  var SidebarView = Backbone.View.extend({
    el: '.detail-sidebar',
    events: {
      // "click .draft-btn": "save",
      "click div.btn-group[data-toggle-name='listing-pane-toggle'] a": "toggleView",
      // "click .save-btn": "publish"
    },
    initialize: function() {
      this.listenTo(listing, 'request', this.showSaving);
      this.listenTo(listing, 'sync', this.hideSaving);

      this.listenTo(specs, 'request', this.showSaving);
      this.listenTo(specs, 'sync', this.hideSaving);

      this.listenTo(photos, 'request', this.showSaving);
      this.listenTo(photos, 'sync', this.hideSaving);
    },
    showSaving: function(event) {
      $('#loading').show();
    },
    hideSaving: function(event) {
      $('#loading').hide();
    },
    toggleView: function(e) {
      $(this).siblings().removeClass("active");
      $(this).addClass("active");
    },
    // save: function(e) {
    //   $('#submit-draft').click();
    // },
    publish: function(e) {
      console.log('publish');
    }
  });
  var sidebarView = new SidebarView;
});
