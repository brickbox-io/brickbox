monthly_chart = {

    initMonthlyBreakdown: function (user, ReqYear) {

        var MonthlyBreakdownAmount = false

        window.onload = MonthlyBreakdown();
        function MonthlyBreakdown() {
            var formData = new FormData();
            var xhttp = new XMLHttpRequest();

            var current_url = window.location.href
            var selected_colo = current_url[current_url.length - 1]
            console.log(selected_colo)
            if (Number.isInteger(Number(selected_colo))) {
                var url = '/data/monthlybreakdown/' + selected_colo;
            } else {
                var url = '/data/monthlybreakdown/';
            }
            console.log(url)

            formData.append('client', user);

            xhttp.onload = function () {
                console.log(this.responseText);
                MonthlyBreakdownAmount = JSON.parse(this.responseText)[ReqYear];
                MonthlyBalanceChart();
            };

            xhttp.open('POST', url, true);
            xhttp.setRequestHeader("X-CSRFToken", csrftoken)
            xhttp.send(formData);
        }

        gradientBarChartConfiguration = {
            maintainAspectRatio: false,
            legend: {
                display: false
            },

            tooltips: {
                backgroundColor: '#f5f5f5',
                titleFontColor: '#333',
                bodyFontColor: '#666',
                bodySpacing: 4,
                xPadding: 12,
                mode: "nearest",
                intersect: 0,
                position: "nearest"
            },
            responsive: true,
            scales: {
                yAxes: [{

                    gridLines: {
                        drawBorder: false,
                        color: 'rgba(29,140,248,0.1)',
                        zeroLineColor: "transparent",
                    },
                    ticks: {
                        suggestedMin: 60,
                        suggestedMax: 120,
                        padding: 20,
                        fontColor: "#9e9e9e"
                    }
                }],

                xAxes: [{

                    gridLines: {
                        drawBorder: false,
                        color: 'rgba(29,140,248,0.1)',
                        zeroLineColor: "transparent",
                    },
                    ticks: {
                        padding: 20,
                        fontColor: "#9e9e9e"
                    }
                }]
            }
        };

        function MonthlyBalanceChart() {

            var ctx = document.getElementById("chartMonthlyBreakdown").getContext("2d");

            var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

            gradientStroke.addColorStop(1, 'rgba(29,140,248,0.2)');
            gradientStroke.addColorStop(0.4, 'rgba(29,140,248,0.0)');
            gradientStroke.addColorStop(0, 'rgba(29,140,248,0)'); //blue colors

            var myChart = new Chart(ctx, {
                type: 'bar',
                responsive: true,
                legend: {
                    display: false
                },
                data: {
                    labels: ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.'],
                    datasets: [{
                        label: "Total $",
                        fill: true,
                        backgroundColor: gradientStroke,
                        hoverBackgroundColor: gradientStroke,
                        borderColor: '#1f8ef1',
                        borderWidth: 2,
                        borderDash: [],
                        borderDashOffset: 0.0,
                        data: MonthlyBreakdownAmount,
                    }]
                },
                options: gradientBarChartConfiguration
            });
        }
    }
}
