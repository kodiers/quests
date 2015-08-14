/**
 * Created by kodiers on 14/08/15.
 */

function edit_task (task_pk) {
    // Send AJAX POST request to edit_task endpoint

    var csrfmiddlewaretoken = $.cookie('csrftoken'); // Get csrf token (need jQuery cookie plugin)

    // Get value from form
    var taskTitle = $('#id_editTaskTitle' + task_pk).val();
    var taskDescription = $('#id_editTaskDescription' + task_pk).val();
    var taskMaplink = $('#id_editMapLink' + task_pk).val();
    var taskTime = $('#id_editTaskTime' + task_pk).val();
    var taskScore = $('#id_editTaskScore' + task_pk).val();
    var taskAnswer = $('#id_editTaskAnswer' + task_pk).val();
    var taskEvent = $('#id_editTaskEvent' + task_pk).val();

    var taskPlacePk = $('#id_editTaskPlacePk' + task_pk).val();
    var taskCountry = $('#id_editTaskCountry' + task_pk).val();
    var taskCity = $('#id_editTaskCity' + task_pk).val();
    var taskStreet = $('#id_editTaskStreet' + task_pk).val();
    var taskLon = $('#id_editTaskLon' + task_pk).val();
    var taskLat = $('#id_editTaskLat' + task_pk).val();

    var taskHint = $('#id_editTaskHint' + task_pk).val();
    var taskHintPk = $('#id_editTaskHintPk' + task_pk).val();

    //var tasklist = $('#id_taskList');

    //Send post request

    $.ajax({
        url: "/edit_task/",
        type: "post",
        data: {
            title: taskTitle,
            description: taskDescription,
            map_link: taskMaplink,
            time: taskTime,
            score: taskScore,
            answer: taskAnswer,
            event: taskEvent,
            country: taskCountry,
            city: taskCity,
            street: taskStreet,
            lon: taskLon,
            lat: taskLat,
            hint: taskHint,
            csrfmiddlewaretoken: csrfmiddlewaretoken,
            placepk: taskPlacePk,
            hintpk: taskHintPk
        },

        success: function(response) {
            // add new task to tasklist without page refresh

            //Clear modal form
            $('.modal').on('hidden.bs.modal', function () {
                $(this).find('form')[0].reset();
            });
            // Close modal
            var button_id = 'id_editCloseButton' + task_pk;
            document.getElementById(button_id).click();
            // Reload page to show changes
            location.reload();
        },
        error: function(xhr, errmsg, err) {
            $('#id_error').html("<p class='error'>" + errmsg + "</p>")
        }

    });
}
