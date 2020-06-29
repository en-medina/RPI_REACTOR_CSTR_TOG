const script = document.currentScript;

document.addEventListener("DOMContentLoaded", function(){
	const ipaddr = script.getAttribute('ipaddr');
	const port = script.getAttribute('port');
	const url = String().concat('http://', ipaddr, ':', port,'/');
	const socket = io.connect(url);
	let limitatorButton = document.querySelector('#limitator-button'); 

	function change_system_state(state){
		limitatorButton.setAttribute('state', updateLimitState['state'].toString());
		if(state){
			limitatorButton.innerHTML = 'Desactivar Limitador';
		}
		else{
		  limitatorButton.innerHTML = 'Activar Limitador';	
		}		
	}

	socket.on('update_limit_state', function(message){
		let updateLimitState = JSON.parse(message);
		change_system_state(updateLimitState['state'])
	});

	socket.on('update_system_state', function(message) {
		let updateLimitState = JSON.parse(message);
		limitatorButton.setAttribute('state', updateLimitState['state'].toString());
		if(updateLimitState['state']){
			limitatorButton.innerHTML = 'Desactivar Limitador';
		}
		else{
		  limitatorButton.innerHTML = 'Activar Limitador';	
		}
	});

	limitatorButton.addEventListener("click", function() {
		let updateLimitState = !Boolean(Number(limitatorButton.getAttribute('state')));
		let jsonToUpload = JSON.stringify({'state': updateLimitState});
		socket.emit('change_limit_state', jsonToUpload);
		});
 });