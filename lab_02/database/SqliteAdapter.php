<?php

class SqliteAdapter {

  protected $dbConnection;

  /**
   * Creates a database conneciton.
   * @return PDO object
   */
  public function connect() {

    if ($this->dbConnection === null) {
      $this->dbConnection = new \PDO('sqlite:database/db.sqlite3');
    }

    $this->dbConnection->setAttribute(\PDO::ATTR_ERRMODE, \PDO::ERRMODE_EXCEPTION);

    return $this->dbConnection;
  }

  /**
   * Select data from a given table with some parameters
   * @param String $table
   * @param String $fields
   * @param String $where
   * @param Array $params
   * @param String $order
   * @param String $limit
   * @return Array
   */
  public function select($table, $fields = "*", $where = null, array $params = null, $order = null, $limit = null) {
    $db = $this->dbConnection;

    if ($where > 1) {
      $where = join(" = ? AND ", array_values($where));
    }

    $sql = "SELECT " . $fields . " FROM " . $table . ($where ? " WHERE " . $where . " = ?" : "") .
      ($order ? " ORDER BY " . $order . " DESC" : "") . ($limit ? " LIMIT " . $limit : "");

    $query = $db->prepare($sql);
    $params ? $query->execute($params) : $query->execute();

    $result = $query->fetchAll(\PDO::FETCH_ASSOC);

    if ($result) {
      return $result;
    }

    return null;
  }

  /**
   * Insert data into a given table with some data
   * @param String $table
   * @param Array $data
   */
  public function insert($table, array $data) {
    $db = $this->dbConnection;

    $fields = join(", ", array_keys($data));
    $values = join(", ", array_values($data));
    $params = explode(", ", $values);

    $count = count($data);

    $sql = "INSERT INTO " . $table . " (" . $fields . ") VALUES (";
    for ($i = 0; $i < $count; $i++) {
      $i === $count-1 ? $sql .= "?" : $sql .= "?, ";
    }
    $sql .= ")";

    $query = $db->prepare($sql);
    $query->execute($params);
  }

  public function delete($table, array $where = null, array $params) {
    $db = $this->dbConnection;

    if ($where > 1) {
      $where = join(" = ? AND ", array_values($where));
    }

    $sql = "DELETE FROM " . $table . ($where ? " WHERE " . $where . " = ?" : "");

    $query = $db->prepare($sql);

    $query->execute($params);

    return $query->rowCount() ? true : false;
  }
}