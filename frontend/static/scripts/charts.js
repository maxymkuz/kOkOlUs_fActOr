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


var ASRchart = new Chart(ASRcanva, config);
var OCRchart = new Chart(OCRcanva, config);

function updateGraph(label, data, title, chart) {
    // console.log(label)
    // console.log(data)
    chart.data.labels = label;
    chart.data.datasets.forEach((dataset) => {
        dataset.label = title;
        dataset.data = data;
    });
    chart.update();
    // console.log(chart.data.labels)
    // console.log(chart.data.datasets)
}


function clickHandler(evt, chart) {
    var firstPoint = chart.getElementAtEvent(evt)[0];
    if (firstPoint) {
        var label = chart.data.labels[firstPoint._index];
        player.seekTo(label);
    }
}

ASRcanva.onclick = (e) => {clickHandler(e, ASRchart)};
OCRcanva.onclick = (e) => {clickHandler(e, OCRchart)};

// function removeData() {
//     chart.data.labels.pop();
//     chart.data.datasets.forEach((dataset) => {
//         dataset.data.pop();
//     });
//     chart.update();
// }
