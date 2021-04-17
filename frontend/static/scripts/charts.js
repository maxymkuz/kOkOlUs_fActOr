const canva = document.getElementById('graph');


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
    data,
    options: {}
  };

var chart = new Chart(canva, config);


function updateGraph(label, data, title) {
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


function clickHandler(evt) {
    var firstPoint = chart.getElementAtEvent(evt)[0];
    if (firstPoint) {
        var label = chart.data.labels[firstPoint._index];
        var value = chart.data.datasets[firstPoint._datasetIndex].data[firstPoint._index];
        move
    }
}

canva.onclick = clickHandler;

// function removeData() {
//     chart.data.labels.pop();
//     chart.data.datasets.forEach((dataset) => {
//         dataset.data.pop();
//     });
//     chart.update();
// }
