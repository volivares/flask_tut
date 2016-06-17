$(function() {
    Morris.Donut({
        element: 'morris-donut-chart-sadasi',
        data: [{
            label: "Capturado",
            value: 18.5
        }, {
            label: "Pendiente",
            value: 81.5
        }],
        resize: true
    });

    Morris.Donut({
        element: 'morris-donut-chart-alta',
        data: [{
            label: "Capturado",
            value: 26
        }, {
            label: "Pendiente",
            value: 74
        }],
        resize: true
    });   
});
