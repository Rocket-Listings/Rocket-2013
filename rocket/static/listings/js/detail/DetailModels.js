var Listing = Backbone.Model.extend({
  urlRoot: '/api/listings',
  validate: function(attrs, options) {
      // this.validateLength('price', 1, 8) || null, 
    var errors = _.filter([
      this.validateLength('title', 3, 100) || null,
      this.validateExists('category') || null,
      this.validateExists('market', 3, 100) || null ], 
    function(obj) { return Boolean(obj); });
    // errors.description = this.validateExists('description', attrs.description);
    if (errors.length) {
      return errors;
    }
  },
  validateExists: function(name) {
    if (!this.get(name)) {
      return { 
        field: name, 
        message: "You should select a " + name + "."
      };
    }
  },
  validateLength: function(name, min, max) {
    var value = this.get(name);
    var msg;
    if (value) {
      if(value.length <= min) {
        msg = "Your " + name + " must be longer than" + min + "characters.";
      } else if (value.length >= max) {
        msg = "Your " + name + " must be shorter than" + max + "characters.";
      };
    } else {
      msg = "Don't forget to enter a " + name;
    };
    if (msg) {
      return {
        field: name,
        message: msg
      }
    }
  }
});

var Spec = Backbone.Model.extend({
  toJSON: function() {
    var json = Backbone.Model.prototype.toJSON.apply(this, arguments);
    if (!this.id && this.cid) {          
      json.id = this.cid;
    }
    return json;
  },
  validate: function(attrs, options) {
    if (options && options.notEmpty && attrs.value.trim().length == 0) {
      return { field: attrs.name, message: "Craigslist requires that this field not be empty." };
    }
  }
});

var SpecList = Backbone.Collection.extend({
  model: Spec,
  url: '/api/specs',
  initialize: function(specs, options){
    this.listing = options.listing;
    _.bindAll(this, 'isValid');
  },
  isValid: function() {
    var result = this.validate();
    if (result) {
      this.validationError = result;
      return false;
    }
    return true;
  },
  validate: function() {
    var isCarsTrucks = (this.listing.get('category') == 12);
    var result = _.chain(this.models)
      .map(function(model) {
        var name = model.get('name');
        // craigslist cars and truck exception
        if (isCarsTrucks 
            && (name == 'make' || name == 'model' || name == 'year') 
            && !model.isValid({ notEmpty: true })) {
          return model.validationError;
        }
      })
      .filter(function(obj) {
        return Boolean(obj);
      })
      .value();
    console.log(result);
    if (result.length > 0) {
      return result;
    }
  },
  toJSON: function() {
    var specs = this.filter(function(spec) {
      return Boolean(spec.get('value').trim());
    });
    return _.map(specs, function(spec) { return spec.toJSON(); });
  },
  removeEmpty: function() {
    this.reset(this.filter(function(spec) {
      return Boolean(spec.get('value').trim());
    }));
  }
});

var Photo = Backbone.Model.extend({
  toJSON: function() {
    var json = Backbone.Model.prototype.toJSON.apply(this, arguments);
    if (!this.id && this.cid) {
      json.id = this.cid;
    }
    return json;
  }, 
  validation: function(attrs, options) {} // no validation for now.
});

var PhotoList = Backbone.Collection.extend({
  model: Photo,
  url: '/api/photos',
  comparator: 'order',
  isValid: function() {
    return _.all(this.models, function(model) {
      return model.isValid();
    });
  }
});