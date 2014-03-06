'use strict';

var app = app || {};

app.BuyerView = Backbone.View.extend({
    model: app.Buyer,
    tagName: 'li',
    template: $("#buyer-template").html(),
    className: 'buyer',
    events: {
      'click': 'select'
    },
    initialize: function(attrs, options) {
      // this.listenTo(this.model, 'all', this.render);
      this.listenTo(this.model, 'destroy', this.remove);
      this.listenTo(this.model, 'change', this.render);
      this.listenTo(this.model, 'remove', this.remove);      
    },
    render: function() {
      var markup = Mustache.render(this.template, { 'buyer': this.model.toJSON() });
      if (this.model.get('selected')) {
        this.$el.addClass('highlight');
      } else {
        this.$el.removeClass('highlight');
      }
      this.$el.html(markup);
      return this;
    },
    select: function() {
      this.model.set({ 'selected': true });
      // var buyerCard = $(this),
      //     buyer_id = buyerCard.data('buyer-id'),
      //     listing_id = buyerCard.data('listing-id'),
      //     unreadMessages = $(".message.unread[data-buyer-id='" + buyer_id + "']");
      // $('.buyer').removeClass('highlight');
      // this.$el.addClass('highlight');
      // $(".message").addClass("hide");
      // $('.message[data-buyer-id="' + buyer_id + '"]').removeClass("hide");
      // $(".dashboard-dashboard-message-form input[name='listing']").val(listing_id);
      // $(".dashboard-dashboard-message-form input[name='buyer']").val(buyer_id);
      // $('.dashboard-messages-body').scrollBottom();
      // unreadMessages.each(function () {
      //   $(this).markSeen(function (data) {
      //     $(".message[data-message-id='" + data.message_id +"'], .buyer[data-buyer-id='" + data.buyer_id + "']").removeClass("unread");
      //     if (data.listing_all_read) {
      //       $(".listing[data-listing-id='" + data.listing_id + "']").removeClass("unread");
      //       $('span.label-info').hide();
      //     }
      //   });
      // });
    }
  // $.fn.markSeen = function(callback) {
  //   var message_id = $(this).data('message-id');
  //   $.ajax({
  //     method: 'GET',
  //     url: '/listings/dashboard/message/seen',
  //     data: {'message_id': message_id},
  //     success: function (response) {
  //       if (response.status == 'success') {
  //         callback(response.message_data);
  //       }
  //       else {
  //         console.log("The server experienced an error.");
  //       }
  //     }
  //   });
  // }
});
