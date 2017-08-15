$(document).ready(function() {
    $(this).on('keypress', function(event) {
        if (event.keyCode == 13) { //carriage return
            console.log('hi.');
        }
    });
})
