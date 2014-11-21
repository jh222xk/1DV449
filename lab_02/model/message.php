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
    $result = $this->adapter->insert("messages", array("message" => $message, "name" => $user, "date" => time()));

    // Send the message back to the client
    return $result;
  }

  public function getLastMessage() {
    return $this->adapter->select("messages", "date", null, null, "date", 1);
  }

  /**
   * Get the specific message
   * @return Array
   */
  public function getMessages() {
    $fields = "*";
    $table = "messages";

    $result = $this->adapter->select($table, $fields, null, null, "date");

    return $result;
  }
}
