var SidebarView = Backbone.View.extend({
  el: '.detail-sidebar',
  events: {
    // "click .draft-btn": "save",
    // "click .save-btn": "publish"
  },
  initialize: function(options) {
    this.listing = options.listing;
    this.specs = options.specs;
    this.photos = options.photos;

    this.listenTo(options.listing, 'request', this.showSaving);
    this.listenTo(options.listing, 'sync', this.hideSaving);
    this.listenTo(options.listing, 'error', this.errorSaving);

    this.listenTo(options.specs, 'request', this.showSaving);
    this.listenTo(options.specs, 'sync', this.hideSaving);
    this.listenTo(options.specs, 'error', this.errorSaving);

    this.listenTo(options.photos, 'request', this.showSaving);
    this.listenTo(options.photos, 'sync', this.hideSaving);
    this.listenTo(options.photos, 'error', this.errorSaving);      

    _.bindAll(this, 'publish');
    $('.publish-btn').click(this.publish);
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
  publish: function(e) {
    $('.publish-btn').prop('disabled', true);
    console.log("listing valid:", this.listing.isValid());
    console.log("specs valid: ", this.specs.isValid());
    console.log("photos valid: ", this.photos.isValid());            
    if (this.listing.isValid() && this.specs.isValid() && this.photos.isValid()) {
      $.ajax({
        url: '/listings/' + this.listing.id.toString() + '/hermes',
        method: 'GET',
        success: function(data, status, xhr) {
          console.log(xhr.status);
          // if (xhr.status == 200) {
          //   window.location.replace('/listings/dashboard/');
          //   console.log(data);
          //   window.postMessage({type: "FROM_PAGE", action: "post", ctx: data}, "*");
          // } else if(xhr.status == 403) {
          //   $('#not-enough-credits').show();
          // }
        },
        error: function(jqXHR, textStatus, errorThrown ) {
          console.log(jqXHR.status);
          console.log('error saving');
        }
      });
    } else {
      this.errorSaving();
    }
  }
  // save: function(e) {
  //   $('#submit-draft').click();
  // },
});

var ListingEditView = Backbone.View.extend({
  el: '#info-fieldset',
  events: {
    // "change input": "changed",
    "keyup .title":   "renderPageTitle",
    "blur .title":  "changed",
    "blur .price":  "changed",
  },
  initialize: function(options) {
    this.categoryEditView = new CategoryEditView(options);
    this.locationEditView = new LocationEditView(options);
    // can't set this listener in the events property since .description is outside the #info-fieldset
    _.bindAll(this, 'changed');
    $('.description').on('blur', this.changed);
    this.listenTo(this.model, 'invalid', this.validationError);
  },
  validationError: function(model, errors) {
    _.each(errors, function(error) {
      switch(error.field) {
        case "category":
          var elem = $('#category-error');
          elem.html(error.message);
          elem.parent().show();
          break;
        case "title":
          var elem = $('#title-error');
          elem.html(error.message);
          elem.parent().addClass('has-error');
          break;
        case "price":
          var elem = $('#price-error');
          elem.html(error.message);
          elem.parent().addClass('has-error'); 
          break;
        case "description":
          var elem = $('#description-error');
          elem.html(error.message);
          elem.parent().addClass('has-error');        
          break;
        case "location":
          var elem = $('#location-error');
          elem.html(error.message);
          elem.parent().addClass('has-error'); 
      }
    });
  },
  changed: function(e) {
    var input = $(e.currentTarget);
    this.model.save(input.attr('name'), input.val(), {patch: true, validate: false});
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
      this.model.save('category', nextCat, { patch: true, validate: false });
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
    this.markets = $.parseJSON($("#market-data").html());
    this.initMarket();
    this.render();
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
      this.model.save({'sub_market': null, 'market':market}, { patch: true, validate: false });
      this.$(".sub_market").hide();
    }
    this.initHood(market, this.model.get('sub_market'));
  },
  initHood: function(market, subMarket) {
    if (this.markets[market] && subMarket && this.markets[market][subMarket-1].hoods) {
      this.$(".hood").select2({
        placeholder: "Select a Sub-Market",
        val: "",
        data: this.markets[market][subMarket-1].hoods
      });
      this.$(".hood").show();
      this.$('#id_location').val('');
      this.$('#id_location').prop('disabled', true);
    } else {
      this.model.save({'sub_market': subMarket, 'market':market, 'hood': null}, { patch: true, validate: false });
      this.$('#id_location').prop('disabled', false);
      this.$(".hood").hide();
    }
  },
  marketChange: function(e) {
    this.initSubmarket(e.val);
    this.model.save('market', e.val, { patch: true, validate: false });
    this.render();
  },
  submarketChange: function(e){
    var value = parseInt(e.val);
    console.log(value);
    this.initHood(this.model.get('market'), value);
    // if (value)
    this.model.save('sub_market', value, { patch: true, validate: false });      
    this.render();      
  },
  hoodChange: function(e) {
    var value = parseInt(e.val);
    this.model.save('hood', value, { patch: true, validate: false });
    this.render();      
  },
  changed: function(e) {
    var input = $(e.currentTarget);
    this.model.save(input.attr('name'), input.val(), { patch: true, validate: false });
    this.render();
  },

  render: function() {
    this.startLoad('render');

    var location = this.model.get('location');
    var market = this.model.get('market');
    var sub = this.model.get('sub_market');
    var hood = this.model.get('hood');
    var marketName, subName, hoodName;

    // hella inefficient
    if (market) {
      marketName = _.findWhere(this.markets.markets, { id: market }).text; 
      // console.log(sub);
      if (sub) {
        subName = _.findWhere(this.markets[market], { id: sub.toString() }).text + ', ' + marketName;
        // console.log(hood);
        if (hood) {
          hoodName = _.findWhere(this.markets[market][sub-1].hoods, { id: hood.toString() }).text + ', ' + subName;
        }
      }
    }

    var mapFocus = location || hoodName || subName || marketName;
    if (mapFocus) {
      this.geocode(mapFocus);
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
  startLoad: function(str) {
    // console.log("startLoad: " + str);
    this.$('.loading-spinner').show();
  },
  stopLoad: function(str) {
    // console.log("stopLoad: " + str);
    this.$('.loading-spinner').hide();
  },

  getLocationByBrowser: function(e) {
    this.startLoad('getLocationByBrowser');
    var that = this;
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        var lat = position.coords.latitude;
        var lng = position.coords.longitude;
        var latlng = new google.maps.LatLng(lat, lng);
        that.mapInit(latlng, 14);
        that.stopLoad('getLoctationByBrowser');
        that.reverseGeocode(latlng);
      }, that.mapError, { enableHighAccuracy: true });
    } else {
      this.mapError("Old or non-compliant browser.");
    }
  },

  geocode: function(address) {
    var that = this;
    this.geocoder.geocode({'address': address}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        var latlng = results[0].geometry.location;
        that.mapInit(latlng, 14);
        that.stopLoad('geocode');
      } else {
        that.mapError('Geocode was not successful because ' + status);
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
        that.mapError('Geocoder failed due to ' + status);
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
        that.stopLoad('getLocationByIP');
        // that.reverseGeocode(latlng);
      },
      error: function(jqXHR, textStatus, errorThrown) {
        that.mapError('freegeoip');
      }
    });      
  },
  mapError: function(error) {
    this.stopLoad("Maps error:" + error);
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
    "blur #spec-row input": "specChanged"
  },
  initialize: function(options) {
    this.listenTo(options.listing, 'change:category', this.switchCategory);
    _.bindAll(this, "specChanged");
    this.defaults = $.parseJSON($('#initial-specs').html());
    this.switchCategory(options.listing, options.listing.get('category'),{ initialLoad: true });
  },
  specChanged: function(e) {
    // this is run every time a spec field is blurred (loses focus)
    var input = $(e.currentTarget);
    var id = input.data('cid');
    var spec = this.collection.get(id);
    var saveResult = spec.save('value', input.val());
    if (!saveResult && !spec.isNew()) {
      // We don't want to destroy it, since we want it to stay in the dom
      spec.sync('delete', spec);
      spec.unset('id');
    }
  },
  validationError: function(model, error, options) {
    if(error.fatal) {
      $('#id_spec-{0}'.format(model.cid)).parent().addClass('has-error');
    }
  },
  saved: function(model, resp, options) {
    $('#id_spec-{0}'.format(model.cid)).parent().removeClass('has-error');
  },
  switchCategory: function(model, value, options) {
    if (!options || !options.initialLoad) {
      // clear collection of specs if were not setting up shop
      this.collection.invoke('destroy');
    }
    var categoryName = $('.cat[data-id="{0}"]'.format(value)).html(); // TODO; workaround
    var specObjects = this.defaults[categoryName];
    if (specObjects) {
      var nextSpecs = _.map(specObjects, function(specObject) {
          var newSpec = new Spec({
            "name": specObject.name,
            "value": "",
            "listing": model.id,
            "required": specObject.required || false
          });
          this.listenTo(newSpec, 'invalid', this.validationError);
          this.listenTo(newSpec, 'sync', this.saved);
          return newSpec;
      // run this map function in the same context as the switchCategory function
      }, this);
    }
    this.collection.set(nextSpecs);
    var markup = this.template({
      'specs': this.collection.toJSON()
    });
    this.$('#spec-row').html(markup);
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
    this.collection.set(nextPhotos, { merge: true });
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
  fillStage: function(e) {
    e.preventDefault();
    var photo = $(e.currentTarget);
    var src = photo.attr('data-full') || photo.attr('src');
    this.$(".preview-stage img").attr('src', src);
    window.location.hash = photo.attr('data-id');
    return this;
  }
});
