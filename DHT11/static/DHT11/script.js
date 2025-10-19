const ctx = document.getElementById('sensorChart').getContext('2d');

let sensorChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [], 
        datasets: [
            {
                label: 'Temperatura (°C)',
                data: [],
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                tension: 0.3
            },
            {
                label: 'Umidade (%)',
                data: [],
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                tension: 0.3
            }
        ]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Função para atualizar o gráfico
function updateChart() {
    fetch('/dht11/dados/')  // URL da API
        .then(response => response.json())
        .then(data => {
            let labels = [];
            let temperatures = [];
            let humidities = [];

            data.reverse().forEach(item => {
                labels.push(new Date(item.timestamp).toLocaleTimeString());
                temperatures.push(item.temperatura);
                humidities.push(item.umidade);
            });

            sensorChart.data.labels = labels;
            sensorChart.data.datasets[0].data = temperatures;
            sensorChart.data.datasets[1].data = humidities;
            sensorChart.update();

            // Atualiza o último valor no div
            if(data.length > 0){
                document.querySelector('.umidadeTempArAtual').innerHTML = `
                    <p>Temperatura: ${data[data.length-1].temperatura} °C</p>
                    <p>Umidade: ${data[data.length-1].umidade} %</p>
                    <p>Atualizado em: ${new Date(data[data.length-1].timestamp).toLocaleTimeString()}</p>
                `;
            }
        })
        .catch(err => console.error('Erro ao buscar dados:', err));
}

// Atualiza a cada 10 segundos
updateChart();
setInterval(updateChart, 10000);
