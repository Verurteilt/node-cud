var io = require('socket.io').listen(8080),
	http = require('http'),
	querystring = require('querystring');

io.sockets.on('connection', function(socket){
	socket.on('nuevo-tweet', function(info){
		var values  = querystring.stringify(info);
		var opt = {
			hostname: 'localhost',
			port: '8000',
			path: '/new-tweet/',
			method: "POST",
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
				'Content-Length': values.length
			}
		};
		var request = http.request(opt, function(res){
			res.setEncoding('utf8');
			res.on('data', function(data){
				console.log("DATA de regreso", data);
				io.sockets.emit('append-tweet', data);
			});
		});
		request.write(values);
		request.end();
	});
});