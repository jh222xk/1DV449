Router.configure({
  layoutTemplate: 'layout',
  loadingTemplate: 'loading',
  notFoundTemplate: 'notFound',
  waitOn: function() {
    return Meteor.subscribe('sr');
  }
});

Router.map(function () {
  this.route('home', {
    path: '/',
    data: function () {
      var params = this.params;
      if (params.query.lat && params.query.long) {
        Session.set("marker_url", {'lat': params.query.lat, 'long': params.query.long});
      };
    }
  });
});