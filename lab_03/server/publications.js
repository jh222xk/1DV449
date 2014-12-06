
// Setup our Mongo collections
SR = new Mongo.Collection('sr');
TraficAreas = new Mongo.Collection('trafic_areas');

// Publish our SR collection to the client
Meteor.publish('sr', function() {
  var ONE_HOUR = 60 * 60 * 1000;
  var self = this;

  var apiUrl = 'http://api.sr.se/api/v2/traffic/messages';

  // Fetch data only if our collection is empty
  // or the time is greater than 1h.
  if (SR.find().count() === 0 || ((moment()) - moment(SR.findOne({}, {sort: {fetched: 1}, limit: 1}).fetched)) < ONE_HOUR) {
    try {
      var response = HTTP.get(apiUrl, {
          params: {
            // size: 100,
            format: 'json',
            // filtervalue: filterValue
            pagination: false
          }
        });

      // Parse our data...
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
            created_at: moment(item.createddate).format('YYYY-MM-DD HH:mm:ss'),
            fetched: moment().format('YYYY-MM-DD HH:mm:ss')
          };

          // SR.insert(doc);

          // ... Add our data!
          self.added('sr', Random.id(), doc);
      });

      self.ready();
    } catch(error) {
      console.log(error);
    }
  }
});


Meteor.publish('trafic_areas', function () {
  var ONE_HOUR = 60 * 60 * 1000;
  var self = this;
  var apiUrl = 'http://api.sr.se/api/v2/traffic/areas';

  // if (TraficAreas.find().count() === 0 || ((moment()) - moment(TraficAreas.findOne({}, {sort: {fetched: 1}, limit: 1}).fetched)) < ONE_HOUR) {
    try {
      var response = HTTP.get(apiUrl, {
          params: {
            // size: 100,
            format: 'json',
            // filtervalue: filterValue
            pagination: false
          }
        });

      // Parse our data...
      var jsonData = JSON.parse(response.content);

      _.each(jsonData.areas, function(item) {
        var doc = {
            name: item.name,
            zoom: item.zoom,
            radius: item.radius,
            traffic_department_unit_id: item.trafficdepartmentunitid,
            fetched: moment().format('YYYY-MM-DD HH:mm:ss')
          };

          // ... Add our data!
          self.added('trafic_areas', Random.id(), doc);
      });

      self.ready();

    } catch(error) {
      console.log(error);
    }
  // }
});

/* Debug... Empty our collection if we want some fresh data on startup. */
Meteor.startup(function () {
  SR.remove({});
});
