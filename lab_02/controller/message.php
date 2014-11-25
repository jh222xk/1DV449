<?php

namespace Controller;

require_once 'model/message.php';
require_once 'view/message.php';

class Message {
  private $model;
  private $view;
  private $login;

  /**
   * @param \View\Message $view
   * @return Void
   */
  function __construct(\View\Message $view) {
    $this->model = new \Model\Message();
    $this->view = $view;
    $this->login = new \Model\Login();
  }

  /**
   * Our "messages" action, a bunch of stuff is decided.
   * @return VIEW?
   */
  public function messages() {
    if ($this->view->userWantsToAddMsg() && $this->login->checkUser() && $this->isAjax()) {
      if ($_SESSION["csrf_token"] === $_POST["csrf_token"]) {
        $message = $this->view->getMessageField();
        $message = trim(filter_var($message, FILTER_SANITIZE_STRING, FILTER_FLAG_STRIP_LOW));
        $user = $_SESSION["user"];
        return $this->addMessage($user, $message);
      } else {
        return $this->view->csrfError();
      }
    }
    elseif ($this->view->userWantsToGetMessages() && $this->login->checkUser() && $this->isAjax()) {
      session_write_close();
      $timestamp = isset($_GET['timestamp']) ? (int)$_GET['timestamp'] : 0;
      $this->getMessages($timestamp);
    } else {
      return $this->view->showMessages();
    }
  }

  public function getMessages($timestamp) {
    set_time_limit(0);
    while (true) {
      $result = array();

      $result = $this->model->getLastMessage($timestamp);

      if(count($result) > 0) {
        $dbTime = (int)$result[0]["date"];
        echo json_encode(array('messages' => array_reverse($result), "timestamp" => $dbTime));
        break;
      }else{
        sleep(1);
        continue;
      }
    }
  }

  /**
   * A a message to the model
   * @return Array
   */
  public function addMessage($user, $message) {
    echo json_encode($this->model->addToDB($user, $message));
  }

  /**
   * Just a simple check to see if the request isAjax!
   * @return Boolean
   */
  public function isAjax() {
    return isset($_SERVER['HTTP_X_REQUESTED_WITH'])
      && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) == 'xmlhttprequest';
  }
}