/**
 * Created by kodiers on 27/08/15.
 */

function start_task (task_id) {
    var csrfmiddlewaretoken = $.cookie('csrftoken'); // Get csrf token (need jQuery cookie plugin)

    $("#playTask" + task_id).modal('show');
    $.ajax({
        url: "/start_task/",
        type: "post",
        data: {
            csrfmiddlewaretoken: csrfmiddlewaretoken,
            pk: task_id
        },
        success: function (response) {
            console.log(response);
            if (response.code == '1') {
                $("#playTask" + task_id).modal('show');
            }
        },
        error: function(xhr, errmsg, err) {
            $('#id_error').html("<p class='error'>" + errmsg + "</p>")
        }
    });
}


