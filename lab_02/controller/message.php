<?php

namespace Controller;

require_once 'model/message.php';
require_once 'view/message.php';

class Message {
  private $model;
  private $view;

  /**
   * @param \View\Message $view
   * @return Void
   */
  function __construct(\View\Message $view) {
    $this->model = new \Model\Message();
    $this->view = $view;
  }

  /**
   * Our "messages" action, a bunch of stuff is decided.
   * @return VIEW?
   */
  public function messages() {
    if ($this->view->userWantsToAddMsg() && $this->isAjax()) {
      $message = $this->view->getMessageField();
      $user = $_SESSION["user"];
      return $this->addMessage($user, $message);
    }
    if ($this->view->userWantsToGetMessages() && $this->isAjax()) {
      return $this->getMessages();
    }
    return $this->view->showMessages();
  }

  /**
   * Get all the messages from the model
   * @return Array
   */
  public function getMessages() {
    echo json_encode($this->model->getMessages());
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