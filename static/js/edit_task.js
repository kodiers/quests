/**
 * Created by kodiers on 14/08/15.
 */
function edit_prevent_refresh(task_pk) {

    var form_id = '#id_editTaskForm' + task_pk;

    $(form_id).on('submit', function (event) {
        // Prevent form refresh
        event.preventDefault();
        // Edit task
        edit_task(task_pk);
    })
}

function edit_task (task_pk) {
    // Send AJAX POST request to edit_task endpoint

    var csrfmiddlewaretoken = $.cookie('csrftoken'); // Get csrf token (need jQuery cookie plugin)

    // Get value from form
    var taskTitle = $('#id_editTaskTitle' + task_pk).val();
    var taskDescription = $('#id_editTaskDescription' + task_pk).val();
    var taskTime = $('#id_editTaskTime' + task_pk).val();
    var taskScore = $('#id_editTaskScore' + task_pk).val();
    var taskAnswer = $('#id_editTaskAnswer' + task_pk).val();
    var taskEvent = $('#id_editTaskEvent' + task_pk).val();

    var taskPlacePk = $('#id_editTaskPlacePk' + task_pk).val();
    var taskCountry = $('#id_editTaskCountry' + task_pk).val();
    var taskCity = $('#id_editTaskCity' + task_pk).val();
    var taskStreet = $('#id_editTaskStreet' + task_pk).val();
    // Longtitude and latitude not used in this version
    //var taskLon = $('#id_editTaskLon' + task_pk).val();
    //var taskLat = $('#id_editTaskLat' + task_pk).val();

    var taskHint = $('#id_editTaskHint' + task_pk).val();
    var taskHintPk = $('#id_editTaskHintPk' + task_pk).val();

    console.log(taskStreet);

    //var tasklist = $('#id_taskList');

    //Send post request

    $.ajax({
        url: "/edit_task/",
        type: "post",
        data: {
            pk: task_pk,
            title: taskTitle,
            description: taskDescription,
            time: taskTime,
            score: taskScore,
            answer: taskAnswer,
            event: taskEvent,
            country: taskCountry,
            city: taskCity,
            street: taskStreet,
            //lon: taskLon,
            //lat: taskLat,
            hint: taskHint,
            csrfmiddlewaretoken: csrfmiddlewaretoken,
            placepk: taskPlacePk,
            hintpk: taskHintPk
        },

        success: function(response) {
            // edit task to tasklist without page refresh

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
