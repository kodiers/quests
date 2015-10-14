/**
 * Created by kodiers on 14/10/15.
 */

$(document).ready(function () {
    var form_checked = false;
    $('#idSendMessageForm').on('submit', function (event) {
        if (!form_checked) {
            event.preventDefault();
            var receiver = $('#idReceiver').val();
            var csrfmiddlewaretoken = $.cookie('csrftoken'); // Get csrf token (need jQuery cookie plugin)
            $.ajax({
                url: '/messages/check_username/',
                type: 'post',
                data: {
                    csrfmiddlewaretoken: csrfmiddlewaretoken,
                    receiver: receiver
                },
                success: function (response) {
                    console.log(response);
                    if (response.code == 2) {
                        $('#modal_error').empty();
                        $('#modal_error').append('<span class="error">User with this username not found!</span>');
                    } else if (response.code == 1) {
                        $('#modal_error').empty();
                        $('#modal_error').append('<span class="message">Username is correct!</span>');
                        form_checked = true;
                        $('#idSendMessageForm').submit();
                        console.log('Form should be submitted');
                        //location.reload();
                        //$('#SendMessageModal').dialog("close");
                    }
                }
            })
        }
    })
});
