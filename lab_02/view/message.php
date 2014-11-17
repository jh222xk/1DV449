<?php

namespace View;

class Message {
  private $message = "mess";

  public function getMessageField() {
    if (isset($_POST[$this->message])) {
      return $_POST[$this->message];
    }
  }

  public function userWantsToAddMsg() {
    return isset($_GET['add_message']);
  }

  public function userWantsToGetMessages() {
    return isset($_GET['get_messages']);
  }

  public function showMessages() {
    $ret = '
      <!DOCTYPE html>
      <html lang="sv">
        <head>
          <meta charset="utf-8">
          <meta http-equiv="X-UA-Compatible" content="IE=edge">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <meta name="description" content="">
          <meta name="author" content="">
          <link rel="apple-touch-icon" href="touch-icon-iphone.png">
          <link rel="apple-touch-icon" sizes="76x76" href="touch-icon-ipad.png">
          <link rel="apple-touch-icon" sizes="120x120" href="touch-icon-iphone-retina.png">
          <link rel="apple-touch-icon" sizes="152x152" href="touch-icon-ipad-retina.png">
          <link rel="shortcut icon" href="static/pic/favicon.png">
          <link rel="stylesheet" type="text/css" href="static/css/bootstrap.css" />
          <link rel="stylesheet" type="text/css" href="static/css/dyn.css" />
        <script type="text/javascript" src="static/js/jquery.js"></script>
        <!-- <script type="text/javascript" src="static/js/longpoll.js"></script> -->

        <script src="static/js/jquery.js"></script>
        <script src="static/js/MessageBoard.js"></script>
        <script src="static/js/script.js"></script>
        <script src="static/js/Message.js"></script>
        <title>Messy Labbage</title>
        </head>
            <body background="http://www.lockley.net/backgds/big_leo_minor.jpg">

              <div id="container">

                  <div id="messageboard">
                      <input class="btn btn-danger" type="button" id="buttonLogout" value="Logout" style="margin-bottom: 20px;" />

                      <div id="messagearea"></div>

                      <p id="numberOfMess">Antal meddelanden: <span id="nrOfMessages">0</span></p>
                      Message: <br />
                      <textarea name="mess" id="inputText" cols="55" rows="6"></textarea>
                      <input class="btn btn-primary" type="button" name="add_message" id="buttonSend" value="Write your message" />
                      <span class="clear">&nbsp;</span>

                  </div>

              </div>
              <!-- This script is running to get the messages -->
            <script>
              $(document).ready(function() {
                MessageBoard.getMessages();
              });
            </script>
            <script src="static/js/bootstrap.js"></script>
        </body>
        </html>';
    echo $ret;
  }
}