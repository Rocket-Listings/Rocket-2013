$(function() {
  /* Listing detail photo slideshow */
  // var photoId = parseInt((window.location.hash || "").substring(1));
  // if(photoId) {
  //   var photo = $('.l-thumbnails img:nth-child({0})'.format(photoId));
  //   if(photo.attr('data-id') == photoId) {
  //     fillStage(photo);
  //   } else {}
  // }
  window.ondragstart = function() { return false; } 
  
  $('.preview-thumbnails img').click(function(e){
    fillStage($(e.currentTarget));
  });

  function fillStage(photo) {
    var src = photo.attr('data-full') || photo.attr('src');
    $(".preview-stage img").attr('src', src);
    window.location.hash = photo.attr('data-id');
  }
});