// Wait for the DOM to fully load
document.addEventListener("DOMContentLoaded", function () {
    // Get the canvas element
    const ctx = document.getElementById('mrLineChart').getContext('2d');

    // Static data for the chart
    const labels = ['Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5'];
    const dataPoints = [1500, 1520, 1540, 1510, 1530];

    // Create a new line chart
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Player MR',
                data: dataPoints,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderWidth: 2,
                tension: 0.2,
                pointStyle: 'circle',
                pointRadius: 5
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Player MR Over 5 Games'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Games'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'MR'
                    },
                    beginAtZero: false
                }
            }
        }
    });
});
