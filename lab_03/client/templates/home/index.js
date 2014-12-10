(function() {
  var markersArray = [];

  Template.map.rendered = function() {
    /*
    (0 = Vägtrafik, 1 = Kollektivtrafik, 2 = Planerad störning, 3 = Övrigt, Alla kategorier = 4)
    (1 = Mycket allvarlig händelse, 2 = Stor händelse, 3 = Störning, 4 = Information, 5 = Mindre störning)
    */

    var isMap, allInfo, mapOptions, marker,
        minZoomLevel, distinctEntries;

    minZoomLevel = 4;
    moment.locale('sv');

    var markerUrl = Session.get('marker_url');
    var areaUrl = Session.get('clickedArea');

    console.log(markerUrl);

    console.log(areaUrl);

    // if (markerUrl) {
    //   var clickedMarker = $(event.currentTarget).attr('class');
    //   google.maps.event.trigger(markersArray[clickedMarker], 'click');
    //   $('a').trigger('click');
    // };

    var categoryArr = [];
    var categoriesNames = ["Vägtrafik", "Kollektivtrafik", "Planerad störning", "Övrigt", "Alla kategorier"];

    mapOptions = {
      zoom: markerUrl ? 10 : 6,
        center: markerUrl ? new google.maps.LatLng(markerUrl.lat, markerUrl.long) : new google.maps.LatLng(62.00, 15.00),
        styles:
        [
          {
            "stylers": [
              { "saturation": -100 },
              { "lightness": 30 }
            ]
          },
          {
            "featureType": "poi",
            "stylers": [
              { "visibility": "off" }
            ]
          }
        ],
        disableDefaultUI: true,
        zoomControl: true,
        draggable: true
    };

    google.maps.Map.prototype.clearOverlays = function() {
      for (var i = 0; i < markersArray.length; i++ ) {
        markersArray[i].setMap(null);
      }
      markersArray.length = 0;
    }
    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

    Deps.autorun(function() {
      var infoWindow = new google.maps.InfoWindow();
      selectVal = Session.get("selectVal");
      selectVal = parseInt(selectVal, 10);

      isMap = Session.get('map');
      if (isMap) {
        if (selectVal && selectVal !== 4) {
          allInfo = SR.find({'category': selectVal}).fetch();
        } else {
          allInfo = SR.find().fetch();
        }

        map.clearOverlays();

        allInfo.forEach(function (item) {
          marker = new google.maps.Marker({
            clickable: true,
            position: new google.maps.LatLng(item.latitude, item.longitude),
            map: map,
            title: item.title,
            // Choose icon depending on priority
            icon: (item.priority == 5) ? '/marker_small_green.png'
              : (item.priority == 4) ? '/marker_small_blue.png'
              : (item.priority == 3) ? '/marker_small_yellow.png'
              : (item.priority == 2) ? '/marker_small_orange.png'
              : 'marker_small_red.png',
            postId: item._id
          });

          var myMark = marker;

          markersArray.push(marker);

          // Add event handler for markers.
          google.maps.event.addListener(marker, 'click', function() {
            infoWindow.setContent(
              '<div id="info-window">' +
                '<h4>' + item.title + '</h4>' +
                '<p>' + item.description + '</p>' +
                '<b>Rapporterad när</b>: <p><time class="map-trafic-date" datetime="' + item.created_at + '"' + item.created_at + '</time></p>' +
                '<b>Kategori</b>: <p>' + categoriesNames[item.category] + '</p>' +
              '</div>'
            );

            infoWindow.open(map, myMark);

            $('.map-trafic-date').each(function(i, e) {
              var time = $(e).attr('datetime');
              $(e).html('<span>' + moment(time).fromNow() + '</span>');
            });
          });
        });
      }

      // Get our categories
      distinctCategories = _.uniq(SR.find({}, {
          sort: {category: 1}, fields: {category: true}
      }).fetch().map(function(x) {
          return x.category;
      }), true);

      if ($('#trafic-categories option').length <= 3) {

        distinctCategories.forEach(function (item, i) {
          $('.form-control')
           .append($("<option></option>")
           .attr("value", i)
           .text(categoriesNames[i]));
        });
      }
    });

    // Limit the zoom level
    google.maps.event.addListener(map, 'zoom_changed', function() {
      if (map.getZoom() < minZoomLevel) map.setZoom(minZoomLevel);
    });

    Session.set('map', true);

    // Right sidebar
    $('[data-toggle=offcanvas]').click(function () {
      if ($('.sidebar-offcanvas').css('background-color') == 'rgb(255, 255, 255)') {
        $('.list-group-item').attr('tabindex', '-1');
      } else {
        $('.list-group-item').attr('tabindex', '');
      }
      $('.row-offcanvas').toggleClass('active');
    });
  }

  Template.map.destroyed = function() {
    Session.set('map', false);
    Session.set("selectVal", null);
  }

  Template.home.events({
    'change #trafic-categories': function (event) {
      var selectVal = $(event.currentTarget).find(':selected').attr('value');
      Session.set("selectVal", selectVal);
    },
    'click .trafic-info a': function(event) {
      var clickedMarker = $(event.currentTarget).attr('class');
      google.maps.event.trigger(markersArray[clickedMarker], 'click');
    },
    'click .area-info a': function(event) {
      event.preventDefault();
      var clickedArea = $(event.currentTarget).attr('href');
      Session.set("clickedArea", clickedArea);
      console.log(clickedArea);
    }
  });
})();