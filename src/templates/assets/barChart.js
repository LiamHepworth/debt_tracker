// Get the canvas element and the data
const chartCanvas = document.getElementById("keywordChart");
const chartDataElement = document.getElementById("keyword-chart-data");

// Check the canvas and data are valid
if (chartCanvas && chartDataElement) {

    // Separate data into keys / values, get maxValue
    const keywordCounts = JSON.parse(chartDataElement.textContent);
    const keywordLabels = Object.keys(keywordCounts);
    const keywordValues = Object.values(keywordCounts);
    const maxValue = Math.max(...keywordValues, 0);

    if (typeof Chart !== "undefined" && keywordLabels.length > 0) {
        new Chart(chartCanvas, {
            type: "bar",
            data: {
                labels: keywordLabels,
                datasets: [{
                    data: keywordValues,
                    backgroundColor: "#46b8e5",
                    borderColor: "#3073a3",
                    borderWidth: 1,
                    borderRadius: 6
                }]
            },
            options: {
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        suggestedMax: maxValue + 1,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }
}
