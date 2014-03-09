'use strict';

var app = app || {};

app.Message = Backbone.Model.extend({
  urlRoot: '/api/messages',
  initialize: function(attrs, options) {},
});