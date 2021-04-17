const ASRcanva = document.getElementById('ASRgraph');
const OCRcanva = document.getElementById("OCRgraph");


const data = {
    labels: [],
    datasets: [{
      label: '',
      backgroundColor: 'rgb(255, 99, 132)',
      borderColor: 'rgb(255, 99, 132)',
      data: [],
    }]
};


const config = {
    type: 'line',
    data: {...data},
    options: {}
  };


var ASRchart = new Chart(ASRcanva, {...config});
var OCRchart = new Chart(OCRcanva, {...config});

function updateGraphASR(label, data, title) {
    ASRchart.data.labels = label;
    ASRchart.data.datasets.forEach((dataset) => {
        dataset.label = title;
        dataset.data = data;
    });
    ASRchart.update();
}

function updateGraphOCR(label, data, title) {
    OCRchart.data.labels = label;
    OCRchart.data.datasets.forEach((dataset) => {
        dataset.label = title;
        dataset.data = data;
    });
    OCRchart.update();
}


function clickHandlerOCR(evt) {
    var firstPoint = OCRchart.getElementAtEvent(evt)[0];
    if (firstPoint) {
        var label = OCRchart.data.labels[firstPoint._index];
        console.log(OCRchart.data.labels)
        player.seekTo(label);
    }
}

function clickHandlerASR(evt) {
    var firstPoint = ASRchart.getElementAtEvent(evt)[0];
    if (firstPoint) {
        var label = ASRchart.data.labels[firstPoint._index];
        console.log(ASRchart.data.labels)

        player.seekTo(label);
    }
}

ASRcanva.onclick = clickHandlerASR;
OCRcanva.onclick = clickHandlerOCR;

// function removeData() {
//     chart.data.labels.pop();
//     chart.data.datasets.forEach((dataset) => {
//         dataset.data.pop();
//     });
//     chart.update();
// }
