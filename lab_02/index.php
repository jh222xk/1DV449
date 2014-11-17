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

/*
 * If we need to hash a password just do that below.
 *
 * require_once 'model/login.php';
 * $model = new \Model\Login();
 * $pass = $model->hashPassword("asdasd");
 * var_dump($pass);
 */

// require_once 'model/message.php';

// $model = new \Model\Message();
// $model->getMessages();