/**
 * Created by kodiers on 25/08/15.
 */
function delete_photo(photo_pk) {
    // Send AJAX POST request to delete_photo endpoint

    var csrfmiddlewaretoken = $.cookie('csrftoken'); // Get csrf token (need jQuery cookie plugin)

    // Send post request
    $.ajax({
        url: '/delete_photo/',
        type: 'post',
        data: {
            pk: photo_pk,
            csrfmiddlewaretoken: csrfmiddlewaretoken
        },
        success: function (response) {

            // if report show debug in console
            if (response.code != 1) {
                console.log('Some error in AJAX request');
            }
            else {
                // reload to show changes
                location.reload();
            }

        },
        error: function(xhr, errmsg, err) {
            $('#id_error').html("<p class='error'>" + errmsg + "</p>")
        }

    })
}