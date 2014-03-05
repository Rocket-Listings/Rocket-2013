// Context for keyboard controls
var context = "l";

// Globally declare List listings for access outside bindEvents() scope
var listings;
var searchHasFocus;
var currentFilterButton = $("#filter-not-deleted");

(function() {
  // Utils
  // Scroll messages to bottom
  $.fn.scrollBottom = function() {
    $(this).scrollTop($(this)[0].scrollHeight);
  }
  $.fn.exists = function () {
    return this.length !== 0;
  }
  // Convert links in messages to anchors
  function linkToClickable(text) {
    var exp = /((([A-Za-z]{3,9}:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]+|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w-_]*)?\??(?:[-\+=&;%@.\w_]*)#?(?:[\w]*))?)/gi;
    return text.replace(exp, "<a href='$1'>$1</a>"); 
  }

  // Bind clicks and list init to the current items
  function bindEvents() {
    $('.listing').click(function () {
      var listingRow = $(this);
      var id = listingRow.data('listing-id'),
      var buyers = $(".buyer[data-listing-id='" + id + "']");
      $('.listing').removeClass('highlight');
      $('.d-arrow').addClass('hide');
      listingRow.addClass('highlight');
      $(".message, .buyer").addClass("hide");
      $(".dashboard-delete-btn").attr('data-listing-id', id).removeClass("disabled");
      if (listingRow.hasClass("deleted")) {
        $(".dashboard-delete-permanent-btn").attr('data-listing-id', id).removeClass("disabled");
      }
      if (buyers.length) {
        $('.d-arrow', this).removeClass('hide');
        $(".dashboard-buyers-body").addClass("border-right").removeClass("hide");
        $(".dashboard-empty-inbox").addClass("hide");
        buyers.removeClass("hide");
        buyers.first().click();
        $('.dashboard-dashboard-dashboard-dashboard-message-form-wrapper').removeClass("hide");
        $('.dashboard-messages-body').removeClass("hide").scrollBottom();
      } else {
        $('.dashboard-dashboard-dashboard-dashboard-message-form-wrapper').addClass("hide");
        $(".dashboard-buyers-body").removeClass("border-right").addClass("hide");
        $(".dashboard-messages-body").addClass("hide");
        $(".dashboard-empty-inbox").removeClass("hide");
      }
    });

    // Initialize the listings globally for List.js
    var options = {
      valueNames: ['id', 'title', 'price', 'category', 'date', 'status']
    };

    if (window.listings) {
      window.listings.filter();
    }

    window.listings = new List('dashboard', options);
    window.currentFilterButton.click();
  }

  // Unbind click events from current items
  function unbindEvents() {
    $('.listing, .buyer').unbind('click');
  }

  // Autopost from dashboard (not used here)
  // $(".share_optn").click(function (e) {
  //   e.preventDefault();
  //   if (!$(this).hasClass("disabled")) {
  //     $.ajax({
  //       type: 'GET',
  //       url: $(this).attr('href'),
  //       success: function (response) {
  //       }
  //     });
  //   }
  //   $(this).addClass("disabled");
  //   checkStatus($(this).attr("id"));
  //   return false;
  // });

  // Check the status of a listing (not used here)
  // function checkStatus(listingid) {
  //   var timer = setInterval(function () {
  //     $.ajax({
  //       type: 'GET',
  //       url: '/listings/' + listingid + '/status',
  //       success: function (response) {
  //         if (response === "Active") {
  //           clearInterval(timer);
  //           $("tr[data-listing-id='" + listingid + "'] td.listing-status").html(response);
  //           $("a#" + listingid).removeClass("disabled");
  //         }
  //       }
  //     });
  //   }, 3000);
  // }

  // Listings filters
  $('#filter-draft').click(function() {
  window.listings.filter(function(item) {
    if (item.values().status == "Draft") {
      return true;
    } else {
      return false;
    }
  });
  return false;
  })();

  $('#filter-active').click(function() {
  window.listings.filter(function(item) {
    if (item.values().status == "Active") {
      return true;
    } else {
      return false;
    }
  });
  return false;
  });

  $('#filter-deleted').click(function() {
  window.listings.filter(function(item) {
    if (item.values().status == "Deleted") {
      return true;
    } else {
      return false;
    }
  });
  return false;
  });

  $('#filter-pending').click(function() {
  window.listings.filter(function(item) {
    if (item.values().status == "Pending") {
      return true;
    } else {
      return false;
    }
  });
  return false;
  });

  $('#filter-sold').click(function() {
  window.listings.filter(function(item) {
    if (item.values().status == "Sold") {
      return true;
    } else {
      return false;
    }
  });
  return false;
  });

  // All
  $('#filter-not-deleted').click(function() {
  window.listings.filter(function(item) {
    if (item.values().status != "Deleted") {
      return true;
    } else {
      return false;
    }
  });
  return false;
  });

  // Make the filter dropdown more intuitive:
  // - Change button text to filter type
  // - Close (toggle) dropdown on click
  // - Scroll to top of listings on filter
  $('.dashboard-filters-text').click(function() {
    window.currentFilterButton = $(this);
    $(".dashboard-filters-button-wrapper").removeClass('selected');
    window.currentFilterButton.parent().addClass('selected');
    $(".listing").first().click();
    $(".dashboard-listings-body").scrollTop(0);
    if (window.currentFilterButton.attr('id') != "filter-deleted") {
      $(".dashboard-delete-btn").removeClass("hide");
      $(".dashboard-delete-permanent-btn").addClass("hide");
    }
    else {
      $(".dashboard-delete-btn").addClass("hide");
      $(".dashboard-delete-permanent-btn").removeClass("hide");
    }
    });

    $(".keyboard-shortcuts-text a").click(function () {
    $("#keyboard-shortcuts-modal").modal();
  });

  var Keys = {
    b: 66, l: 76,
    j: 74, k: 75,
    m: 77, r: 82, n: 78,
    esc: 27, enter: 13, slash: 191,
    shift: 16, qmark: 191,
    rarr: 39, larr: 37,
    up: 38, down: 40,
    context: "l",
    keys: [],
    init: function () {
      this.cacheElements();
      this.bindEvents();
    },
    cacheElements: function () {
      this.$body = $("body");
      this.$listings = $(".dashboard-listings-body");
      this.$buyers = $(".dashboard-buyers-body");
      this.$search = $("input.search");
      this.$refresh = $(".dashboard-refresh");
      this.$messageFormWrapper = $(".dashboard-dashboard-dashboard-dashboard-message-form-wrapper");
      this.$message = this.$messageFormWrapper.find("textarea");
    },
    bindEvents: function () {
      var $doc = $(document);
      $doc.on('keydown', this.addKey);
      $doc.on('keydown', this.executeEvents);
      $doc.on('keyup', this.removeKey);
    },
    addKey: function (e) {
      var key = e.which || e.keyCode;
      if (Keys.keys.indexOf(key) == -1) {
        Keys.keys.push(key);
      }
    },
    removeKey: function (e) {
      var key = e.which || e.keyCode;
      var keyIndex = Keys.keys.indexOf(key);
      Keys.keys.splice(keyIndex, 1);
    },
    executeEvents: function (e) {
      var keys = Keys.keys;
      var context = Keys.context;
      if (keys.length > 1) {
        if ((keys.length == 2) 
          && (keys.indexOf(Keys.shift) != -1) 
          && (keys.indexOf(Keys.qmark) != -1)
          && (!Keys.$search.is(":focus")) 
          && (!Keys.$message.is(":focus"))) {
          $("#keyboard-shortcuts-modal").modal('toggle');
        }
      }
      if (!Keys.$body.hasClass("modal-open")) {
        if ((!Keys.$search.is(":focus")) && (!Keys.$message.is(":focus"))) {
          switch (keys[0]) {
            case Keys.l:
            case Keys.larr:
              if (Keys.$listings.find("li:not(.hide)").length != 0) {
                Keys.context = "l";
              }
              break;
            case Keys.b:
            case Keys.rarr:
              if (Keys.$buyers.find("ul:not(.hide)").length != 0) {
                Keys.context = "b";
              }
              break;
            case Keys.j:
            case Keys.down:
              switch (context) {
                case "l":
                  var currentSelectedListing = Keys.$listings.find("li.highlight");
                  var nextListing = currentSelectedListing.next("li:not(.hide)");
                  if (nextListing.exists()) {
                    nextListing.click();
                    Keys.$listings.scrollTo(nextListing)
                  }
                  break;
                case "b":
                  var currentSelectedBuyer = Keys.$buyers.find("ul.highlight");
                  var nextBuyer = currentSelectedBuyer.next("ul:not(.hide)");
                  if (nextBuyer.exists()) {
                    nextBuyer.click();
                    Keys.$buyers.scrollTo(nextBuyer);
                  }
                  break;
              }
              break;
            case Keys.k:
            case Keys.up:
              switch (context) {
                case "l":
                  var currentSelectedListing = Keys.$listings.find("li.highlight");
                  var prevListing = currentSelectedListing.prev("li:not(.hide)");
                  if (prevListing.exists()) {
                    prevListing.click();
                    Keys.$listings.scrollTo(prevListing)
                  }
                  break;
                case "b":
                  var currentSelectedBuyer = Keys.$buyers.find("ul.highlight");
                  var prevBuyer = currentSelectedBuyer.prev("ul:not(.hide)");
                  if (prevBuyer.exists()) {
                    prevBuyer.click();
                    Keys.$buyers.scrollTo(prevBuyer);
                  }
                  break;
              }
              break;
            case Keys.m:
              if (!Keys.$messageFormWrapper.hasClass("hide")) {
                Keys.$message.focus();
                return false;
              }
              break;
            case Keys.slash:
              Keys.$search.focus();
              return false;
              break;
            case Keys.r:
              Keys.$refresh.click();
              break;
            case Keys.n:
              window.location.href = "/listings/new";
              break;
          }
        }
        if (((Keys.$search.is(":focus")) || (Keys.$message.is(":focus"))) 
          && (keys[0] == Keys.esc)) {
          Keys.$search.blur();
          Keys.$message.blur();
          return false;
        }
        if (Keys.$search.is(":focus") && (keys[0] == Keys.enter)) {
          Keys.$search.blur();
          $(".listing").first().click();
          window.searchHasFocus = false;
          return false;
        }
      }
    }
  }
  Keys.init();

  // Init
  bindEvents();
  $(".message.unread").each(function () {
    var buyer   = $(this).data('buyer-id'),
      listing = $(this).data('listing-id');
    $('.buyer[data-buyer-id="' + buyer + '"]').addClass("unread");
    $('.listing[data-listing-id="' + listing + '"]').addClass("unread");
  });
  // Convert links in the message text
  $(".message-content").each(function() {
    $(this).html(linkToClickable($(this).text()));
  });
})();