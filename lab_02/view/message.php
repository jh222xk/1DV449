<?php

namespace View;

class Message {
  private $message = "mess";

  /**
   * Get the value of the given message field.
   * @return String
   */
  public function getMessageField() {
    if (isset($_POST[$this->message])) {
      return $_POST[$this->message];
    }
  }

  /**
   * Just check if the user GET's the 'add_message'
   * @return Boolean
   */
  public function userWantsToAddMsg() {
    return isset($_GET['add_message']);
  }

  /**
   * Just check if the user GET's the 'get_messages'
   * @return Boolean
   */
  public function userWantsToGetMessages() {
    return isset($_GET['get_messages']);
  }

  public function csrfError() {
    return "<h1>ERROR, CSRF TOKEN INVALID!</h1>";
  }

  /**
   * Just a bunch of plain ol'html.
   * @return Echos HTML
   */
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
          <link rel="shortcut icon" href="static/pic/favicon.png">
          <link href="static/css/compressed.css" rel="stylesheet">
          <title>Messy Labbage</title>
        </head>
            <body>

              <div id="container">

                  <div id="messageboard">
                      <a href="?logout" class="btn btn-danger" id="buttonLogout" value="Logout" style="margin-bottom: 10px;">Logout</a>

                      <div id="messagearea"></div>

                      <p id="numberOfMess">Antal meddelanden: <span id="nrOfMessages">0</span></p>
                      Message: <br />
                      <textarea name="mess" id="inputText" cols="55" rows="6"></textarea>
                      <input type="hidden" id="csrf_token" name="csrf_token" value="';
                      $ret .= $_SESSION["csrf_token"];

                      $ret .= '"/><input class="btn btn-primary" type="button" name="add_message" id="buttonSend" value="Write your message" />
                      <span class="clear">&nbsp;</span>

                  </div>

              </div>

            <script src="static/js/compressed.js"></script>
            <script>
              $(document).ready(function() {
                MessageBoard.getMessages();
              });
            </script>
        </body>
        </html>';
    echo $ret;
  }
}