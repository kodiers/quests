/**
 * Created by kodiers on 07/09/15.
 */
function prevent_refresh_complete(event_id) {
    $('#completeEventForm').on('submit', function (event) {
        event.preventDefault();
        complete_event(event_id);
    })
}

function complete_event(event_id){
    var csrfmiddlewaretoken = $.cookie('csrftoken'); // Get csrf token (need jQuery cookie plugin)
    $.ajax({
        url: "/complete_event/",
        type: "post",
        data: {
            csrfmiddlewaretoken: csrfmiddlewaretoken,
            pk: event_id
        },
        success: function (response) {
            console.log(response);
            location.reload();
        }
    })

}