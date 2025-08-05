document.addEventListener('DOMContentLoaded', () => {
    const chartContainer = document.getElementById('chart-container');
    if (chartContainer) {
        console.log('Chart-Container gefunden');
        const canvas = document.createElement('canvas');
        canvas.id = 'categoryChart';
        chartContainer.appendChild(canvas);
        const ctx = canvas.getContext('2d');

        const chartData = document.getElementById('chart-data');
        if (chartData) {
            console.log('Chart-Data gefunden');
            const labelsRaw = chartData.dataset.labels || '[]';
            const dataRaw = chartData.dataset.data || '[]';
            console.log('Raw Labels:', labelsRaw);
            console.log('Raw Data:', dataRaw);
            console.log('Labels Length:', labelsRaw.length);
            console.log('Data Length:', dataRaw.length);

            let labels, data;
            try {
                labels = JSON.parse(labelsRaw);
                data = JSON.parse(dataRaw);
                console.log('Parsed Labels:', labels);
                console.log('Parsed Data:', data);
            } catch (e) {
                console.error('JSON-Parsing-Fehler:', e.message, 'Raw Labels:', labelsRaw, 'Raw Data:', dataRaw);
                labels = [];
                data = [];
            }

            if (labels.length === 0 || data.length === 0) {
                console.warn('Keine gültigen Daten für das Diagramm');
                chartContainer.innerHTML = '<p>Keine Daten verfügbar.</p>';
            } else {
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Ausgaben pro Kategorie (€)',
                            data: data,
                            backgroundColor: 'rgba(54, 162, 235, 0.6)',
                            borderColor: 'rgba(54, 162, 235, 1)',
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
            }
        } else {
            console.error('Chart-Data-Element nicht gefunden');
        }
    } else {
        console.error('Chart-Container nicht gefunden');
    }
});