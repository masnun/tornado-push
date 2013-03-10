<?php
/**
 * Author: Abu Ashraf Masnun
 * URL: http://masnun.me
 */


require_once 'Utils.php';

class AfChatWidget extends WP_Widget
{
    public function __construct()
    {
        parent::__construct(
            'afchat_widget', // Base ID
            'AfChat Widget', // Name
            array('description' => __('Afchat Widget'), 'text-domain') // Args
        );

    }

    public function widget($args, $instance)
    {

        extract($args);
        $title = apply_filters('widget_title', $instance['title']);

        echo $before_widget;
        if (!empty($title))
            echo $before_title . $title . $after_title;

        //WIDGET START

        $wpUser = wp_get_current_user();
        if ($wpUser->ID > 0) {
            //user is logged in
            //var_dump($wpUser);
            if (array_key_exists('moderate_comments', $wpUser->allcaps)) {
                $isMod = (int)$wpUser->allcaps['moderate_comments'];
            } else {
                $isMod = 0;
            }

            $token = getUserAuthToken("http://localhost:8888/auth", "secret", $wpUser->user_login, $isMod);

            echo '<iframe width="200px" height="300px" src="http://localhost:8888/?csrf_token=' . $token . '"></iframe>';

        } else {
            echo 'You must be logged into wordpress to chat!';
        }

        //END WIDGET

        echo $after_widget;

    }

    public function update($new_instance, $old_instance)
    {
        $instance = array();
        $instance['title'] = strip_tags($new_instance['title']);

        return $instance;

    }

    public function form($instance)
    {
        if (isset($instance['title'])) {
            $title = $instance['title'];
        } else {
            $title = __('AF Chat', 'text_domain');
        }
        ?>
        <p>
            <label for="<?php echo $this->get_field_id('title'); ?>"><?php _e('Title:'); ?></label>
            <input class="widefat" id="<?php echo $this->get_field_id('title'); ?>"
                   name="<?php echo $this->get_field_name('title'); ?>" type="text"
                   value="<?php echo esc_attr($title); ?>"/>
        </p>
    <?php
    }


}