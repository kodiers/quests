/**
 * Created by kodiers on 16/09/15.
 */
function message_queue() {
    $('#newMessageForm').on('submit', function (event) {
        event.preventDefault();
        var username = $('#to_user').val();
        var text = $('#text').val();
        if (check_username(username)) {
            send_message(username, text);
        } else {
            $('#error').html("<p class='error'>User with this username not found</p>")
        }

    })
}

function check_username (username) {
    var csrfmiddlewaretoken = $.cookie('csrftoken'); // Get csrf token (need jQuery cookie plugin)
    $.ajax({
        url: "/check_username/",
        type: "post",
        data: {
            csrfmiddlewaretoken: csrfmiddlewaretoken,
            username: username
        },
        success: function (response) {
            if (response.code == 1) {
                return true;
            }
        }
    })
}

function send_message (username, text){
    var csrfmiddlewaretoken = $.cookie('csrftoken'); // Get csrf token (need jQuery cookie plugin)

    $.ajax({
        url: "/send_new_message/",
        type: "post",
        data: {
            csrfmiddlewaretoken: csrfmiddlewaretoken,
            username : username,
            text: text
        },
        success: function (response) {
            console.log(response);
        }
    })
}