var app = app || {};

'use strict';

app.Listings = Backbone.Collection.extend({
  url: '/api/listings',
  model: app.Listing,
  initialize: function(models, options) {}
});