<?php
require_once('controller/login.php');
require_once('view/login.php');

// Start our session
session_start();

// Create a login view
$view = new \View\Login();

// Setup our controller
$controller = new \Controller\Login($view);
$controller->showPage();

// require_once 'model/message.php';

// $model = new \Model\Message();
// $model->getMessages();