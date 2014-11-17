<?php

namespace View;

class Login {
  private $user = "username";
  private $password = "password";

  /**
   * Just a bunch of plain ol'html.
   * @return Echos HTML
   */
  public function showLogin() {
    $ret = '<!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="">
        <meta name="author" content="">
        <link rel="shortcut icon" href="static/ico/favicon.png">
        <title>Mezzy Labbage - Logga in</title>
        <!-- Bootstrap core CSS -->
        <link href="static/css/bootstrap.css" rel="stylesheet">
        <link href="static/css/login.css" rel="stylesheet">
        <script type="text/javascript" src="static/js/jquery.js"></script>
        <script src="static/js/bootstrap.js"></script>
      </head>

      <body>

        <div class="container">

          <form class="form-signin" action="." method="POST">
            <h2 class="form-signin-heading">Log in</h2>
            <input value="" name="username" type="text" class="form-control" placeholder="Användarnamn" required autofocus>
            <input value="" name="password" type="password" class="form-control" placeholder="Password" required>
            <button class="btn btn-lg btn-primary btn-block" name="login" type="submit">Log in</button>
          </form>
        </div> <!-- /container -->
      </body>
    </html>

    ';

    echo $ret;
  }

  /**
   * Just check if the user POST's the 'login'
   * @return Boolean
   */
  public function userWantsToLogin() {
    return isset($_POST['login']);
  }

  /**
   * Get the value of the given user field.
   * @return String
   */
  public function getUserField() {
    if (isset($_POST[$this->user])) {
      return $_POST[$this->user];
    }
  }

  /**
   * Just check if the user GET's the 'logout'
   * @return Boolean
   */
  public function userWantsToLogout() {
    return isset($_GET['logout']);
  }

  /**
   * Get the value of the given password field.
   * @return String
   */
  public function getPasswordField() {
    if (isset($_POST[$this->password])) {
      return $_POST[$this->password];
    }
  }

  /**
   * Just a simple redirect (header location).
   * @return HTTP REDIRECT (301)
   */
  public function redirectTo($path) {
    header('Location: ' . $path);
  }
}