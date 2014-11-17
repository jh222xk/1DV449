<?php

namespace Model;

require_once 'Database/SqliteAdapter.php';

class Message {
  private $db;
  private $adapter;

  /**
   * @return Void
   */
  public function __construct() {
    $this->adapter = new \SqliteAdapter();
    $this->db = $this->adapter->connect();
  }

  /**
   * Called from AJAX to add stuff to DB
   * @param String $user
   * @param String $message
   * @return Array
   */
  public function addToDB($user, $message) {
    $result = $this->adapter->insert("messages", array("message" => $message, "name" => $user));

    // Send the message back to the client
    return $result;
  }

  /**
   * Get the specific message
   * @return Array
   */
  public function getMessages() {
    $fields = "*";
    $table = "messages";

    $result = $this->adapter->select($table, $fields);

    return $result;
  }
}
