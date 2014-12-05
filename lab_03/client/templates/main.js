SR = new Mongo.Collection('sr');

Template.home.helpers({
  sr: function() {
    var selectVal = Session.get("selectVal");
    selectVal = parseInt(selectVal, 10);
    if (selectVal && selectVal !== 4) {
      srInfo = SR.find({'category': selectVal}).fetch();
    } else {
      srInfo = SR.find({}, {sort: {created_at: -1}}).fetch();
    }
    var index = 0;
    srInfo.map(function(o, i) {
      srInfo[i].index = index++;
    })
    return srInfo;
  }
});