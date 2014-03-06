'use strict';

var app = app || {};
  
app.Listing = Backbone.Model.extend({
  defaults: {
    "selected": false
  },
  initialize: function(attrs, options) {
    this.buyers = new app.Buyers;
    this.buyers.reset(this.get('buyer_set'));
    this.unset('buyer_set');
  },
});