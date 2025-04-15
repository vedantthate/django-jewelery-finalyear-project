// custom_admin.js
document.addEventListener("DOMContentLoaded", function() {
    // Basic Chart.js example for a simple line chart
    var ctx = document.getElementById('orderChart').getContext('2d');
    var orderChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
            datasets: [{
                label: 'Orders Over Time',
                data: [12, 19, 3, 5, 2, 3, 8],
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
