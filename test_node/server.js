var http = require('http');
var url = require('url');
var fs = require('fs');
//var keydown = require('keydown');
//var kd = keydown(['q']);
//var createKeyboard = require('crtrdg-keyboard');
//var keyboard = createKeyboard();

http.createServer(function (req, res) {
    var url_parts = url.parse(req.url, true);
    var query = url_parts.query;
    var page = '';
    page += '<head>';
    page += '<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>';
    //page += '<script type="text/javascript" src="browser.js"></script>';
    data_fs = fs.readFileSync('browser.js');
    page += '<script type="text/javascript">';
    page += data_fs.toString();
    page += '</script>';
    //console.log(data_fs.toString());
    
    
    page += '</head>';
    page += '<body>';
    url_z = 'http://textadventures.co.uk/games/play/5zyoqrsugeopel3ffhz_vq'
    page += '<iframe src="' + url_z +'" height=600 width=900 id="frame_inner"></iframe><br>'
    page += '<p>' + url_z + '</p>';
    
    
    if(url_parts.path == '/text') {
        page += '<p></p>';
    } else {
        page += '<p>Hello World</p>';
        page += '<p><a href="/text">Please, click me</a></p>';
    }

    page += "</body>";
    
    
    res.writeHead(200, {'Content-Type': 'text/html'});


    res.end(page);
}).listen(1337, '127.0.0.1');



//keyboard.on('keydown', function (key) {
//  console.log(key)
//})

console.log('Server running at http://127.0.0.1:1337/');
