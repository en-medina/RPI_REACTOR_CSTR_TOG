const script = document.currentScript;
document.addEventListener("DOMContentLoaded", function(){

	//Json information about the graph
	//labes: list('string')
	//data: list('float')
	//title: string
	const graphData = JSON.parse(script.getAttribute('data'));

	let canvasGraph = document.querySelector('#out_graphics').getContext('2d');
	let downloadButton = document.querySelector('#csv-button'); 
	let myChart = new	Chart(canvasGraph, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: graphData['labels'],
        datasets: [{
            label: graphData['title'],
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: graphData['data'],
						fill: false

        }]
    },
    // Configuration options go here
    options: {
      title:{
       display:true,
       text:graphData['title']
      },
			maintainAspectRatio: false,
			spanGaps: false,
			elements: {
				line: {
					tension: 0.4
				}
			},
			plugins: {
				filler: {
					propagate: false
				}
			},
			scales: {
				xAxes: [{
					ticks: {
						autoSkip: false,
						maxRotation: 0
					}
				}]
			}
    }
	});	

	function downloadData(xAxis,yAxis,name){
		let i=0;
		let csvContent = "value,time\n";
		for(i; i<xAxis.length; i++){
			csvContent += `${yAxis[i]},${xAxis[i]}\n`;
		}
		let hiddenElement = document.createElement('a');
		hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csvContent);
		hiddenElement.target = '_blank';
		hiddenElement.download = `${name}.csv`;
		hiddenElement.click();
	}
	downloadButton.addEventListener("click", function() {
			downloadData(graphData['labels'], graphData['data'], graphData['title']);
		});
 });