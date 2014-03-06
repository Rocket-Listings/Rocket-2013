'use strict';

var app = app || {};

app.DashboardView = Backbone.View.extend({
  el: '#dashboard',
  events: {
    'click .sort': 'sort',
    'click .close': 'closeFirstVisitAlert',
    'click .dashboard-refresh': 'refresh',
    'submit form.dashboard-dashboard-message-form': 'sendMessage',
    'click .dashboard-delete-btn': 'markSelected',
    'click .dashboard-delete-permanent-btn': 'destroyMarked',
    'keydown input.search': 'search',
    'focus input.search': 'toggleSearch',
    'click .dashboard-search-btn': 'forceSearch'
  },
  initialize: function() {
    this.$listings = this.$('.dashboard-listings-inner-body');
    this.$buyers = this.$('.dashboard-buyers-body');
    this.$messages = this.$('.dashboard-messages-inner-body');

    // ids of the selected listing and buyer
    this.listingSelected = -1;
    this.buyerSelected = -1;

    this.listingFilter = {};
    this.buyerFilter = {};

    this.shownListings = new app.Listings;
    this.shownBuyers = new app.Buyers;
    this.shownMessages = new app.Messages;

    // Dashboard refreshes will always be resets for now.
    // this.listenTo(this.collection, 'add', this.showListing);
    this.listenTo(this.collection, 'set', this.showListings);    
    this.listenTo(this.collection, 'all', this.render);
    this.listenTo(this.collection, 'reset', this.onReset);
    this.onReset();
  },
  onReset: function() {
    this.collection.each(function(listing) {
      this.listenTo(listing, 'change:selected', this.listingSelectedChange);
      // this.listenTo(listing, 'change:selected', this.listingSelectedChange);
      // again, not implementing add case just yet
      // this.listenTo(listing.buyers, 'set', this.showBuyers);
      // this.listenTo(listing.buyers, 'all', this.render);      
      listing.buyers.each(function(buyer) {
        this.listenTo(buyer, 'change:selected', this.buyerSelectedChange);
        // not paying attention to this event for now
        // this.listenTo(buyer.messages, 'set', this.showMessages);
        // this.listenTo(buyer.messages, 'all', this.render);
      }, this);
    }, this);
    this.showListings(this.collection);
  },
  showListings: function(listings) {
    var listingsFiltered = listings.filter(_.matches(this.listingFilter));
    this.shownListings.set(listingsFiltered);
    if (this.shownListings.length === 0) {
      this.$('.dashboard-listings-message.no-listings').show();
      return;
    } else {
      this.$('.dashboard-listings-message.no-listings').hide();
    }
    this.shownListings.each(function(listing) {
      // add the model to the current model collection,
      // and instantiate and attach the model's view to the dom.
      var view = new app.ListingView({ model: listing });
      this.$listings.append(view.render().el);      
    }, this);
  },
  listingSelectedChange: function(listing, selected) {
    // TODO: implement multiselect
    if(selected) { // not unselected
      if (this.listingSelected >= 0) {
        // this sets off another event, running this method a second time.
        this.shownListings.get(this.listingSelected).set({ 'selected': false });
      }
      this.listingSelected = listing.id;
      this.showBuyers(listing.buyers);
    }
  },
  showBuyers: function(buyers) {
    this.shownMessages.set([]);
    this.hideMessagesAlerts();
    this.$('.dashboard-messages-message.no-buyer-selected').show();

    // TODO: rename to setShownBuyers
    var buyersFiltered = buyers.filter(_.matches(this.buyerFilter));
    this.shownBuyers.set(buyersFiltered);
    this.hideBuyersAlerts();
    if (this.shownBuyers.length === 0) {
      this.$('.dashboard-buyers-message.no-buyers').show();
      return;
    }
    this.buyerSelected = -1;
    var selected = this.shownBuyers.findWhere({ 'selected': true });
    if (selected) {
      this.buyerSelectedChange(selected, true);
    }
    this.shownBuyers.each(function(buyer) {
      var view = new app.BuyerView({ model: buyer });
      this.$buyers.append(view.render().el);
    }, this);
  },
  hideBuyersAlerts: function() {
    this.$('.dashboard-buyers-message').hide();
  },
  buyerSelectedChange: function(buyer, selected) {
    // TODO: implement multiselect
    if(selected) { // not unselected
      if (this.buyerSelected >= 0) {
        this.shownBuyers.get(this.buyerSelected).set({ 'selected': false });
      }
      this.buyerSelected = buyer.id;
      this.showMessages(buyer.messages);
    }
  },
  showMessages: function(messages) {
    this.shownMessages.set(messages.models);
    this.hideMessagesAlerts();
    if (this.shownMessages.length === 0) {
      this.$('.dashboard-messages-message.no-messages').show();
      return;
    } else {
      this.$('.dashboard-message-form').show();
    }
    this.shownMessages.each(function(message) {
      var view = new app.MessageView({ model: message });
      this.$messages.append(view.render().el);
    }, this);
  },
  hideMessagesAlerts: function() {
    this.$('.dashboard-message-form').hide();
    this.$('.dashboard-messages-message').hide();
  },
  render: function() {
    // render app wide changes that don't include the listings, buyers, or messages panels.
  },
  sort: function() {
    // TODO: refactor
    // var icon = $(this).next('span'),
    //     icons = $("span.glyphicon.sort-toggle"),
    //     iconsNotClicked = $("span.glyphicon.sort-toggle:not('span.glyphicon.active')"),
    //     down = 'glyphicon-chevron-down',
    //     up = 'glyphicon-chevron-up';
    // icons.addClass("hide").removeClass("active");
    // icon.removeClass("hide").addClass('active');
    // iconsNotClicked.removeClass(down + " " + up).addClass(down);
    // if (icon.hasClass(down)) {
    //   icon.removeClass(down).addClass(up);
    // }
    // else {
    //   icon.removeClass(up).addClass(down);
    // }
    // return false;
  },
  closeFirstVisitAlert: function(event) {
    // Remove the 'first-visit' class from the dashboard panel
    // This will move the dashboard back up on the page when
    // the first visit info box is closed
    // $('.dashboard-body').removeClass("first-visit");
  },
  refresh: function(e) {
    // e.preventDefault();
    // var currentSelectedListing = $(".dashboard-listings-body").find("li.highlight").data('listing-id');
    //   $.ajax({
    //     type: 'GET',
    //     url: '/listings/dashboard/data/',
    //     data: {'listing': $(".last-listing").text(),
    //          'buyer': $(".last-buyer").text(),
    //          'message': $(".last-message").text()},
    //       success: function (response) {
    //         insertNewData(response);
    //         unbindEvents(); // To prevent overlap
    //         bindEvents(); // Bind all items (including new)
    //         $(".message.unread").each(function () {
    //           var buyer   = $(this).data('buyer-id'),
    //             listing = $(this).data('listing-id');
    //           $('.buyer[data-buyer-id="' + buyer + '"]').addClass("unread");
    //           $('.listing[data-listing-id="' + listing + '"]').addClass("unread");
    //         });
    //         if (currentSelectedListing != null) {
    //           // Maintain the clicked listing
    //           $(".dashboard-listings-body").find("li[data-listing-id='" + currentSelectedListing + "']").click();
    //         }
    //         else { $(".dashboard-listings-body li").first().click(); }
    //       }
    //     });
  },
  sendMessage: function() {
    // Submit and handle a new message
    // var csrftoken = getCookie('csrftoken');
    // $.ajax({
    //   url: '/listings/dashboard/message/',
    //   method: 'POST',
    //   data: $(this).serialize(),
    //   beforeSend: function(xhr) {
    //     xhr.setRequestHeader("X-CSRFToken", csrftoken);
    //   },
    //   success: function (response) {
    //     switch (response.status) {
    //       case 'success':
    //         console.log(response);
    //         $(".dashboard-messages-body").append(Mustache.render($("#message-template").html(), response));
    //         $(".message[data-message-id='" + response.messages.message_id +"'], .buyer[data-buyer-id='" + response.messages.buyer_id + "']").removeClass("hide");
    //         $('.dashboard-messages-body').scrollBottom();
    //         $('.last-message').text(response.messages.message_id);
    //         $('.dashboard-dashboard-message-form textarea').val("").focus();
    //         break;
    //       case 'err_validation':
    //         console.log("There was an error sending the message.");
    //         break;
    //       case 'err_empty':
    //         break;
    //     }
    //   },
    //   error: function (response) {
    //     console.log("There was an error sending the message.");
    //   }
    // });
    // return false;
  },
  markSelected: function(e) {
    // Change the status of the selected listing to "Deleted"
    // var id = $(this).attr('data-listing-id');
    // e.preventDefault();
    // if (!$(this).hasClass("disabled")) {
    //   $.ajax({
    //     url: '/listings/' + id + '/status/update',
    //     method: 'GET',
    //     data: {'status': 'Deleted'},
    //     success: function (response) {
    //       var item = window.listings.get('id', response.listing.id);
    //       item.values({'status': response.listing.status});
    //       $('.listing[data-listing-id="' + response.listing.id + '"]').addClass('deleted').removeClass('active draft pending sold');
    //       window.currentFilterButton.click();
    //     }
    //   });
    // }
  },
  destroyMarked: function() {
    // // Delete the currently selected listing
    // var id = $(this).attr('data-listing-id');
    // e.preventDefault();
    // if (!$(this).hasClass("disabled")) {
    //   $.ajax({
    //     url: '/listings/' + id + '/delete',
    //     method: 'GET',
    //     success: function () {
    //       $(".buyer[data-listing-id='" + id + "'], .message[data-listing-id='" + id + "']").remove();
    //       window.listings.remove('id', id);
    //       window.currentFilterButton.click();
    //       $(".dashboard-listings-body").scrollTop(0);
    //     }
    //   });
    // }
    // return false;
  },
  search: function(e) {
    // Remove focus from the listings and hide buyers/messages during search
    // $(".dashboard-buyers-body, .dashboard-messages-body, .dashboard-dashboard-dashboard-dashboard-message-form-wrapper").addClass("hide");
    // $(".dashboard-listings-body li").removeClass("highlight");
    // $(".dashboard-empty-inbox").removeClass("hide");
    // $(".dashboard-delete-btn, .dashboard-delete-permanent-btn").addClass("disabled");
  },
  toggleSearch: function() {
    // window.searchHasFocus = true;
  },
  forceSearch: function() {
    // if (window.searchHasFocus == true) {
    //   $("input.search").blur();
    //   $(".listing").first().click();
    //   window.searchHasFocus = false;
    // }
    // else {
    //   $("input.search").focus();
    // }
  }
});
