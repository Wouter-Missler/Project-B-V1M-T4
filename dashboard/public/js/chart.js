function createBarChart(data, canvasElement, options) {
    // functie om een bar chart te maken
    // data (array): de data die in de chart moet komen
    // canvasElement: het element waar de chart in moet komen
    // options (optioneel): de opties die de chart moet hebben

    // als er geen opties zijn meegegeven, maak dan een lege optie
    if (options == undefined) {
        options = {
            scales: { y: { beginAtZero: true } } // begin de y-as bij 0
        };
    }

    var chart = new Chart(canvasElement, {
        type: 'bar',
        data: data,
        options: options
    });

    return chart; // return de chart, voor als je er nog iets mee wilt doen
}