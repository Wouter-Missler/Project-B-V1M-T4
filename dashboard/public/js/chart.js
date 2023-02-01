const defaultOptions = {
    scales: {
        y: {
            beginAtZero: true,
            ticks: { color: "#C7D5E0" }
        },
        x: {
            ticks: { color: "#C7D5E0" }
        }
    }, // begin de y-as bij 0
    plugins: {
        legend: {
            labels: {
                color: "#C7D5E0",  // not 'fontColor:' anymore
            }
        }
    },
};

function createBarChart(data, canvasElement, options) {
    // functie om een bar chart te maken
    // data (array): de data die in de chart moet komen
    // canvasElement: het element waar de chart in moet komen
    // options (optioneel): de opties die de chart moet hebben

    // als er geen opties zijn meegegeven, maak dan een lege optie
    if (options == undefined) {
        options = defaultOptions;
    }

    console.log(options);

    var chart = new Chart(canvasElement, {
        type: 'bar',
        data: data,
        options: options
    });

    return chart; // return de chart, voor als je er nog iets mee wilt doen
}

function createPieChart(data, canvasElement, options) {
    // functie om een pie chart te maken
    // data (array): de data die in de chart moet komen
    // canvasElement: het element waar de chart in moet komen
    // options (optioneel): de opties die de chart moet hebben

    // als er geen opties zijn meegegeven, maak dan een lege optie
    if (options == undefined) {
        options = defaultOptions;
    }

    options.scales.y.ticks.color = "#00000000";
    options.scales.x.ticks.color = "#00000000";

    var chart = new Chart(canvasElement, {
        type: 'pie',
        data: data,
        options: options
    });

    return chart; // return de chart, voor als je er nog iets mee wilt doen
}