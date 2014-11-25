<?php

namespace Model;

require_once 'Database/SqliteAdapter.php';

class Login {
  private $db;
  private $adapter;
  private $clientIdentifier;
  private $csrfToken;

  /**
   * @return Void
   */
  public function __construct() {
    $this->adapter = new \SqliteAdapter();
    $this->db = $this->adapter->connect();
    $this->clientIdentifier = $_SERVER["REMOTE_ADDR"] . $_SERVER["HTTP_USER_AGENT"];
  }

  public function getCsrfToken() {
    return $this->csrfToken;
  }

  private function generateCsrfToken() {
    return base64_encode(openssl_random_pseudo_bytes(32));
  }

  /**
   * Get a given user using username as param
   * @param String $user
   * @return Array
   */
  public function getUser($user) {
    $fields = "*";
    $table = "users";

    $result = $this->adapter->select($table, $fields, "username", "=", array($user));

    return $result;
  }

  /**
   * Logging in the given user, with a given username and password
   * @param String $user
   * @param String $password
   * @return Void
   */
  public function login($user, $password) {
    $storedUser = $this->getUser($user);
    if ($storedUser !== null) {
      if ($this->checkHashedPassword($password, $storedUser[0]["password"])) {
        $_SESSION["user"] = $user;
        $_SESSION["csrf_token"] = $this->generateCsrfToken();
        $_SESSION["client_identifier"] = base64_encode($this->clientIdentifier);
      }
    }
  }

  /**
   * Logging out the user, i.e. kills the session.
   * @return Void
   */
  public function logout() {
    unset($_SESSION["user"]);
    unset($_SESSION["client_identifier"]);
  }

  /**
   * Check if we're logged in. If our session is fine.
   * @return Boolean
   */
  public function checkUser() {
    if(!isset($_SESSION["user"]) || isset($_SESSION["client_identifier"]) && base64_decode($_SESSION["client_identifier"]) !== $this->clientIdentifier) {
      return false;
    }

    $user = $this->getUser($_SESSION["user"]);

    return true;
  }

  /**
   * Hashes the password and returns it, just something for
   * generating a password.
   * @return String
   */
  public function hashPassword($password) {
    return crypt($password);
  }

  /**
   * Check if hashed password matches.
   * @param String $password
   * @param String $hashedPassword
   * @return Boolean
   */
  function checkHashedPassword($password, $hashedPassword) {
    return crypt($password, $hashedPassword) === $hashedPassword;
  }
}