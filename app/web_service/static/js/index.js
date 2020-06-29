const script = document.currentScript;

document.addEventListener("DOMContentLoaded", function(){
	const ipaddr = script.getAttribute('ipaddr');
	const port = script.getAttribute('port');
	const url = String().concat('http://', ipaddr, ':', port,'/');
	const socket = io.connect(url);

	socket.on('update_information', function(message){
		let data = JSON.parse(message);
		for(key in data){
				document.querySelector('#' + key).innerHTML = data[key][0].toString();
		}
	});
 });