$(document).ready(function() {
    $('#dataTable').DataTable({
        "paging": false,
        "searching": false,
    });

    var c = $('[name=enableExistingLetters]');
    var d = $('[name=existingLetters]');
    if (c.prop("checked") === true) {
        d.removeAttr('disabled');
    } else {
        d.attr('disabled', 'disabled');
    }
    c.change(function() {
        if (c.prop("checked") === true) {
            d.removeAttr('disabled');
        } else {
            d.attr('disabled', 'disabled');
        }
    });
});