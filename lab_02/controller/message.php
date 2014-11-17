<?php

namespace Controller;

require_once 'model/message.php';
require_once 'view/message.php';

class Message {
  private $model;
  private $view;

  function __construct(\View\Message $view) {
    $this->model = new \Model\Message();
    $this->view = $view;
  }

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

  public function getMessages() {
    echo json_encode($this->model->getMessages());
  }

  public function addMessage($user, $message) {
    echo json_encode($this->model->addToDB($user, $message));
  }

  public function isAjax() {
    return isset($_SERVER['HTTP_X_REQUESTED_WITH'])
      && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) == 'xmlhttprequest';
  }
}