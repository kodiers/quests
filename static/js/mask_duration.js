/**
 * Created by kodiers on 05/11/15.
 * This script add mask to duration field and shows showsCongrats modal.
 */
$(document).ready(function () {
    $('#id_duration').mask('0d 00:00:00');
    $('#id_taskTime').mask('0ZZ', {translation: {'Z': {pattern: /[0-9]/, optional: true}}});
    $('#id_taskScore').mask('0Z', {translation: {'Z': {pattern: /[0-9]/, optional: false}}});
    var rowsEditTaskScore = document.getElementsByName("editTaskScore");
    for (var i = 0; i < rowsEditTaskScore.length; i++) {
        var idScore = '#' + rowsEditTaskScore[i].id;
        $(idScore).mask('0Z', {translation: {'Z': {pattern: /[0-9]/, optional: true}}});
    }
    var rowsEditTaskTime = document.getElementsByName("editTaskTime");
    for (var j = 0; j < rowsEditTaskTime.length; j++) {
        var idTime = '#' + rowsEditTaskTime[j].id;
        $(idTime).mask('0ZZ', {translation: {'Z': {pattern: /[0-9]/, optional: true}}});
    }
    $('#showCongrats').modal('show');
})