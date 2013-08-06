$(function() {
  
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
        this.$('.listing-title').text("Create a listing");
        // not sure why this.$('#preview-btn') is not found here. Using global selector.
        $('#preview-btn').attr('disabled', 'disabled');
      }
      return this;
    }
  });
  var listingView = new ListingView;


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

  $("div.btn-group[data-toggle-name='listing-pane-toggle'] a").click(function() {
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