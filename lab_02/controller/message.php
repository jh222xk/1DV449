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
      if ($_SESSION["csrf_token"] === $_POST["csrf_token"]) {
        $message = $this->view->getMessageField();
        $message = trim(filter_var($message, FILTER_SANITIZE_STRING, FILTER_FLAG_STRIP_LOW));
        $user = $_SESSION["user"];
        return $this->addMessage($user, $message);
      } else {
        return $this->view->csrfError();
      }
    }
    elseif ($this->view->userWantsToGetMessages() && $this->isAjax()) {
      $data = $this->model->getMessages();
      $counter = 0;

      $last_ajax_call = isset($_GET['timestamp']) ? (int)$_GET['timestamp'] : null;
      $last_change_in_data_file = $this->model->getLastMessage();

      $last_change_in_data_file = (int)$last_change_in_data_file[0]["date"];

      while ($last_ajax_call == null || $last_change_in_data_file > $last_ajax_call) {
        usleep(10000);
        clearstatcache();

        $counter++;

        if($counter >= 29) {
          break;
        }
      }
      $result = array(
        'messages' => $data,
        'timestamp' => $last_change_in_data_file
      );
      $json = json_encode($result);
      echo $json;
    } else {
      return $this->view->showMessages();
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