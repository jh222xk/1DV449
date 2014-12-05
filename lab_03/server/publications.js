SR = new Mongo.Collection('sr');

Meteor.publish('sr', function() {
  var self = this;
  var apiUrl;

  apiUrl = 'http://api.sr.se/api/v2/traffic/messages';

  if (SR.find().count() === 0) {

    var response = HTTP.get(apiUrl, {
      params: {
        // size: 100,
        format: 'json',
        // filtervalue: filterValue
        pagination: false
      }
    });
  }

  if (SR.find().count() === 0) {

    try {

      var jsonData = JSON.parse(response.content);

      _.each(jsonData.messages, function(item) {
        var doc = {
            title: item.title,
            description: item.description,
            latitude: item.latitude,
            longitude: item.longitude,
            exact_location: item.exactlocation,
            category: item.category,
            sub_category: item.subcategory,
            priority: item.priority,
            created_at: item.createddate
          };

          // SR.insert(doc);

          self.added('sr', Random.id(), doc);
      });

      self.ready();
    } catch(error) {
      console.log(error);
    }
  }
});

// Meteor.startup(function () {
//   SR.remove({});
// });