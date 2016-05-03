/**
 * Created by kodiers on 26/04/16.
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
        url: "/complete_event_organizer/",
        type: "post",
        data: {
            csrfmiddlewaretoken: csrfmiddlewaretoken,
            pk: event_id
        },
        success: function (response) {
            if (response.code == '1') {
                console.log(response);
                location.reload();
            } else {
                console.log(response);
                location.reload();
                $("p.error").text("Error then completing event");
            }
        }
    })

}