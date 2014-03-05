'use strict';

var app = app || {};

app.Messages = Backbone.Collection.extend({
  url: '/api/messages',
  model: app.Message,
  initialize: function(models, options) {},
});