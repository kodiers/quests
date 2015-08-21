/**
 * Created by kodiers on 21/08/15.
 */
function prevent_refresh_team_leave(team_pk) {

    var form_id = '#id_leaveTeamForm' + team_pk;

    $(form_id).on('submit', function (event) {
        // Prevent form refresh
        event.preventDefault();
        // Delete team
        leave_team(team_pk);
    })
}


function leave_team(team_pk) {
    // Send AJAX POST request to leave_team endpoint

    var csrfmiddlewaretoken = $.cookie('csrftoken'); // Get csrf token (need jQuery cookie plugin)
    //var EventId = '#delEventID' + event_pk; // form task id parameter
    //var task_val = $(EventId).val(); // get value of form

    // Send post request
    $.ajax({
        url: '/leave_team/',
        type: 'post',
        data: {
            pk: team_pk,
            csrfmiddlewaretoken: csrfmiddlewaretoken
        },
        success: function (response) {
            //console.log(response);

            // close modal
            var button_id = 'id_leaveTeamCloseButton' + team_pk;
            document.getElementById(button_id).click();

            // if report show debug in console
            if (response.code != 1) {
                console.log('Some error in AJAX request');
            }
            else {
                // delet div with deleted task
                var div_id = '#team' + team_pk;
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