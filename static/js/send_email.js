/**
 * Created by kodiers on 22/10/15.
 * Script for send message from contacts feedback form.
 */
$(document).ready(function () {
    $('#idSendMessage').on('submit', function (event) {
        event.preventDefault();
        $('#result').html('');
        var csrfmiddlewaretoken = $.cookie('csrftoken');
        var SenderName = $('#idName').val();
        var SenderEmail = $('#idEmail').val();
        var SenderMessage = $('#idMessage').val();
        var token = $('#token').val();
        var canSend = true;
        if (SenderEmail === '') {
            $('#result').append('<span class="error">Enter your email please!</span>');
            canSend = false;
        } else if (SenderName === '') {
            $('#result').append('<span class="error">Enter your name please!</span>');
            canSend = false;
        } else if (SenderMessage == '') {
            $('#result').append('<span class="error">Enter your message please!</span>');
            canSend = false;
        }
        if (canSend) {
            $.ajax({
                url: '/pages/send_email/',
                type: 'post',
                data: {
                    csrfmiddlewaretoken: csrfmiddlewaretoken,
                    token: token,
                    SenderName: SenderName,
                    SenderEmail: SenderEmail,
                    SenderMessage: SenderMessage
                },
                success: function (response) {
                    if (response.data === 1) {
                        $('#result').append('<span class="message">Your message was successfully sent!</span>');
                        $('#idName').val('');
                        $('#idEmail').val('');
                        $('#idMessage').val('');
                    } else {
                        $('#result').append('<span class="error">Error the sent your message!</span>');
                    }
                },
                error: function (xhr, errmsg, err) {
                    $('#result').html("<p class='error'>" + errmsg + "</p>");
                }
            });
        }
    });
});