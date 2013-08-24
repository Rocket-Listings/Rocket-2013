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
      this.listenTo(this.model, 'invalid', this.validationError);
    },
    validationError: function(model, error) {
      if (error.category) {
        var elem = $('#category-error');
        elem.html(error.category.join(' ,'));
        elem.parent().show();
      };
      if (error.title) {
        var elem = $('#title-error');
        elem.html(error.title.join(' ,'));
        elem.parent().addClass('has-error');
      };
      if (error.price) {
        var elem = $('#price-error');
        elem.html(error.price.join(' ,'));
        elem.parent().addClass('has-error');        
      };
      if (error.description) {
        var elem = $('#description-error');
        elem.html(error.description.join(' ,'));
        elem.parent().addClass('has-error');        
      };
      if (error.location) {
        var elem = $('#location-error');
        elem.html(error.location.join(' ,'));
        elem.parent().addClass('has-error');        
      };
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
      if (nextCat != prevCat) {
        this.render(nextCat, prevCat);
        this.model.save('category', nextCat, { patch: true });
      }
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
      "change .market": "marketChange",
      "change .sub_market": "submarketChange",
      "change .hood": "hoodChange"
    },
    initialize: function() {
      _.bindAll(this, 'mapResize', 'changed', 'marketChange', 'submarketChange', 'hoodChange');
      this.geocoder = new google.maps.Geocoder();
      this.render();
      this.markets = $.parseJSON($("#market-data").html());
      this.initMarket();
      $('.edit-btn').on('shown.bs.tab', this.mapResize);
    },
    initMarket: function() {
      //Initialization and edit state
      this.$(".market").select2({
        placeholder: "Select a Market",
        data: this.markets.markets
      });
      this.$(".market").show();
      this.initSubmarket(this.model.get('market'));
    },
    initSubmarket: function(market) {
      if (this.markets[market]) {
        this.$(".sub_market").select2({
          placeholder: "Select a Sub-Market",
          val: "",
          data: this.markets[market]
        });
        this.$(".sub_market").show(); 
      } else {
        this.$(".sub_market").hide();
      }
      this.initHood(market, this.model.get('sub_market'));
    },
    initHood: function(market, subMarket) {
      if (this.markets[market] && this.markets[market][subMarket-1].hoods) {
        this.$(".hood").select2({
          placeholder: "Select a Sub-Market",
          val: "",
          data: this.markets[market][subMarket-1].hoods
        });
        this.$(".hood").show();
      } else {
        this.$(".hood").hide();
      }
    },
    marketChange: function(e) {
      this.initSubmarket(e.val);
      if (e.val)
        this.model.save('market', e.val, { patch: true });
    },
    submarketChange: function(e){
      var value = parseInt(e.val);
      this.initHood(this.model.get('market'), value);
      if (value)
        this.model.save('sub_market', value, { patch: true });      
    },
    hoodChange: function(e) {
      var value = parseInt(e.val);
      this.model.save('hood', value, { patch: true });
    },
    changed: function(e) {
      var input = $(e.currentTarget);
      this.model.save(input.attr('name'), input.val(), { patch: true });
    },

    render: function() {
      this.toggleLoading();
      this.model.get('location');
      if (location.length > 0) {
        this.geocode(location);
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
        this.mapError("Error: Old or non-compliant browser.");
      }
    },

    geocode: function(address) {
      var that = this;
      this.geocoder.geocode({'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
          var latlng = results[0].geometry.location;
          that.mapInit(latlng, 12);
          that.toggleLoading('geocode stop success');
        } else {
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
        url: 'https://freegeoip.net/json/' + REMOTE_ADDR,
        beforeSend: function(xhr, settings) {},
        success: function(response) {
          var latlng = new google.maps.LatLng(response.latitude, response.longitude);
          that.mapInit(latlng, 12);
          that.toggleLoading();
          // that.reverseGeocode(latlng);
        },
        error: function(jqXHR, textStatus, errorThrown) {
          console.log('freegeoip error');
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
      "change .description":  "descriptionChanged",
      "change #spec-row input": "specChanged"
    },
    initialize: function(options) {
      this.listenTo(this.model, 'change:category', this.switchCategory);
      _.bindAll(this, "descriptionChanged", "specChanged");
      this.defaults = $.parseJSON($('#initial-specs').html());
      this.switchCategory(this.model);
    },
    descriptionChanged: function(e) {
      var input = $(e.currentTarget);
      this.model.save(input.attr('name'), input.val(), { patch: true });
    },
    specChanged: function(e) {
      var input = $(e.currentTarget);
      var id = input.data('id')
      var spec = this.collection.get(id);
      if (input.val().length > 0) {
        spec.save('value', input.val());
      } else if (!spec.isNew()) {
        spec.destroy();
      }
    },
    switchCategory: function(model) {
      var that = this;
      var cat = model.get('category');
      var catName = $('.cat[data-id="{0}"]'.format(cat)).html(); // workaround
      var specNames = this.defaults[catName];
      var filteredSpecs = this.collection.filter(function(spec) {
        return spec.get('value').length > 0;
      });
      if (filteredSpecs) {
        this.collection.reset(filteredSpecs);
      }
      if (specNames) {
        var nextSpecs = _.map(specNames, function(name, index) {
          var existing = that.collection.findWhere({name: name });
          if (existing)
            return existing;
          else
            return new Spec({
              "name": name,
              "value": "",
              "listing": that.model.id
            });
        });
      }
      this.collection.add(nextSpecs, { merge: true });
      this.$('#spec-row').html(this.template({ 'specs': this.collection.toJSON() }));
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
      this.render(false);
      this.collection.on('add', function(photo) {
        photo.save();
      });
      // this.parseToCollection();
    },
    render: function(update) {
      if (this.collection.length > 0) {
        var context = { 'photos': this.collection.toJSON() };
        if (update) {
          var thumbnails = this.template(context);
          this.$('#photos').html(thumbnails);
        }
        this.bindSortable();
        this.$('.photo-view').fadeIn();
        this.$('.upload-view').hide();
      } else {
        this.$('.photo-view').hide();
        this.$('.upload-view').show();
      }
    },
    onSuccess: function(InkBlobs) {
      var that = this;
      var len = this.collection.length;
      var nextPhotos = _.map(InkBlobs, function(blob, index) {
        return new Photo({
          url: blob.url,
          key: blob.key,
          order: len + index,
          listing: that.model.id
        });
      });
      console.log(this.collection.toJSON());
      this.collection.set(nextPhotos, { merge: true });
      console.log(this.collection.toJSON());      
      this.render(true);
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
    // theres a beneign error that happens around here that we should fix
    updateOrder: function(e, ui) {
      var that = this;
      this.$('.sortable div').each(function(_index, item) {
        var id = $(item).data('id');
        that.collection.get(id).save('order', _index, { patch: true });
      });
    },
    bindSortable: function() {
      $('.sortable').sortable()
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
      if (this.listing.isValid() && this.specs.isValid() && this.photos.isValid()) {
        $.ajax({
          url: '/listing/' + this.listing.id.toString() + '/autopost',
          method: 'GET',
          success: function(data, status, xhr) {
            window.location.replace('/listings/dashboard/');
          },
          error: function(jqXHR, textStatus, errorThrown ) {
            console.log('error saving');
          }
        });
      }
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
    urlRoot: '/api/listings',
    validate: function(attrs, options) {
      var errors = {};

      // title
      errors.title = this.validateLength('title', attrs.title, 3, 100);
      errors.price = this.validateLength('price', attrs.price, 1, 8);      
      errors.category = this.validateExists('category', attrs.category);
      // errors.description = this.validateExists('description', attrs.description);
      errors.market = this.validateExists('market', attrs.market, 3, 100);
      errors.title = this.validateLength('title', attrs.title, 3, 100);

      var filteredErrors = {};
      _.each(errors, function(value, name) { if(value.length > 0) filteredErrors[name] = value; });
      if (!$.isEmptyObject(filteredErrors)) {
        return filteredErrors;
      }
    },
    validateExists: function(name, value) {
      if (!value) {
        return ["You should select a " + name + "."];
      } else {
        return [];
      }
    },
    validateLength: function(name, value, min, max) {
      if (value) {
        if (value.length > min && value.length < max) {
          return [];
        } else if(value.length <= min) {
          return ["Your " + name + " must be longer than" + min + "characters."];
        } else if (value.length >= max) {
          return ["Your " + name + " must be shorter than" + max + "characters."];
        };
      } else {
        return ["Don't forget to enter a " + name];
      };
    }
  });
  var Spec = Backbone.Model.extend({
    toJSON: function() {
      var json = Backbone.Model.prototype.toJSON.apply(this, arguments);
      if (!this.id && this.cid) {          
        json.id = this.cid;
      }
      return json;
    },
    validate: function(attrs, options) {} // no spec validation for now
  });
  var SpecList = Backbone.Collection.extend({
    model: Spec,
    url: '/api/specs',
    isValid: function() {
      return _.all(this.models, function(model) {
        return model.isValid();
      });
    }
  });

  var Photo = Backbone.Model.extend({
    toJSON: function() {
      var json = Backbone.Model.prototype.toJSON.apply(this, arguments);
      if (!this.id && this.cid) {
        json.id = this.cid;
      }
      return json;
    }, 
    validation: function(attrs, options) {} // no validation for now.
  });

  var PhotoList = Backbone.Collection.extend({
    model: Photo,
    url: '/api/photos',
    comparator: 'order',
    isValid: function() {
      return _.all(this.models, function(model) {
        return model.isValid();
      });
    }
  });

  var specsJSON = listingJSON.spec_set;
  var photosJSON = listingJSON.listingphoto_set;

  // prune json.. we should probably modify the serializer so we don't have to do this
  delete listingJSON.spec_set;
  delete listingJSON.listingphoto_set;  
  delete listingJSON.user;

  var listing = new Listing(listingJSON);
  var specs = new SpecList(specsJSON);
  var photos = new PhotoList(photosJSON);

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
  });

  var previewView = new PreviewView({ listing: listing, specs: specs, photos: photos });

  var specEditView = new SpecEditView({ collection: specs, model: listing  });
  var photoEditView = new PhotoEditView({ collection: photos, model: listing });
  var listingEditView = new ListingEditView({ model: listing });

  var SidebarView = Backbone.View.extend({
    el: '.detail-sidebar',
    events: {
      // "click .draft-btn": "save",
      // "click .save-btn": "publish"
    },
    initialize: function() {
      this.listenTo(listing, 'request', this.showSaving);
      this.listenTo(listing, 'sync', this.hideSaving);
      this.listenTo(listing, 'error', this.errorSaving);

      this.listenTo(specs, 'request', this.showSaving);
      this.listenTo(specs, 'sync', this.hideSaving);
      this.listenTo(listing, 'error', this.errorSaving);

      this.listenTo(photos, 'request', this.showSaving);
      this.listenTo(photos, 'sync', this.hideSaving);
      this.listenTo(listing, 'error', this.errorSaving);      
    },
    showSaving: function(event) {
      $('#error-saving').hide();      
      $('#loading').show();
    },
    hideSaving: function(event) {
      $('#error-saving').hide();
      $('#loading').hide();
    },
    errorSaving: function(event) {
      $('#loading').hide();      
      $('#error-saving').show();
    },
    // save: function(e) {
    //   $('#submit-draft').click();
    // },
  });
  var sidebarView = new SidebarView;
});
