/**
 * Created by kodiers on 10/08/15.
 */

$('#id_addTaskForm').on('submit', function(event) {
    // Prevent form refresh
    event.preventDefault();
    if (checkEmpty()) {
        add_task();
        return true;
    } else {
        return false;
    }
})

function checkEmpty() {
    // Check if task title or task description is empty
    if (document.getElementById('id_taskTitle').value.length == 0)
    {
        $('#title_error').html("Enter title for task");
        $('#description_error').html("");
        return false;
    }
    if (document.getElementById('id_taskDescription').value.length == 0) {
        $('#title_error').html("");
        $('#description_error').html("Enter description");
        return false;
    }
    return true;
}

function add_task () {
    // Send AJAX POST request to add_task endpoint

    var csrfmiddlewaretoken = $.cookie('csrftoken'); // Get csrf token (need jQuery cookie plugin)

    // Get value from form
    var taskTitle = $('#id_taskTitle').val();
    var taskDescription = $('#id_taskDescription').val();
    var taskTime = $('#id_taskTime').val();
    var taskScore = $('#id_taskScore').val();
    var taskAnswer = $('#id_taskAnswer').val();
    var taskEvent = $('#id_taskEvent').val();

    var taskCountry = $('#id_taskCountry').val();
    var taskCity = $('#id_taskCity').val();
    var taskStreet = $('#id_taskStreet').val();
    // Longtitude and latitude not used in this version
    //var taskLon = $('#id_taskLon').val();
    //var taskLat = $('#id_taskLat').val();

    var taskHint = $('#id_taskHint').val();

    var tasklist = $('#id_taskList');

    //Send post request

    $.ajax({
        url: "/add_task/",
        type: "post",
        data: {
            title: taskTitle,
            description: taskDescription,
            time: taskTime,
            score: taskScore,
            answer: taskAnswer,
            event: taskEvent,
            country: taskCountry,
            city: taskCity,
            street: taskStreet,
            hint: taskHint,
            csrfmiddlewaretoken: csrfmiddlewaretoken
        },

        success: function(response) {
            // add new task to tasklist without page refresh

            //Clear modal form
            $('.modal').on('hidden.bs.modal', function () {
                $(this).find('form')[0].reset();
            });
            // Close modal
            document.getElementById('id_closeButton').click();
            // Reload page to show changes
            location.reload();
        },
        error: function(xhr, errmsg, err) {
            $('#modal_error').html("<p class='error'>" + errmsg + "</p>")
            $('#id_error').html("<p class='error'>" + errmsg + "</p>")
        }

    });
}
