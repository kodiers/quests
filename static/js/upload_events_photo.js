/**
 * Created by kodiers on 25/08/15.
 */
function prevent_refresh_eventphoto(event_pk) {

    var form_id = '#addEventPhotoForm' + event_pk;

    $(form_id).on('submit', function (event) {
        // Prevent form refresh
        event.preventDefault();
        upload_event(form_id);
    })
}

function upload_event(form_id) {
    // Send AJAX POST request to upload_photo endpoint with event parameter from form

    var data = new FormData($(form_id).get(0));
    var csrfmiddlewaretoken = $.cookie('csrftoken'); // Get csrf token (need jQuery cookie plugin)

    console.log('Form handled');

    $.ajax({
        url: '/upload_photo/',
        type: 'post',
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function (response) {
            if (response.code != 1) {
                console.log('Some error in AJAX request');
            } else {
                console.log('Uploaded');
                location.reload();
            }
        },
        error: function(xhr, errmsg, err) {
            $('#id_error').html("<p class='error'>" + errmsg + "</p>");
        }
    });
}