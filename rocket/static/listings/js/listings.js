if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) { 
      return typeof args[number] != 'undefined' ? args[number] : match;
    });
  };
}

// serialize for backbone
$.fn.serializeObject = function() {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

$(function() {

  // Backbone listing preview stuff
  var Listing = Backbone.Model.extend({
    initialize: function() {}
  });

  var ListingView = Backbone.View.extend({

    el: '#listing-detail',
    template: Mustache.compile($('#preview-template').html()),
    events: {
      "change input":  "changed",
      "change textarea":  "changed",
      "change select": "changed"
    },

    initialize: function() {
      this.model = new Listing(this.$('.listing-form:first').serializeObject());
      this.render();
      _.bindAll(this, 'changed', 'render');
    },

    changed: function(evt) {
      var changed = $(evt.currentTarget)
      var obj = {};
      obj[changed.attr('name')] = changed.val();
      this.model.set(obj);
      this.render();
    },

    render: function() {
      this.$('#preview-view').html(this.template(this.model.toJSON()));
    }
  });
  var ListingView = new ListingView;

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
      var thumbnail = Mustache.render($('#thumbnail-template').html(), view);
      $('#photos').append(thumbnail);
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
        formset.find('#id_listingphoto_set-{0}-order'.format(photo.index)).val(photo.index);               
      });

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
        $('.sortable li').each(function(index, item) {
          var id = $(item).data('id');
          formset.find('#id_listingphoto_set-{0}-order'.format(id)).val(index);
        });
      });
    }
  }
  // Make drag and drop photo upload pane
  // $('#dragdrop').click(function(e) {
    // e.preventDefault();
  filepicker.pickAndStore(fpConfig.picker_options, fpConfig.store_options, $.proxy(fpConfig.onSuccess, fpConfig), fpConfig.onError);
  $('.toggle-view').click(fpConfig.toggleView);
  fpConfig.bindSortable();
  // });
  // filepicker.makeDropPane($('#dragdrop'), $.extend({
  //   onSuccess: fpConfig.onSuccess,
  //   onError: fpConfig.onError,
  //   onProgress: fpConfig.onProgress,
  //   dragEnter: fpConfig.dragEnter,
  //   dragLeave: fpConfig.dragLeave
  // }, fpConfig.picker_options, fpConfig.store_options));

  /* Listings table */
  $('.table-listings').tablesorter({ cssHeader: 'table-header'});


  /* Listing detail photo slideshow */
  // var photoId = parseInt((window.location.hash || "").substring(1));
  // if(photoId) {
  //   if($($('.l-thumbnails img')[photoId]).attr('data-id') == photoId) {
  //     fillStage($($('.l-thumbnails img')[photoId]));
  //   } else {
  //     $('.l-thumbnails img').each(function(index, element) {
  //       if($(element).attr('data-id') == photoId){
  //         fillStage($(element));
  //         return false; // break iteration
  //       }
  //     });
  //   }
  // }

  // $('.l-thumbnails img').click(function(event){
  //   fillStage($(event.target));
  // });

  // function fillStage(image) {
  //   $(".l-stage img").attr('src', image.attr('data-full'));
  //   id = image.attr('data-id');
  //   window.location.hash = image.attr('data-id');
  // }
});