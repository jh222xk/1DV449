<?php

namespace Model;

require_once 'Database/SqliteAdapter.php';

class Login {
  private $db;
  private $adapter;
  private $clientIdentifier;

  public function __construct() {
    $this->adapter = new \SqliteAdapter();
    $this->db = $this->adapter->connect();
    $this->clientIdentifier = $_SERVER["REMOTE_ADDR"] . $_SERVER["HTTP_USER_AGENT"];
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

  public function login($user) {
    $_SESSION["user"] = $user;
    $_SESSION["client_identifier"] = base64_encode($this->clientIdentifier);
  }

  public function logout() {
    unset($_SESSION["user"]);
    unset($_SESSION["client_identifier"]);
  }

  public function checkUser() {
    if(!isset($_SESSION["user"]) || isset($_SESSION["client_identifier"]) && base64_decode($_SESSION["client_identifier"]) !== $this->clientIdentifier) {
      return false;
    }

    $user = $this->getUser($_SESSION["user"]);

    return true;
  }
}