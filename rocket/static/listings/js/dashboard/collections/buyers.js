'use strict';

var app = app || {};

app.Buyers = Backbone.Collection.extend({
  url: '/api/buyers',
  model: app.Buyer,
  initialize: function(models, options) {}
});