/**
 * Created by kodiers on 11/04/16.
 */
function get_hint (task_id) {
    var csrfmiddlewaretoken = $.cookie('csrftoken');
    var divid = "#hint" + task_id;
    console.log(divid);
    $.ajax({
        url: "/get_hint/",
        type: "post",
        data: {
            csrfmiddlewaretoken: csrfmiddlewaretoken,
            pk: task_id
        },
        success: function (response) {
            console.log(response);
            if (response.code == 1) {
                $(divid).text(response.hint);
            } else {

                console.log('error');
                $(divid).text('No hint fo this task!');
            }
        }
    });
}
