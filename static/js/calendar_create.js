/**
 * Created by kodiers on 20/08/15.
 */
$(function () {
    //$("#id_start_date").datepicker();
    $("#id_start_date").datetimepicker({
        format: 'Y-m-d H:i'
    });
    $("#id_end_date").datetimepicker({
        format: 'Y-m-d H:i'
    });
});