// enable formatting strings
if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) { 
      return typeof args[number] != 'undefined' ? args[number] : match;
    });
  };
}

// serialize for backbone
$.fn.serializeObject = function()
{
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
      console.log('changed');
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
    next_specs.find('input').removeAttr('disabled');
    next_specs.show();
  }
  // set initial/current value
  selectCategory($('#id_category').val());
  $('.tab-pane .cat').click(function(e) {
    selectCategory($(this).data('id'))
  });


  /* Listings table */
  $('.table-listings').tablesorter({ cssHeader: 'table-header'});
  $('.table-listings').tooltip({ selector: "a[data-toggle=tooltip]" });


  /* Listing detail photo slideshow */
  var photoId = parseInt((window.location.hash || "").substring(1));
  if(photoId) {
    if($($('.l-thumbnails img')[photoId]).attr('data-id') == photoId) {
      fillStage($($('.l-thumbnails img')[photoId]));
    } else {
      $('.l-thumbnails img').each(function(index, element) {
        if($(element).attr('data-id') == photoId){
          fillStage($(element));
          return false; // break iteration
        }
      });
    }
  }

  $('.l-thumbnails img').click(function(event){
    fillStage($(event.target));
  });

  function fillStage(image) {
    $(".l-stage img").attr('src', image.attr('data-full'));
    id = image.attr('data-id');
    window.location.hash = image.attr('data-id');
  }

  var cl_embed = $('.cl-embed');
  if(cl_embed) {
    cl_embed.click(function(e) {
      cl_embed.select();
    });
  }

  function fileUpload(){
  /* function needs more work inorder to better save photos in s3 */
    filepicker.pickAndStore({
      services: ['COMPUTER','URL'],
      mimetype:"image/*",
      multiple: "true"
      },
      {location:"S3"},
    function(InkBlobs){
      var filepickerObject = InkBlobs;
      photoLog(filepickerObject); /* Logs photos for storing in database */
      editImage(filepickerObject); /* Preview images on edit page */
      }
    );
  }
});