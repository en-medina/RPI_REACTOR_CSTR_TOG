const script = document.currentScript;

document.addEventListener("DOMContentLoaded", function(){
	const ipaddr = script.getAttribute('ipaddr');
	const port = script.getAttribute('port');
	const url = String().concat('http://', ipaddr, ':', port,'/');
	const socket = io.connect(url);
	let limitatorButton = document.querySelector('#limitator-button'); 
	let systemButton = document.querySelector('#system-button');
	let systemDelayField = document.querySelector('#state-timer');
	let systemState = document.querySelector('#system-state');

	socket.on('update_limit_state', function(message){
		let updateLimitState = JSON.parse(message);
		limitatorButton.setAttribute('state', updateLimitState['state'].toString());
		if(updateLimitState['state']){
			limitatorButton.innerHTML = 'Desactivar limitador';
		}
		else{
		  limitatorButton.innerHTML = 'Activar limitador';	
		}		
	});

	limitatorButton.addEventListener("click", function() {
		let updateLimitState = !Boolean(Number(limitatorButton.getAttribute('state')));
		let jsonToUpload = JSON.stringify({'state': updateLimitState});
		socket.emit('change_limit_state', jsonToUpload);
		});

	socket.on('update_system_state', function(message) {
		let updateSystemState = JSON.parse(message);
		systemButton.setAttribute('state', updateSystemState['state'].toString());
		systemState.setAttribute('state', updateSystemState['state'].toString());
		if(updateSystemState['state']){
			systemButton.innerHTML = 'Apagar sistema';
			systemState.innerHTML = 'Encendido';
		}
		else{
		  systemButton.innerHTML = 'Encender sistema';	
			systemState.innerHTML = 'Apagado';
		}
	});


	systemButton.addEventListener("click", function() {
		let delay = Number(systemDelayField.value);
		systemDelayField.value ="";
		let state = !Boolean(Number(systemButton.getAttribute('state')));
		console.log(state);
		let jsonToUpload = JSON.stringify({'delay': delay, 'state':state});
		socket.emit('change_system_state', jsonToUpload);
		});
 });