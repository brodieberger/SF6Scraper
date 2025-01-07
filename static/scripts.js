document.addEventListener("DOMContentLoaded", function () {
    const playerId = window.location.pathname.split('/').pop(); // Extract player_id from URL

    // Fetch data for the line chart
    fetch(`/streetfighter/data/${playerId}/line_chart`)
        .then(response => response.json())
        .then(data => {
            console.log("Line Chart Data:", data);

            // Parse and process data for Chart.js (Line Chart)
            const labels = data.map(match => match.id);
            const mrData = data.map(match => match.mr);

            // Render Line Chart
            const lineCtx = document.getElementById('mrLineChart').getContext('2d');
            new Chart(lineCtx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Player MR',
                        data: mrData,
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
                            text: `Player ${playerId} MR`
                        }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Match ID'
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
        })
        .catch(error => console.error("Error fetching line chart data:", error));

    // Fetch data for the pie chart
    fetch(`/streetfighter/data/${playerId}/pie_chart`)
        .then(response => response.json())
        .then(data => {
            console.log("Pie Chart Data:", data);

            // Parse and process data for Chart.js (Pie Chart)
            const labels = data.map(entry => entry.opponent_character);
            const counts = data.map(entry => entry.count);

            // Render Pie Chart
            const pieCtx = document.getElementById('characterPieChart').getContext('2d');
            new Chart(pieCtx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Character Frequency',
                        data: counts,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1
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
                            text: `Character Frequency for Player ${playerId}`
                        }
                    }
                }
            });
        })
        .catch(error => console.error("Error fetching pie chart data:", error));
});
