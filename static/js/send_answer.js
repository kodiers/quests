/**
 * Created by kodiers on 07/09/15.
 */
function prevent_refresh_answer(task_id){
    var form_id = '#answerForm' + task_id;
    $(form_id).on('submit', function (event) {
        event.preventDefault();
        send_answer(task_id);
    })
}

function send_answer(task_id) {

    var csrfmiddlewaretoken = $.cookie('csrftoken'); // Get csrf token (need jQuery cookie plugin)
    var taskAnswer = $('#id_answer' + task_id).val();

    console.log(taskAnswer);

    $.ajax({
        url: "/task_answer/",
        type: "post",
        data: {
            csrfmiddlewaretoken: csrfmiddlewaretoken,
            pk: task_id,
            answer: taskAnswer
        },
        success: function (response) {
            console.log(response);
            location.reload();
        }
    });
}