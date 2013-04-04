function connect() {
    var ws = new WebSocket("ws://" + server_host + "/socket");
    ws.onmessage = function (event) {
        var data = eval('(' + event.data + ')');

        $("span#online").html(data.online);

        var action = data.action;

        if (action == "add") {

            addToPrivateChat(data.user, {});

            if (mod_status == 1) {
                var del_link = ' <a href="javascript:void(0)" onclick="removeMessage(' + data.line + ');"><span style="float:left;" class="ui-icon ui-icon-trash"></span></a>';
                var del_all_link = ' <a href="javascript:void(0)" onclick="removeAllMessages(\'' + data.user + '\');"><span style="float:left;" class="ui-icon ui-icon-alert"></span></a>';
                var ban_link = ' <a href="javascript:void(0)" onclick="banUser(\'' + data.user + '\');"><span style="float:left;" class="ui-icon ui-icon-circle-minus"></span></a>';
            } else {
                var del_link = '';
                var del_all_link = '';
                var ban_link = '';
            }

            var msg_link = ' <a href="javascript:void(0)" onclick="sendPvtMsg(\'' + data.user + '\');"><span style="float:left;" class="ui-icon ui-icon-comment"></span></a>';

            html = $('<div class="message" id="' + data.line + '"><b><u>' + data.user + ':</u></b>  ' + data.val + '<span class="right_float">' + msg_link + del_link + del_all_link + ban_link + '</span></div>');
            $("div#chat").append(html);
            scrollChat();
        }

        if (action == "remove") {
            $("div#" + data.val).remove();
            scrollChat();
        }


    }

    ws.onclose = function () {
        $("div#chat").append($('<b>Connection Terminated</b><br/><br/>'));
        $("input#connect_btn").show();
    }

    $("div#chat").append($('<b>Connection Stabilished</b><br/><br/>'));
    $("input#connect_btn").hide();
}

function postMessage() {
    var msg = $("#message").val();
    var token = $("input#csrf_token").val()

    $.ajax({
        url: 'http://' + server_host + '/push',
        method: 'POST',
        data: {
            action: 'add',
            csrf_token: token,
            val: msg
        },
        success: function (re) {
            console.log("Data pushed");
            $("#message").val('')
        }
    });
}

function banUser(username) {
    if (!confirm('You are about to ban ' + username)) {
        return false;
    }

    var token = $("input#csrf_token").val();

    $.ajax({
        url: 'http://' + server_host + '/push',
        method: 'POST',
        data: {
            'action': 'ban',
            'csrf_token': token,
            'val': username
        },
        success: function (re) {
            console.log("Data pushed");
            $("#message").val('')
        }
    });
}

function removeAllMessages(username) {
    if (!confirm('You are about to remove all messages from ' + username)) {
        return false;
    }

    var token = $("input#csrf_token").val();

    $.ajax({
        url: 'http://' + server_host + '/push',
        method: 'POST',
        data: {
            'action': 'remove_all',
            'csrf_token': token,
            'val': username
        },
        success: function (re) {
            console.log("Data pushed");
            $("#message").val('')
        }
    });
}

function sendPvtMsg(username) {
    alert(username);
}

function removeMessage(id) {
    if (!confirm('You are about to delete this message!')) {
        return false;
    }

    var token = $("input#csrf_token").val();

    $.ajax({
        url: 'http://' + server_host + '/push',
        method: 'POST',
        data: {
            'action': 'remove',
            'csrf_token': token,
            'val': id
        },
        success: function (re) {
            console.log("Data pushed");
            $("#message").val('')
        }
    });
}

function scrollChat() {
    $("div#chat").scrollTop($("div#chat").height() + ($("div.message").length * 40));
}

function addToPrivateChat(username, data) {

    if (window.tabs.find('div#' + username).length < 1) {
        // user tab doesn't exist - create it
        var ul = tabs.find("ul");
        $("<li><a href='#" + username + "'>" + username + "</a></li>").appendTo(ul);
        $("<div id='" + username + "'></div>").appendTo(tabs);
        tabs.tabs("refresh");
    }

}

