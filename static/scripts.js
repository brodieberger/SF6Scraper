document.addEventListener("DOMContentLoaded", function () {
    const playerId = window.location.pathname.split('/').pop(); // Extract player_id from URL

    // Fetch data from the server for the player ID
    fetch(`/data/${playerId}/line_chart`)
    .then(response => response.json())
    .then(data => {
        console.log("Line Chart Data:", data);
            // Parse and process data for Chart.js
            const labels = data.map(match => match.id); // Replace `match_date` with actual date field
            const mrData = data.map(match => match.mr); // Replace `mr` with actual MR field

            // Render Chart.js chart
            const ctx = document.getElementById('mrLineChart').getContext('2d');
            new Chart(ctx, {
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
        .catch(error => console.error("Error fetching player data:", error));
});
