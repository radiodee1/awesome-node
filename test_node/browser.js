$(document).ready(function() {

//$(window).load(function() {
    
    $(this).on('keypress', function(event) {
        
        var x = document.getElementById("frame_inner");
        var win = (x.contentWindow || x.contentDocument);
    //if (y.document)y = y.document;
    //y.body.style.backgroundColor = "red";
        var content = win.document.getElementById("contenedor");

        content.focus();
        
        if (event.keyCode == 13) { //carriage return
            console.log('hi.');
        }
        url_z ='*';// 'http://textadventures.co.uk/'
        var char = String.fromCharCode(event.keyCode);
        win.postMessage("west", url_z);
        //console.log(event.keyCode);
        
        console.log(char);
    });
})
