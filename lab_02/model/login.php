<?php

namespace Model;

require_once 'Database/SqliteAdapter.php';

class Login {
  private $db;
  private $adapter;

  public function __construct() {
    $this->adapter = new \SqliteAdapter();
    $this->db = $this->adapter->connect();
  }

  public function isUser($user, $password) {
    $fields = "id";
    $table = "users";

    $result = $this->adapter->select($table, $fields, array("username", "password"), array($user, $password));

    return $result;
  }

  public function getUser($user) {
    $fields = "*";
    $table = "users";

    $result = $this->adapter->select($table, $fields, "username", array($user));

    return $result;
  }

  public function logout() {
    unset($_SESSION["user"]);
    unset($_SESSION["login_string"]);
  }

  // public function sec_session_start() {
  //   $session_name = 'sec_session_id'; // Set a custom session name
  //   $secure = false; // Set to true if using https.
  //   ini_set('session.use_only_cookies', 1); // Forces sessions to only use cookies.
  //   $cookieParams = session_get_cookie_params(); // Gets current cookies params.
  //   session_set_cookie_params(3600, $cookieParams["path"], $cookieParams["domain"], $secure, false);
  //   $httponly = true; // This stops javascript being able to access the session id.
  //   session_name($session_name); // Sets the session name to the one set above.
  //   session_start(); // Start the php session
  //   session_regenerate_id(); // regenerated the session, delete the old one.
  // }

  public function checkUser() {
    if(!isset($_SESSION["user"])) {
      return false;
    }

    $user = $this->getUser($_SESSION["user"]);
    $un = $user[0]["username"];

    if(isset($_SESSION['login_string'])) {
      if($_SESSION['login_string'] !== hash('sha512', "123456" + $un) ) {
        return false;
      }
    }
    else {
      return false;
    }
    return true;
  }
}