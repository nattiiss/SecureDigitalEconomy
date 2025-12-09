document.addEventListener('DOMContentLoaded', async () => {
    await loadEvents();
    await loadCustomers();
});

async function loadEvents() {
    try {
        const res = await fetch('/events/');
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

        const data = await res.json();

        const kpiElement = document.getElementById('eventsKPI');
        if (kpiElement) {
            kpiElement.innerText = data.length; 
        } else {
            console.warn('Element #eventsKPI nicht gefunden');
        }

        const listElement = document.getElementById('eventsList');
        if (listElement) {
            listElement.innerHTML = data.map(e => `<li>${e.title} - ${e.date}</li>`).join('');
        }

    } catch (err) {
        console.error('Error fetching events:', err);
    }
}

async function loadProfit() {
    try {
        const res = await fetch('/payments/');
        const data = await res.json();
        const totalProfit = data.reduce((sum, p) => sum + p.amount, 0);
        document.getElementById('profitKPI').innerText = '$' + totalProfit;
    } catch (err) {
        console.error('Error fetching profit:', err);
    }
}

async function loadCustomers() {
    try {
        const res = await fetch('/clients/'); 
        console.log("Response status:", res.status);
        const data = await res.json();
        console.log("Clients data:", data);
        document.getElementById('customersKPI').innerText = data.length;
    } catch (err) {
        console.error('Error fetching customers:', err);
    }
}


async function loadTopPayments() {
    try {
        const resPayments = await fetch('/payments/');
        const payments = await resPayments.json();

        const resTypes = await fetch('/payment-types/');
        const types = await resTypes.json();

        const typeMap = {};
        types.forEach(t => typeMap[t.id] = t.title);

        const counts = {};
        payments.forEach(p => {
            const title = typeMap[p.type_id] || 'Unknown';
            counts[title] = (counts[title] || 0) + 1;
        });

        const sorted = Object.entries(counts)
            .sort((a,b) => b[1]-a[1])
            .slice(0,3);

        const tbody = document.getElementById('topPaymentsTableBody');
        tbody.innerHTML = '';
        sorted.forEach(([system, count]) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${system}</td><td>${count}</td>`;
            tbody.appendChild(tr);
        });

    } catch (err) {
        console.error('Error fetching top payments:', err);
    }
}


async function loadEventTypes() {
    try {
        const res = await fetch("/event-types/");
        const types = await res.json();
        types.forEach(t => {
            eventTypesMap[t.id] = t.title;
        });
    } catch (err) {
        console.error("Error fetching event types:", err);
    }
}

async function loadEventDetails() {
    try {
        const res = await fetch('/events/');
        const data = await res.json();
        const tbody = document.getElementById('eventDetailsTableBody');
        tbody.innerHTML = '';

        data.forEach(ev => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${ev.title}</td>
                <td>${eventTypesMap[ev.event_type_id] || "Unknown"}</td>
                <td>${ev.date}</td>
                <td>${ev.budget}</td>
                <td>${ev.guests || 0}</td> <!-- falls guests nicht existiert -->
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error('Error fetching event details:', err);
    }
}

async function loadTopBudgets() {
    try {
        const res = await fetch('/events/');
        const data = await res.json();
        const sorted = data.sort((a,b)=>b.budget - a.budget).slice(0,5);
        const tbody = document.getElementById('topBudgetsTableBody');
        tbody.innerHTML = '';
        sorted.forEach(ev => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${ev.title}</td><td>${ev.budget}</td>`;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error('Error fetching top budgets:', err);
    }
}


async function loadEventsChart() {
    try {
        const res = await fetch('/events/');
        const data = await res.json();

        const months = Array.from({length:12}, (_,i)=>i+1);
        const eventsPerMonth = months.map(m => data.filter(ev => new Date(ev.date).getMonth()+1 === m).length);

        const ctx = document.getElementById('eventsChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: months.map(m=>'Month '+m),
                datasets: [{
                    label: 'Events per Month',
                    data: eventsPerMonth,
                    backgroundColor: 'rgba(54, 162, 235, 0.6)'
                }]
            },
            options: { responsive:true }
        });

    } catch (err) {
        console.error('Error loading events chart:', err);
    }
}


async function loadProfitChart() {
    try {
        const res = await fetch('/payments/');
        const data = await res.json();

        const months = Array.from({length:12}, (_,i)=>i+1);
        const profitPerMonth = months.map(m => data
            .filter(p => new Date(p.date).getMonth()+1 === m)
            .reduce((sum,p)=>sum+p.amount,0)
        );

        const ctx = document.getElementById('profitChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: months.map(m=>'Month '+m),
                datasets: [{
                    label: 'Profit per Month',
                    data: profitPerMonth,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    fill: true
                }]
            },
            options: { responsive:true }
        });

    } catch (err) {
        console.error('Error loading profit chart:', err);
    }
}


