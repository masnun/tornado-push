<?php
/*
Plugin Name: Anime Fushigi Chat
Plugin URI: http://vitzo.com
Description: Add afchat to the blog
Author: Abu Ashraf Masnun
Version: 1.0
Author URI: http://masnun.me
*/

// Require all the PHP
require_once 'AfChatWidget.php';


// Register function
add_action('widgets_init', 'register_afchat_widget');

// Register the actual widget
function register_afchat_widget()
{
    register_widget('AfChatWidget');
}