"use strict";

/* dataset_type field in security of classification of organization within manage mode.
 *
 * This JavaScript module will check the value of dataset_type field .  It will switch 
 * to different sets of classification based on this field's value, the dataset_type.
 *
 * params: different sets of different dataset_types.
 *
 */
ckan.module('classification', function ($, _) {
  return {
    initialize: function () {
      $.proxyAll(this, /_on/);
      this.get_classifications(this.el.val())
      this.el.on('change', this._onChange);
    },

    _onChange: function(event){
      this.get_classifications(this.el.val())
    },

    get_classifications: function(dataset_type){
      var classification_field = $('#field-classification');
      var classifications = this.options.classifications[dataset_type];
      var c_list = JSON.parse(classifications);
      classification_field.children().remove();
      $.each(c_list, function (index, value) {
          classification_field.append($('<option/>', { 
              value: value,
              text : value 
          }));
      });
    },

  };
});