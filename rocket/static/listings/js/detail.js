$(function() {

  //Market Select Stuff
  var dat = $.parseJSON($("#market-data").html());

  $(".form-select").select2({
    placeholder: "Select a Market",
    data: dat.markets
  });
  $(".form-select").show();

  $(".form-select").on("change", function(e){

    if (dat[e.val]) {
      $(".form-select-sub").select2({
        placeholder: "Select a Sub-Market",
        data: dat[e.val]
      });
      $(".form-select-sub").show();
    }
    else{
      $(".form-select-sub").hide();
    }
  });


  
  // Category Selection Stuff
  function selectCategory(next_id) {
    var cat_input = $('#id_category');
    var prev_id = cat_input.val();
    cat_input.val(next_id);

    if (prev_id) {
      $('.tab-pane .cat[data-id="{0}"]'.format(prev_id)).removeClass('selected');
      var prev_specs = $('.specs-form > div[data-cat="{0}"]'.format(prev_id));
      prev_specs.hide();
      prev_specs.find('input').attr('disabled', 'disabled');
    }

    var cat = $('.tab-pane .cat[data-id="{0}"]'.format(next_id));
    cat.addClass('selected');

    // switch to tab
    $('.nav-tabs a[href="#{0}"]'.format(cat.parent('.tab-pane').attr('id'))).tab('show');

    var next_specs = $('.specs-form > div[data-cat="{0}"]'.format(next_id));
    if (next_specs.length) {
      next_specs.find('input').removeAttr('disabled');
      next_specs.show();
      $('#no-specs').hide();
    } else {
      $('#no-specs').show();
    }
  }

  // set initial/current category value
  selectCategory($('#id_category').val());
  $('.tab-pane .cat').click(function(e) {
    selectCategory($(this).data('id'))
  });

  var Photo = Backbone.Model.extend({});
  var Listing = Backbone.Model.extend({});
  var Spec = Backbone.Model.extend({});  

  var SpecList = Backbone.Collection.extend({
    model: Spec
  });
  var PhotoList = Backbone.Collection.extend({
    model: Photo,
    comparator: 'order'
  });

  var LocationEditView = Backbone.View.extend({
    el: '#location-col',
    events: {
      "change #id_location": "render",
      "click #location-btn": "getLocationByBrowser",
    },

    initialize: function() {
      _.bindAll(this, 'mapResize');
      this.geocoder = new google.maps.Geocoder();
      this.render();

      $('.edit-btn').on('shown.bs.tab', this.mapResize);
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
          disableDoubleClickZoom: true
        };
        this.map = new google.maps.Map(document.getElementById("location-map"), mapOptions);
      }
    },

    mapResize: function(e) {
      google.maps.event.trigger(this.map, 'resize');
    },

    toggleLoading: function() {
      this.$('.loading-spinner').toggle();
    },

    getLocationByBrowser: function(e) {
      this.toggleLoading();
      var that = this;
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
          var lat = position.coords.latitude;
          var lng = position.coords.longitude;
          var latlng = new google.maps.LatLng(lat, lng);
          that.mapInit(latlng, 14);
          that.toggleLoading();
          that.reverseGeocode(latlng);
        }, that.mapError, { enableHighAccuracy: true });
      } else {
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
          that.toggleLoading();
        } else {
          that.toggleLoading();
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
            }
          });
        }
      });
    },

    mapError: function(error) { 
      // this.toggleLoading();
      console.log("Maps error");
      console.log(error);
    }
  });

  var SidebarView = Backbone.View.extend({
    el: '.detail-sidebar',
    events: {
      // "click .draft-btn": "save",
      "click .save-btn": "publish"
    },

    // save: function(e) {
    //   $('#submit-draft').click();
    // },
    publish: function(e) {
      $('#submit-publish').click();
    }
  });
  
  var sidebarView = new SidebarView;
  var PhotoListView = Backbone.View.extend({
    // el is defined in template with the backbone.subview plugin
    el: '#preview-gallery', 
    template: Mustache.compile($('#preview-gallery-template').html()),
    events: {
      "click .preview-thumbnails img": "fillStage"
    },

    initialize: function() {
      _.bindAll(this, 'fillStage', 'load');
      this.photos = new PhotoList;
      this.load();
    },

    render: function() {
      var context = {
        "photos": this.photos.toJSON(),
      };
      if (this.photos.length > 0) {
        context["first_photo"] = this.photos.at(0).toJSON();
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
    },

    load: function() {      
      var formObject = $('.listing-form:first').serializeObject();
      var total = formObject['listingphoto_set-TOTAL_FORMS'];
      var photolist = [];
      for (var i = 0; i < total; i++) {
        var key = 'listingphoto_set-{0}-'.format(i);
        photolist.push(new Photo({
          url: formObject[key + 'url'],
          key: formObject[key + 'key'],
          listing: formObject[key + 'listing'],
          order: formObject[key + 'ORDER'],
          markedDelete: formObject[key + 'DELETE'] || false
        }));
      }
      this.photos.set(photolist); // {merge: true});
      return this;
    }
  });

  var SpecListView = Backbone.View.extend({
    el: '#preview-specs',
    template: Mustache.compile($('#preview-specs-template').html()),
    initialize: function(e) {
      _.bindAll(this, 'load');
      this.specs = new SpecList;
      this.load();
    },

    render: function() {
      var context = {
        "specs": this.specs.toJSON(),
        "has_specs": this.specs.length > 0
      }
      this.$el.html(this.template(context));
    },

    load: function() {
      var inputs = _.filter($('.specs-form input:enabled'), function(input) {
        return $(input).val().length > 0;
      });
      var specs = _.map(inputs, function(input) {
        return new Spec({
          key: $(input).siblings('label').text(),
          value: $(input).val()
        });
      });
      this.specs.set(specs);
    }
  });

  var ListingView = Backbone.View.extend({
    el: '#listing-detail',
    template: Mustache.compile($('#preview-text-template').html()),
    events: {
      // "change input": "changed",
      "keyup .title":         "changed",      
      "change .price":        "changed",
      "change .description":  "changed",
      "change .location":     "changed",
      "change .specs-form input:enabled": "specChanged",
      "change #photo_formset input": "photoChanged",
    },

    initialize: function() {
      _.bindAll(this, 'changed', 'specChanged', 'photoChanged');
      Backbone.Subviews.add(this);
      this.on('photoChanged', this.photoChanged, this);

      var form = this.$('.listing-form:first').serializeObject();
      var listing = {
        "title": form.title,
        "category": form.category,       
        "price": form.price,
        "description": form.description,
        "location": form.location
      }
      this.model = new Listing(listing);
      // this.photoView = new PhotoListView;
      this.render();
    },

    subviewCreators : {
      "photoView": function() {
          var options = {};
          return new PhotoListView(options);
      },
      "specView": function() {
        var options = {};
        return new SpecListView(options);
      }
    },

    changed: function(e) {
      // this.photos.changed();
      var changed = $(e.currentTarget);

      var obj = {};
      obj[changed.attr('name')] = changed.val();
      this.model.set(obj);
      this.render();
    },

    specChanged: function(e) {
      this.subviews.specView.load();
      this.subviews.specView.render();
    },

    photoChanged: function(e) {
      this.subviews.photoView.load();
      this.subviews.photoView.render();      
    },

    render: function() {
      var context = { 
        "listing": this.model.toJSON(),
      };
      this.$('#preview-view').html(this.template(context));

      if (this.model.get('title').length > 0) {
        this.$('.listing-title').text(this.model.get('title'));
        $('#preview-btn').removeAttr('disabled');
      } else {
        this.$('.listing-title').html("Create a listing");
        // not sure why this.$('#preview-btn') is not found here. Using global selector.
        $('#preview-btn').attr('disabled', 'disabled');
      }
      return this;
    }
  });
  var listingView = new ListingView;
  var locationEditView = new LocationEditView;

  // file picker options and callbacks
  var fpConfig = {
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
    onSuccess: function(InkBlobs) {
      // update management form
      var totalForms = parseInt($('#id_listingphoto_set-TOTAL_FORMS').val());
      var initialForms = parseInt($('#id_listingphoto_set-INITIAL_FORMS').val());
      $('#id_listingphoto_set-TOTAL_FORMS').val(totalForms + InkBlobs.length);

      // prepare view context variables
      var view = { photos: [] };
      $.each(InkBlobs, function(index, blob) {
        view.photos.push({
          index: initialForms + index,
          url: blob.url,
          key: blob.key,
          src: "https://s3.amazonaws.com/static.rocketlistings.com/" + blob.key
        });
      });

      // user interface first
      var thumbnails = Mustache.render($('#thumbnail-template').html(), view);
      $('#photos').append(thumbnails);
      this.bindSortable();
      $('.photo-view').fadeIn();
      $('.upload-view').hide();

      // then formset stuff
      var photoFormTemplate = $('#photo-form-template').html().replace(/__prefix__/g, "{{ index }}");
      var photoForm = Mustache.render(photoFormTemplate, view);
      var formset = $('#photo_formset');
      formset.append(photoForm);

      // manual labor to insert values
      $.each(view.photos, function(index, photo) {
        formset.find('#id_listingphoto_set-{0}-url'.format(photo.index)).val(photo.url);
        formset.find('#id_listingphoto_set-{0}-key'.format(photo.index)).val(photo.key);
        formset.find('#id_listingphoto_set-{0}-ORDER'.format(photo.index)).val(photo.index);               
      });

      listingView.trigger('photoChanged');
    },
    onError: function(type, message) {
      console.log('('+type+') '+ message);
    },
    toggleView: function(e) {
      if (e)
        e.preventDefault();

      $('.upload-view').toggle();
      $('.photo-view').toggle();      
    },
    bindSortable: function() {
      $('.sortable').sortable().bind('sortupdate', function() {
        var formset = $('#photo_formset');
        $('.sortable div').each(function(index, item) {
          var id = $(item).data('id');
          var orderInput = formset.find('#id_listingphoto_set-{0}-ORDER'.format(id));
          orderInput.val(index);
          listingView.trigger('photoChanged');
        });
      });
    }
  }

  filepicker.setKey('ATM8Oz2TyCtiJiHu6pP6Qz');
  filepicker.pickAndStore(fpConfig.picker_options, fpConfig.store_options, $.proxy(fpConfig.onSuccess, fpConfig), fpConfig.onError);
  $('.toggle-view').click(fpConfig.toggleView);
  fpConfig.bindSortable();

  $("div.btn-group[data-toggle-name='listing-pane-toggle'] a").click(function(e) {
    $(this).siblings().removeClass("active");
    $(this).addClass("active");
  });

/*  $('.preview-thumbnails img').on('click', function(e){
    fillStage($(e.currentTarget));
  });

  function fillStage(photo) {
    var src = photo.attr('data-full') || photo.attr('src');
    $(".preview-stage img").attr('src', src);
    window.location.hash = photo.attr('data-id');
  } */

  /* Listings table */
  // $('.listings-table').tablesorter({ cssHeader: 'table-header'});
});