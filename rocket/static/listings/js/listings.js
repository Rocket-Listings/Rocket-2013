// enable formatting strings
if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) { 
      return typeof args[number] != 'undefined' ? args[number] : match;
    });
  };
}

$(function() {

  function selectCategory(next_id, prev_id) {
    if (prev_id)
      $('.tab-pane .cat[data-id="{0}"]'.format(prev_id)).removeClass('selected');
      $('table tr[data-cat="{0}"]'.format(prev_id)).hide();

    var cat = $('.tab-pane .cat[data-id="{0}"]'.format(next_id));
    cat.addClass('selected');

    // switch to tab
    $('.nav-tabs a[href="#{0}"]'.format(cat.parent('.tab-pane').attr('id'))).tab('show');
    var a = $('.specs-table tr[data-cat="{0}"]'.format(next_id));
    console.log(a);
    a.show();
  }
  // set initial/current value
  selectCategory($('#id_category').val());

  // Listing form category selection 
  $('.tab-pane .cat').click(function(e) {
    t = $(this);
    var catInput = $('#id_category');
    var id = t.data('id');
    if (catInput.val()) // if cat input is set
      selectCategory(id, catInput.val())
    else
      selectCategory(id)
    catInput.val(id);
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


  /* Listing Offers */
  // $('.table-offers').tablesorter({ cssHeader: 'table-header'});

  // $('.content').hide();
  // $('.bottom').hide();
  
  // var firstId = $('.buyer-tiles:first').data('buyerid');
  // $('.buyer-tiles[data-buyerid="'+firstId+'"]').click();
  // $('.content[data-buyerid="'+firstId+'"]').show();
  // $('.bottom[data-buyerid="'+firstId+'"]').show();

  // $('.buyer-tiles').click(function(){
  //   var buyerid = $(event.target).data('buyerid');
  //   $('.content').hide();
  //   $('.content[data-buyerid="'+buyerid+'"]').show();
  //   $('.bottom').hide();
  //   $('.bottom[data-buyerid="'+buyerid+'"]').show();
  // });

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

  $(".edit_button").click(switchPane);
  $(".preview_button").click(switchPane);


  function switchPane(e) {
    console.log($(e.target) == $('.edit_button').first());
  }

  // function handleEditClick(e) {
  //   $(".edit").show();
  //   $(".preview-pane").hide();
  // }


  // function handlePreviewClick(e) {
  //   $(".edit").hide();
  //   $(".preview-pane").show();
  //   $('.l-description').text($('#id_description').val());
  //   $('.title').text($('#id_title').val());
  //   $('.l-location').text("(" + $('#id_location').val() + ")");
  //   $('.l-price').text("$" + $('#id_price').val());
  //   var category = $(".hidden > select option:selected").html();
  //   var base_category = $("li.active").text().toLowerCase().trim();
  //   $(".l-category").text(base_category + " > " + category);

  //   $('.category_' + prev, ".preview-pane").hide();

  //   if (is_housing == 1){
  //     $(".preview-pane .category_" + val +":eq(0)").show();
  //     var specs = $('.table_' + val + ':eq(0) input').length;

  //     for (var i=0;i<specs;i++){
  //       var spec_value = $('.table_' + val + ':eq(0) input:eq('+i+')').val();
  //       $('.table_preview_' + val + ':eq(0) input:eq('+i+')').val(spec_value);
  //     }
  //   }
  //   else if (is_housing == 2) {
  //     $(".preview-pane .category_" + val +":eq(1)").show();
  //     var specs = $('.table_' + val + ':eq(1) input').length;

  //     for (var i=0;i<specs;i++){
  //       var spec_value = $('.table_' + val + ':eq(1) input:eq('+i+')').val();
  //       $('.table_preview_' + val + ':eq(1) input:eq('+i+')').val(spec_value);
  //     }
  //   }
  //   else {
  //     $('.category_' + val, ".preview-pane").show();
  //     var specs = $('.table_' + val + ' input').length;

  //     for (var i=0;i<specs;i++){
  //       var spec_value = $('.table_' + val + ' input:eq('+i+')').val();
  //       $('.table_preview_' + val + ' input:eq('+i+')').val(spec_value);
  //     }
  //   }
});