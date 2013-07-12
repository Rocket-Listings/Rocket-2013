$(function() {
  /* Listing Form */
  $('.tab-pane .cat').click(function(e) {
    e = $(this);
    var cat = $('#category-input');
    if (cat.val()) // if cat input is set
      $('.tab-pane .cat#cat-' + cat.val()).removeClass('selected');
    e.addClass('selected');
    cat.val(e.html());
  });


  /* Listings table */
  $('.table-listings').tablesorter({ cssHeader: 'table-header'});
  $('.table-listings').tooltip({ selector: "a[data-toggle=tooltip]" });

  /***
  okay. So trusted domains refers to the host domain(s) not the CDN (AKA aws s3)
  see: https://github.com/jonrohan/ZeroClipboard/issues/116.
  Also scripted access is not neccesary for out version of Zeroclipboard (1.1.6)
  b/c its default value is 'always'.
  ***/
  /* ZeroClipboard.setDefaults({
    moviePath: STATIC_URL +'js/ZeroClipboard.swf', 
    trustedDomains: [   
      'beta.rocketlistings.com', 
      'rocketlistings.com', 
      'www.rocketlistings.com', 
      'rocket-listings.herokuapp.com',
      'quiet-beyond-7797.herokuapp.com'
    ]
  });
  var clip = new ZeroClipboard( $(".clipboard") )
  clip.on( 'mousedown', function(client){ $(this).addClass("active"); })
  clip.on( 'mouseup', function(client){ $(this).removeClass("active"); }); */

  /* Listing Detail */
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

  $('.table-offers').tablesorter({ cssHeader: 'table-header'});

  $('.content').hide();
  $('.bottom').hide();
  
  var firstId = $('.buyer-tiles:first').data('buyerid');
  $('.buyer-tiles[data-buyerid="'+firstId+'"]').click();
  $('.content[data-buyerid="'+firstId+'"]').show();
  $('.bottom[data-buyerid="'+firstId+'"]').show();

  $('.buyer-tiles').click(function(){
    var buyerid = $(event.target).data('buyerid');
    $('.content').hide();
    $('.content[data-buyerid="'+buyerid+'"]').show();
    $('.bottom').hide();
    $('.bottom[data-buyerid="'+buyerid+'"]').show();
  });
});
