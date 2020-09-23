$(document).ready(function () {

    var voteChartCtx = $("#vote-chart");
    var ratioChartCtx = $("#ratio-chart");
    var voteChart = undefined;
    var ratioChart = undefined;

    var colors = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf"
    ]

    function toogleLoading(isLoading) {
        if (isLoading) {
            $(".spinner-border").show();
        } else {
            $(".spinner-border").hide();
        }
    }

    /**
     * Pick color by index
     */
    function colorPicker(index) {
        return colors[index % colors.length];
    }

    /**
     * Generate a set of color according to the data length
     */
    function colorSetGenerator(total_length) {
        var colorSet = [];
        for (var i = 0; i < total_length; i++) {
            colorSet.push(colorPicker(i));
        }
        return colorSet;
    }

    /**
     * Set up charts
     */
    function initChart(response) {
        voteChart = new Chart(voteChartCtx, {
            type: "horizontalBar",
            data: {
                labels: response.answer_texts,
                datasets: [{
                    label: "Votes",
                    data: response.votes,
                    backgroundColor: colorSetGenerator(response.answer_texts.length)
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    xAxes: [{
                        ticks: {
                            beginAtZero: true,
                            precision: 0
                        }
                    }]
                },
            }
        });

        ratioChart = new Chart(ratioChartCtx, {
            type: "doughnut",
            data: {
                labels: response.answer_texts,
                datasets: [{
                    data: response.votes,
                    backgroundColor: colorSetGenerator(response.answer_texts.length)
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                tooltips: {
                    // Add percentage showing in doughnut chart
                    callbacks: {
                        label: function (tooltipItem, data) {
                            var dataset = data.datasets[tooltipItem.datasetIndex];
                            var meta = dataset._meta[Object.keys(dataset._meta)[0]];
                            var total = meta.total;
                            var currentValue = dataset.data[tooltipItem.index];
                            var percentage = parseFloat((currentValue / total * 100).toFixed(1));
                            return currentValue + ' (' + percentage + '%)';
                        },
                        title: function (tooltipItem, data) {
                            return data.labels[tooltipItem[0].index];
                        }
                    }
                },
            }
        });
    }

    /**
     * Fetch data for drawing charts
     */
    async function fetchData() {
        var uuid = $("#poll-question").attr("data-id");
        var totalVotes = $("#total-votes-text").attr("data-total-votes");
        if (uuid.length > 0 && parseInt(totalVotes) > 0) {
            toogleLoading(true);
            var request = {
                method: "POST",
                body: JSON.stringify({
                    "uuid": uuid,
                }),
                headers: new Headers({
                    "Content-Type": "application/json"
                }),
            };
            try {
                const response = await fetch(window.location.origin + "/result", request);
                const json_res = await response.json();
                initChart(json_res);
            } catch (error) {
                console.log(error);
            } finally {
                toogleLoading(false);
            }

        } else {
            console.log("Erro: UUID is empty")
        }
    }

    fetchData();
});