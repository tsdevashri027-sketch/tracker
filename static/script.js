// script.js will create a simple bar chart from history data

function drawChart(history) {
    // count each reason
    const counts = {};
    history.forEach(e => {
        counts[e.reason_text] = (counts[e.reason_text] || 0) + 1;
    });

    const labels = Object.keys(counts);
    const data = labels.map(l => counts[l]);

    const ctx = document.getElementById('historyChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of entries',
                data: data,
                backgroundColor: 'rgba(54, 162, 235, 0.5)'
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}
