'use strict';

var app = app || {};

app.DashboardView = Backbone.View.extend({
  el: '#dashboard',
  events: {
    'click .sort': 'sort',
    'click .close': 'closeFirstVisitAlert',
    'click .dashboard-refresh': 'refresh',
    'submit form.dashboard-message-form': 'sendMessage',
    'click .dashboard-delete-btn': 'markSelected',
    'click .dashboard-delete-permanent-btn': 'destroyMarked',
    'keydown input.search': 'search',
    'click .dashboard-filters-text': 'filter',
    'focus input.search': 'toggleSearch',
    'click .dashboard-search-btn': 'forceSearch'
  },
  initialize: function() {
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      }
    });

    this.$listings = this.$('.dashboard-listings-inner-body');
    this.$buyers = this.$('.dashboard-buyers-body');
    this.$messages = this.$('.dashboard-messages-inner-body');

    // ids of the selected listing and buyer
    this.listingSelected = -1;
    this.buyerSelected = -1;

    this.listingFilter = { "marked": false };
    this.buyerFilter = {};

    this.shownListings = new app.Listings;
    this.shownBuyers = new app.Buyers;
    this.shownMessages = new app.Messages;

    // this.listenTo(this.shownListings, 'sort', this.renderListings);
    this.listenTo(this.shownListings, 'add', function(listing) {
      var view = new app.ListingView({ model: listing });
      this.$listings.append(view.render().el);
    });
    // remove event is automatically triggered on the listing model, 
    // which removes the associated view from the dom

    // this.listenTo(this.shownBuyers, 'sort', this.renderBuyers);
    this.listenTo(this.shownBuyers, 'add', function(buyer) {
      var view = new app.BuyerView({ model: buyer });
      this.$buyers.append(view.render().el);
    });

    // this.listenTo(this.shownMessages, 'sort', this.renderMessages);
    this.listenTo(this.shownMessages, 'add', function(message) {
      var view = new app.MessageView({ model: message });
      this.$messages.append(view.render().el);
    });

    this.listenTo(this.shownListings, 'sort', this.render);
    this.collection.each(function(listing) {
      this.listenTo(listing, 'change:selected', this.listingSelectedChange);
      listing.buyers.each(function(buyer) {
        this.listenTo(buyer, 'change:selected', this.buyerSelectedChange);
      }, this);
    }, this);
    this.shownListings.set(this.listingsFiltered());    
    this.renderListings();
  },
  listingsFiltered: function() {
    return this.collection.where(this.listingFilter);
  },
  buyersFiltered: function() {
    if (this.listingSelected !== -1) {
      if (_.isEmpty(this.buyerFilter))
        return this.collection.get(this.listingSelected).buyers.models;
      else
        return this.collection.get(this.listingSelected).buyers.where(this.buyerFilter);
    }
  },
  messagesFiltered: function() {
    if (this.listingSelected !== -1 && this.buyerSelected !== -1) {
      return this.collection.get(this.listingSelected).buyers
                            .get(this.buyerSelected).messages.models;
    }
  },
  render: function() {
    // render app wide changes that don't include the listings, buyers, or messages panels.
  },  
  renderListings: function() {
    if (this.shownListings.length === 0) {
      this.$('.dashboard-listings-message.no-listings').show();
      return;
    } else {
      this.$('.dashboard-listings-message.no-listings').hide();
    }
  },
  renderBuyers: function() {
    // hide messages
    this.shownMessages.set([]);
    this.hideMessagesAlerts();
    this.$('.dashboard-messages-message.no-buyer-selected').show();

    // TODO: rename to setShownBuyers
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
  },
  renderMessages: function() {
    this.hideMessagesAlerts();
    if (this.shownMessages.length === 0) {
      this.$('.dashboard-messages-message.no-buyer-selected').show();
      return;
    } else {
      this.$('.dashboard-message-form').show();
    }
  },
  // UI Methods
  hideBuyersAlerts: function() {
    this.$('.dashboard-buyers-message').hide();
  },  
  hideMessagesAlerts: function() {
    this.$('.dashboard-message-form').hide();
    this.$('.dashboard-messages-message').hide();
  },
  // DOM event callbacks
  listingSelectedChange: function(listing, selected) {
    // TODO: implement multiselect
    if (selected) { // not unselected
      if (this.listingSelected !== -1) {
        // this sets off another event, running this method a second time.
        this.shownListings.get(this.listingSelected).set({ 'selected': false });
      }
      this.listingSelected = listing.id;
      this.shownBuyers.set(this.buyersFiltered());      
      this.renderBuyers();
    }
  },
  buyerSelectedChange: function(buyer, selected) {
    // TODO: implement multiselect
    if (selected) { // not unselected
      if (this.buyerSelected !== -1) {
        this.shownBuyers.get(this.buyerSelected).set({ 'selected': false });
      }
      this.buyerSelected = buyer.id;
      this.shownMessages.set(this.messagesFiltered());      
      this.renderMessages();
    }
  },
  // UI Actions
  filter: function(e) {
    var target = $(e.currentTarget),
        attribute = target.data('filter-attr'),
        value = target.data('filter-val'),
        filter = {};
    // convert string to boolean
    value = (value === 'true') ? true : (value === 'false') ? false : value;
    filter[attribute] = value;
    if (!_.isEqual(filter, this.listingFilter)) {
      this.$('.dashboard-filters-text').parent().removeClass('selected');
      target.parent().addClass('selected');
      this.listingFilter = filter;
      this.shownListings.set(this.listingsFiltered());
      this.renderListings();
    }
  },
  sort: function(e) {
    // TODO: This method should work through a render, not an events simulation hack.
    // Unfortunately events are the only way we have of communicating with the listing views.
    // Later we'll either switch over to Marionette.Backbone.js or keep track of the views.
    var target = $(e.currentTarget),
        targetSortKey = target.data('sort'),
        icon = target.find('.sort-toggle.glyphicon'),
        icons = $('.sort-toggle.glyphicon'),
        down = 'glyphicon-chevron-down',
        up = 'glyphicon-chevron-up';

    if (this.shownListings.sortKey == targetSortKey) {
      this.shownListings.reverseSort *= -1;
    } else {
      this.shownListings.sortKey = targetSortKey;
    }

    if (this.shownListings.reverseSort == 1) {
      icon.removeClass(down).addClass(up);
    } else {
      icon.removeClass(up).addClass(down);
    }

    this.shownListings.sort();
    this.shownListings.chain()
      .each(function(l) {
        l.trigger('remove', l, this.shownListings);
      }, this).each(function(l) {
        l.trigger('add', l, this.shownListings);
      }, this);
    this.renderListings();

    icons.addClass("hide");
    icon.removeClass("hide");
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
  sendMessage: function(e) {
    e.preventDefault();
    var content = $(e.currentTarget).find('textarea').val();
    if (content.length === 0) return;
    var message = new app.Message({
      listing: this.listingSelected,
      isSeller: true,
      buyer: this.buyerSelected,
      content: content,
    });
    var that = this;
    message.save(null, {
      success: function (model, response, options) {
        // $('.dashboard-messages-body').scrollBottom();
        // $('.last-message').text(response.messages.message_id);
        var messages = that.collection.get(that.listingSelected).buyers.get(that.buyerSelected).messages;
        messages.add(message);
        that.shownMessages.set(that.messagesFiltered());
        that.renderMessages();
        $('.dashboard-message-form textarea').val("").focus();
      },
      error: function (model, response, options) {
        console.log(response);
      }
    });
  },
  markSelected: function(e) {
    console.log("mark selected");
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
    console.log("destroy marked");
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
    console.log("search");
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
    console.log("force search");
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