async function loadAvgProfitChart() {
    try {
        const paymentsRes = await fetch('/payments/');
        const clientsRes = await fetch('/clients');
        const payments = await paymentsRes.json();
        const clients = await clientsRes.json();

        const months = Array.from({length:12}, (_,i)=>i+1);
        const avgProfitPerMonth = months.map(m => {
            const monthPayments = payments.filter(p => new Date(p.date).getMonth()+1 === m);
            return monthPayments.reduce((sum,p)=>sum+p.amount,0) / clients.length;
        });

        const ctx = document.getElementById('avgProfitChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: months.map(m=>'Month '+m),
                datasets: [{
                    label: 'Avg Profit per Customer',
                    data: avgProfitPerMonth,
                    backgroundColor: 'rgba(153, 102, 255, 0.6)'
                }]
            },
            options: { responsive:true }
        });

    } catch (err) {
        console.error('Error loading avg profit chart:', err);
    }
}


async function loadCustomerChart() {
    try {
        const res = await fetch('/clients/');
        const data = await res.json();

        const months = Array.from({length:12}, (_,i)=>i+1);
        const customersPerMonth = months.map(m => data.filter(c => new Date(c.registered_date).getMonth()+1 === m).length);

        const ctx = document.getElementById('customerChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: months.map(m=>'Month '+m),
                datasets: [{
                    label: 'Customers per Month',
                    data: customersPerMonth,
                    borderColor: 'rgba(255, 159, 64, 1)',
                    backgroundColor: 'rgba(255, 159, 64, 0.2)',
                    fill: true
                }]
            },
            options: { responsive:true }
        });

    } catch (err) {
        console.error('Error loading customer chart:', err);
    }
}

async function loadTopBudgets() {
    try {
        const res = await fetch('/events/');
        const data = await res.json();

        const sorted = data.sort((a, b) => b.budget - a.budget).slice(0, 5);

        const tbody = document.getElementById('topBudgetsTableBody');
        tbody.innerHTML = '';

        sorted.forEach(ev => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${ev.title}</td>
                <td>${ev.budget}</td>
            `;
            tbody.appendChild(tr);
        });

    } catch (err) {
        console.error('Error loading top budgets:', err);
    }
}



async function loadIncomeChart() {
    try {
        const res = await fetch('/payments/');
        const payments = await res.json();

        const months = Array.from({ length: 12 }, (_, i) => i);

        const incomePerMonth = months.map(m =>
            payments
                .filter(p => new Date(p.date).getMonth() === m)
                .reduce((sum, p) => sum + p.amount, 0)
        );

        const ctx = document.getElementById('incomeChart').getContext('2d');

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: months.map(m => 'Month ' + (m + 1)),
                datasets: [{
                    label: 'Income per Month',
                    data: incomePerMonth,
                    borderColor: 'rgba(0, 200, 0, 1)',
                    backgroundColor: 'rgba(0, 200, 0, 0.2)',
                    fill: true
                }]
            },
            options: { responsive: true }
        });

    } catch (err) {
        console.error('Error loading income chart:', err);
    }
}



async function loadExpensesChart() {
    try {
        const res = await fetch('/expenses/');
        const expenses = await res.json();

        const months = Array.from({ length: 12 }, (_, i) => i);

        const expensesPerMonth = months.map(m =>
            expenses
                .filter(e => new Date(e.date).getMonth() === m)
                .reduce((sum, e) => sum + e.amount, 0)
        );

        const ctx = document.getElementById('expensesChart').getContext('2d');

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: months.map(m => 'Month ' + (m + 1)),
                datasets: [{
                    label: 'Expenses per Month',
                    data: expensesPerMonth,
                    backgroundColor: 'rgba(255, 80, 80, 0.6)',
                    borderColor: 'rgba(255, 80, 80, 1)',
                    borderWidth: 1
                }]
            },
            options: { responsive: true }
        });

    } catch (err) {
        console.error('Error loading expenses chart:', err);
    }
}


async function loadEventsByTypeChart() {
    try {
        const resEvents = await fetch('/events/');
        const events = await resEvents.json();

        const resTypes = await fetch('/event-types/');
        const eventTypes = await resTypes.json();

        const typeMap = {};
        eventTypes.forEach(t => typeMap[t.id] = t.title);

        const months = Array.from({length: 12}, (_, i) => i + 1);

        const datasets = eventTypes.map(t => {
            const dataPerMonth = months.map(m => 
                events.filter(ev => ev.event_type_id === t.id && new Date(ev.date).getMonth() + 1 === m).length
            );

            return {
                label: t.title,
                data: dataPerMonth,
                backgroundColor: getRandomColor(),
            };
        });

        const ctx = document.getElementById('eventsByTypeChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: months.map(m => 'Month ' + m),
                datasets: datasets
            },
            options: {
                responsive: true,
                scales: {
                    x: { stacked: true },
                    y: { stacked: true, beginAtZero: true }
                }
            }
        });

    } catch (err) {
        console.error('Error loading Events by Type chart:', err);
    }
}

function getRandomColor() {
    const r = Math.floor(Math.random()*200);
    const g = Math.floor(Math.random()*200);
    const b = Math.floor(Math.random()*200);
    return `rgba(${r},${g},${b},0.6)`;
}

loadEventsByTypeChart();

async function initCharts() {
    await loadEventsChart();
    await loadProfitChart();
    await loadCustomerChart();
    await loadAvgProfitChart();
    await loadProfit();
    await loadTopPayments();
    await loadEventDetails();
    await loadTopBudgets();
    await loadIncomeChart(); 
    await loadExpensesChart(); 
}

initCharts();


async function initDashboard() {
    await loadEventTypes(); 
    await loadEventDetails();
}

initDashboard();





