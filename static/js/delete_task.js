/**
 * Created by kodiers on 13/08/15.
 */
function prevent_refresh(task_pk) {

    var form_id = '#id_deleteTaskForm' + task_pk;

    $(form_id).on('submit', function (event) {
        // Prevent form refresh
        event.preventDefault();
        // Delete task
        delete_task(task_pk);
    })
}

function delete_task (task_pk) {
    // Send AJAX POST request to delete_task endpoint

    var csrfmiddlewaretoken = $.cookie('csrftoken'); // Get csrf token (need jQuery cookie plugin)
    var taskId = '#delTaskID' + task_pk; // form task id parameter
    var task_val = $(taskId).val(); // get value of form

    // Send post request
    $.ajax({
        url: '/delete_task/',
        type: 'post',
        data: {
            pk: task_val,
            csrfmiddlewaretoken: csrfmiddlewaretoken
        },
        success: function (response) {
            //console.log(response);

            // close modal
            var button_id = 'id_delcloseButton' + task_pk;
            document.getElementById(button_id).click();

            // if report show debug in console
            if (response.code != 1) {
                console.log('Some error in AJAX request');
            }
            else {
                // delet div with deleted task
                var div_id = '#task' + task_pk;
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
