'use strict';

var app = app || {};

app.Listings = Backbone.Collection.extend({
  url: '/api/listings',
  model: app.Listing,
  sortKey: 'title',
  reverseSort: 1, // disabled by default
  comparator: function(listing) {
    var val = listing.get(this.sortKey);
    if (_.isString(val)) {
      return this.strComparator(val, this.reverseSort);
    } else {
      return this.reverseSort * listing.get(this.sortKey);
    }
  },
  // static function
  strComparator: function (str, reverse) {
    str = str.toLowerCase();
    str = str.split('');
    str = _.map(str, function(letter) {
      return String.fromCharCode(reverse * (letter.charCodeAt(0)));
    });
    return str;
  },
});