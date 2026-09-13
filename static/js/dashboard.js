

// Sidebar toggle
const burger = document.getElementById('dashBurger');
const sidebar = document.getElementById('dashSidebar');
if (burger && sidebar) {
    burger.addEventListener('click', () => sidebar.classList.toggle('is-open'));
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 860 &&
            sidebar.classList.contains('is-open') &&
            !sidebar.contains(e.target) && e.target !== burger) {
            sidebar.classList.remove('is-open');
        }
    });
}

// Render chart if Chart.js is loaded
if (window.Chart) {
    const el = document.getElementById('chart-data');
    const canvas = document.getElementById('leadsChart');
    if (el && canvas) {
        const data = JSON.parse(el.textContent);
        new Chart(canvas, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    borderColor: '#176B45',
                    backgroundColor: 'rgba(23,107,69,.10)',
                    fill: true,
                    tension: .35,
                    pointRadius: 3,
                    pointBackgroundColor: '#176B45',
                    borderWidth: 2,
                }]
            },
            options: {
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true, ticks: { precision: 0 } },
                    x: { grid: { display: false } }
                }
            }
        });
    }
}