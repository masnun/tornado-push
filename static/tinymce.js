// Tiny MCE
$().ready(function() {

    $('textarea#message').tinymce({
        // Location of TinyMCE script
        script_url : '/static/tinymce/jscripts/tiny_mce/tiny_mce.js',

        // General options
        theme : "advanced",
        plugins : "emotions",

        // Theme options
        theme_advanced_buttons1 : "bold,italic,underline,emotions",
        theme_advanced_toolbar_location : "top",
        theme_advanced_toolbar_align : "left",
        theme_advanced_statusbar_location : "none"
    });

});
