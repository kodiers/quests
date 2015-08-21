/**
 * Created by kodiers on 21/08/15.
 */
function prevent_refresh_unregister(event_pk) {

    var form_id = '#id_unregisterForm' + event_pk;

    $(form_id).on('submit', function (event) {
        // Prevent form refresh
        event.preventDefault();
        // Delete team
        unregister(event_pk);
    })
}


function unregister(event_pk) {
    // Send AJAX POST request to unregister_event endpoint

    var csrfmiddlewaretoken = $.cookie('csrftoken'); // Get csrf token (need jQuery cookie plugin)
    //var EventId = '#delEventID' + event_pk; // form task id parameter
    //var task_val = $(EventId).val(); // get value of form

    // Send post request
    $.ajax({
        url: '/unregister_event/',
        type: 'post',
        data: {
            pk: event_pk,
            csrfmiddlewaretoken: csrfmiddlewaretoken
        },
        success: function (response) {
            //console.log(response);

            // close modal
            var button_id = 'id_unregisterCloseButton' + event_pk;
            document.getElementById(button_id).click();

            // if report show debug in console
            if (response.code != 1) {
                console.log('Some error in AJAX request');
            }
            else {
                // delet div with deleted task
                var div_id = '#reg_event' + event_pk;
                $(div_id).remove();
                // reload to show changes
                location.reload();
            }

        },
        error: function(xhr, errmsg, err) {
            $('#id_error').html("<p class='error'>" + errmsg + "</p>")
        }

    })
}