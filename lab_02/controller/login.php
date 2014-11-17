<?php

namespace Controller;

require_once 'model/login.php';
require_once 'view/message.php';
require_once 'controller/message.php';

class Login {
  private $model;
  private $view;
  private $msgController;

  /**
   * @param \View\Login $view
   * @return Void
   */
  function __construct(\View\Login $view) {
    $this->model = new \Model\Login();
    $this->view = $view;
    $msgView = new \View\Message();
    $this->msgController = new \Controller\Message($msgView);
  }

  /**
   * "Router", decides which page to be shown
   */
  public function showPage() {
    if ($this->view->userWantsToLogout()) {
      return $this->logout();
    }
    if ($this->model->checkUser()) {
      return $this->msgController->messages();
    }
    return $this->login();
  }

  /**
   * Our login action, will login a user if to be true
   * @return View?
   */
  public function login() {
    $user = $this->view->getUserField();
    $password = $this->view->getPasswordField();

    if ($this->view->userWantsToLogin()) {
        // Set stuff
        $this->model->login($user, $password);

        // Then show our new view.
        return $this->view->redirectTo('index.php');
    }
    // Else redirect
    return $this->view->showLogin();
  }

  /**
   * Just a logout action that redirects us after logout.
   */
  public function logout() {
    $this->model->logout();
    $this->view->redirectTo('index.php');
  }
}