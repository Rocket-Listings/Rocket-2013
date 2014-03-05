'use strict';

var app = app || {};

app.Buyer = Backbone.Model.extend({
  initialize: function(attrs, options) {
    this.messages = new app.Messages;
    this.messages.reset(this.get('message_set'));
    this.unset('message_set');
  }
});