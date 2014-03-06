'use strict';

var app = app || {};

app.ListingView = Backbone.View.extend({
    model: app.Listing,
    tagName: 'li',
    className: 'listing',
    attributes: {
      'data-listing-id': this.id
    },
    template: $("#listing-template").html(),
    events: {
      'click': 'select'
    },
    initialize: function(attrs, options) {
      this.listenTo(this.model, 'change', this.render);
      this.listenTo(this.model, 'destroy', this.remove);
      this.listenTo(this.model, 'remove', this.remove);
    },
    render: function() {
      var markup = Mustache.render(this.template, {'listing': this.model.toJSON() });
      if (this.model.get('selected')) {
        this.$el.addClass('highlight');
      } else {
        this.$el.removeClass('highlight');
      }
      this.$el.addClass(this.model.get('status_lower'));
      this.$el.html(markup);
      return this;
    },
    select: function(e) {
      this.model.set({ 'selected': true });
        // var listingRow = $(e.currentTarget);
        // var id = listingRow.data('listing-id');
        // var buyers = $(".buyer[data-listing-id='" + id + "']");
        // this.$el.removeClass('highlight');
      // this.$('.d-arrow').addClass('hide');
      // this.$el.addClass('highlight');
      // HIDE ALL BUYERS AND MESSAGES
      // ENABLE DASHBOARD LISTING DELETE BUTTON
      // $(".dashboard-delete-btn").attr('data-listing-id', id).removeClass("disabled");
      // if (listingRow.hasClass("deleted")) {
      //   $(".dashboard-delete-permanent-btn").attr('data-listing-id', id).removeClass("disabled");
      // }
      // SHOW BUYERS
      // if (buyers.length) {
      //   $('.d-arrow', this).removeClass('hide');
      //   $(".dashboard-buyers-body").addClass("border-right").removeClass("hide");
      //   $(".dashboard-empty-inbox").addClass("hide");
      //   buyers.removeClass("hide");
      //   buyers.first().click();
      //   $('.dashboard-dashboard-dashboard-dashboard-message-form-wrapper').removeClass("hide");
      //   $('.dashboard-messages-body').removeClass("hide").scrollBottom();
      // } else {
      //   $('.dashboard-dashboard-dashboard-dashboard-message-form-wrapper').addClass("hide");
      //   $(".dashboard-buyers-body").removeClass("border-right").addClass("hide");
      //   $(".dashboard-messages-body").addClass("hide");
      //   $(".dashboard-empty-inbox").removeClass("hide");
      // }
    }
});