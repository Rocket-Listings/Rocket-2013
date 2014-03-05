'use strict';

var app = app || {};

app.MessageView = Backbone.View.extend({
  model: app.Message,
  tagName: 'li',
  className: function() {
    if(this.model.get('isSeller')) {
      return 'message message-seller';
    } else {
      return 'message message-buyer';
    }
  },
  template: $("#message-template").html(),
  initialize: function(attrs, options) {
    this.listenTo(this.model, 'all', this.render);
    this.listenTo(this.model, 'destroy', this.remove);
  },
  render: function() {
    var markup = Mustache.render(this.template, { 'message': this.model.toJSON() });
    this.$el.html(markup);
    return this;
  },
  // Mark a message as seen on the server
  // Must have attr 'data-message-id'
  markSeen: function(e) {
    // var message_id = $(this).data('message-id');
    // $.ajax({
    //   method: 'GET',
    //   url: '/listings/dashboard/message/seen',
    //   data: {'message_id': message_id},
    //   success: function (response) {
    //     if (response.status == 'success') {
    //       callback(response.message_data);
    //     } else {
    //       console.log("The server experienced an error.");
    //     }
    //   }
    // });
  }
});