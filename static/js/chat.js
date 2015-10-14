/**
 * Created by kodiers on 14/10/15.
 * Chat JS file.
 */
$(document).ready(function () {
    // After document ready open WebSocket connection
    scroll_chat_window();
    var chat_id = $('#idChat').val();
    var sender = $('#idSender').val();
    var host = 'ws://localhost:8888/send_async_message/' + chat_id + '/';
    var ws = new WebSocket(host);
    ws.onopen = function (e) {
        console.log('WebSocket created');
    };
    ws.onclose = function (e) {
        console.log('WebSocket closed');
    };
    ws.onmessage = function (e) {
        var response = JSON.parse(e.data);
        //console.log(response);
        var html_string = response['text'];
        //console.log(html_string);
        if (response['sender'] === sender) {
            html_string = '<p class="sender">' + sender + ' ' + response['datetime'] + '</p>' +
                '<p class="chat_message">' + response['text'] + '</p>';
        } else {
            html_string = '<p class="receiver">' + response['sender'] + ' ' + response['datetime'] + '</p>' +
                '<p class="chat_message">' + response['text'] + '</p>';
        }
        //console.log(html_string);
        $("div.conversation").append(html_string);
        scroll_chat_window();
    };
    $('#idSendMessageForm').on('submit', function (event) {
        event.preventDefault();
    });
    $('#idSend').click(function (event) {
        var text = $('#idText').val();
        var msg = JSON.stringify({'sender': sender, 'text': text});
        sendMessage(ws, msg);
        $('#idText').val('');
    })

});

function scroll_chat_window() {
    $("div.conversation").scrollTop($("div.conversation")[0].scrollHeight);
}

function sendMessage(ws, msg) {
    waitForSocketConnection(ws, function () {
        console.log('Sending message');
        ws.send(msg);
    });
};

function waitForSocketConnection(socket, callback) {
    setTimeout(function () {
        if(socket.readyState === 1) {
            if (callback !== undefined) {
                callback();
            }
            return;
        } else {
            waitForSocketConnection(socket, callback);
        }
    }, 5);
}