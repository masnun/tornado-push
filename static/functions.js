function connect() {
            var ws = new WebSocket("ws://" + server_host + "/socket");
            ws.onmessage = function (event) {
                var data = eval('(' + event.data + ')');

                $("span#online").html(data.online);

                var action = data.action;

                if (action == "add") {

                    if(mod_status == 1) {
                        var del_link = ' <a href="javascript:void(0)" onclick="removeMessage('+ data.line +');">x</a>';
                    } else {
                        var del_link = '';
                    }

                    html = $('<div class="message" id="' + data.line + '"><b><u>' + data.user + ':</u></b>  '+ data.val + '<span class="right_float">' + del_link + '</span></div>');
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
            var token =  $("input#csrf_token").val()

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


        function removeMessage(id) {
            var token =  $("input#csrf_token").val();

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
            $("div#chat").scrollTop( $("div#chat").height() + ($("div.message").length * 40)  );
        }