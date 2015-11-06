/**
 * Created by kodiers on 05/11/15.
 * This script add mask to duration field and shows showsCongrats modal.
 */
$(document).ready(function () {
    $('#id_duration').mask('0d 00:00:00');
    $('#showCongrats').modal('show');
})