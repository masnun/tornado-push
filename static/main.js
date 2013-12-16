$(document).ready(function () {

    window.tabs = $("#tabs").tabs(
        {
            activate: function (event, ui) {
                var tabId = ui.newPanel[0].id;
                if (tabId == 'chat') {
                    window.private_chat = null;
                } else {
                    window.private_chat = tabId;
                }

            }
        }
    );

    $("#message").keyup(function (event) {
        if (event.keyCode == 13) {
            postMessage();
        }
    });


    $('.dialog-hidden').hide();
    connect();
});