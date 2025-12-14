// PAGE INIT

document.addEventListener("DOMContentLoaded", () => {
    setupThemeToggle();
    updateNavbar();
    guardInvoicesPage();
    initializePage();
    setActiveNavLink();
});


// PAGE INITIALIZATION (Navbar + Dashboard Access)

function setupThemeToggle() {
    const toggle = document.getElementById("themeToggle");
    if (toggle) {
        toggle.addEventListener("click", () => {
            document.body.classList.toggle("theme-light");
            document.body.classList.toggle("theme-dark");
        });
    }
}

function setActiveNavLink() {
    const path = window.location.pathname;

    const linkMap = {
        "/": "homeLink",
        "/about": "aboutLink",
        "/dashboard": "dashboardLink",
        "/invoices": "accountLink",
        "/tickets": "contactLink"
    };

    // Remove active class from all nav links
    const allNavAnchors = document.querySelectorAll(".nav-links a");
    allNavAnchors.forEach(a => a.classList.remove("nav-active"));

    const activeLiId = linkMap[path];
    if (!activeLiId) return;

    const activeLi = document.getElementById(activeLiId);
    if (!activeLi) return;

    const activeAnchor = activeLi.querySelector("a");
    if (activeAnchor) activeAnchor.classList.add("nav-active");
}


function initializePage() {
    updateNavbar();

    const path = window.location.pathname.replace(/\/$/, "");
    const isDashboard = document.getElementById("eventsChart") !== null;
    const isInvoices = path === "/invoices";

    // Protect dashboard – redirect if not logged in
    if (isDashboard && !localStorage.getItem("username")) {
        window.location.href = "/login";
        return;
    }

    if (isDashboard) {
        initDashboard();
    }

    if (isInvoices) {
        loadMyInvoices();
    }
}


function guardInvoicesPage() {
    const path = window.location.pathname;
    const isInvoicesPage = (path === "/invoices");
    if (!isInvoicesPage) return;

    const user = localStorage.getItem("username");
    const role = localStorage.getItem("role");

    // Not logged in -> go login
    if (!user || !role) {
        window.location.href = "/login";
        return;
    }

    // Employees are not allowed
    const employeeRoles = ["management", "event-management", "finances"];
    if (employeeRoles.includes(role)) {
        window.location.href = "/";
    }
}

// NAVBAR + LOGOUT

function updateNavbar() {
    const user = localStorage.getItem("username");
    const role = localStorage.getItem("role");

    const loginBtn = document.getElementById("loginBtn");
    const userDisplay = document.getElementById("userDisplay");
    const logoutBtn = document.getElementById("logoutBtn");

    const dashboardLink = document.getElementById("dashboardLink");
    const accountLink = document.getElementById("accountLink");
    const contactLink = document.getElementById("contactLink");

    // 1) Base login UI
    if (loginBtn) loginBtn.style.display = user ? "none" : "block";

    if (userDisplay) {
        userDisplay.style.display = user ? "block" : "none";
        if (user) userDisplay.innerHTML = `<span style="color:#fff;">${user}</span>`;
    }

    if (logoutBtn) logoutBtn.style.display = user ? "block" : "none";

    // 2) Default: hide special links, then enable per role
    if (dashboardLink) dashboardLink.style.display = "none";
    if (accountLink) accountLink.style.display = "none";

    // 3) Contact Us is ALWAYS visible (everyone)
    if (contactLink) contactLink.style.display = "block";

    // If not logged in, stop here (no dashboard, no account)
    if (!user || !role) return;

    // 4) Dashboard visibility:
    // Employees + IT see dashboard. Customer does not.
    const employeeRoles = ["management", "event-management", "finances"];
    if (dashboardLink && (employeeRoles.includes(role) || role === "it")) {
        dashboardLink.style.display = "block";
    }

    // 5) My Account visibility:
    // Only customer + IT can see it. Employees must not.
    if (accountLink && (role === "customer" || role === "it")) {
        accountLink.style.display = "block";
    }
}


async function logout() {
    await fetch("/auth/logout", { method: "POST" });

    localStorage.removeItem("username");
    localStorage.removeItem("role");

    window.location.href = "/login";
}

// ROLE-BASED DASHBOARD FILTERING

function filterDashboardByRole() {
    const role = localStorage.getItem("role");

    const managementSection = document.getElementById("managementSection");
    const eventMgmtSection = document.getElementById("eventMgmtSection");
    const financeSection = document.getElementById("financeSection");

    // Hide all by default
    if (managementSection) managementSection.style.display = "none";
    if (eventMgmtSection) eventMgmtSection.style.display = "none";
    if (financeSection) financeSection.style.display = "none";

    if (!role) return;

    // IT — sees everything
    if (role === "it") {
        if (managementSection) managementSection.style.display = "block";
        if (eventMgmtSection) eventMgmtSection.style.display = "block";
        if (financeSection) financeSection.style.display = "block";
        return;
    }

    // MANAGEMENT — sees management + event-management
    if (role === "management") {
        if (managementSection) managementSection.style.display = "block";
        if (eventMgmtSection) eventMgmtSection.style.display = "block";
        return;
    }

    // EVENT MANAGEMENT — sees event management only
    if (role === "event-management") {
        if (eventMgmtSection) eventMgmtSection.style.display = "block";
        return;
    }

    // FINANCES — sees only finance section
    if (role === "finances") {
        if (financeSection) financeSection.style.display = "block";
        return;
    }
}


// DASHBOARD INIT SEQUENCE

let eventTypesMap = {};

async function initDashboard() {
    await loadEventTypes();
    await loadEvents();
    await loadCustomers();
    await loadProfit();
    await loadTopPayments();
    await loadEventDetails();
    await loadTopBudgets();
    await loadEventsChart();
    await loadProfitChart();
    await loadCustomerChart();
    await loadAvgProfitChart();
    await loadIncomeChart();
    await loadExpensesChart();
    await loadEventsByTypeChart();

    // Apply role filtering after everything is drawn
    filterDashboardByRole();
    const role = localStorage.getItem("role");

    if (role === "event-management" || role === "management") {
        loadEventManagementTickets();
    }

    if (role === "it") {
        loadEventManagementTickets();
        loadITTickets();
    }

}

// KPI + TABLE LOADERS

async function loadEvents() {
    try {
        const res = await fetch('/events/');
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

        const data = await res.json();

        const kpiElement = document.getElementById('eventsKPI');
        if (kpiElement) {
            kpiElement.innerText = data.length;
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
        const el = document.getElementById('profitKPI');
        if (el) {
            el.innerText = '$' + totalProfit;
        }
    } catch (err) {
        console.error('Error fetching profit:', err);
    }
}

async function loadCustomers() {
    try {
        const res = await fetch('/clients/');
        const data = await res.json();
        const el = document.getElementById('customersKPI');
        if (el) {
            el.innerText = data.length;
        }
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
            .sort((a, b) => b[1] - a[1])
            .slice(0, 3);

        const tbody = document.getElementById('topPaymentsTableBody');
        if (!tbody) return;
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
        if (!tbody) return;
        tbody.innerHTML = '';

        data.forEach(ev => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${ev.title}</td>
                <td>${eventTypesMap[ev.event_type_id] || "Unknown"}</td>
                <td>${ev.date}</td>
                <td>${ev.budget}</td>
                <td>${ev.guests || 0}</td>
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

        const sorted = data.sort((a, b) => b.budget - a.budget).slice(0, 5);

        const tbody = document.getElementById('topBudgetsTableBody');
        if (!tbody) return;
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

// CHARTS

async function loadEventsChart() {
    try {
        const res = await fetch('/events/');
        const data = await res.json();

        const months = Array.from({ length: 12 }, (_, i) => i + 1);
        const eventsPerMonth = months.map(m =>
            data.filter(ev => new Date(ev.date).getMonth() + 1 === m).length
        );

        const canvas = document.getElementById('eventsChart');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: months.map(m => 'Month ' + m),
                datasets: [{
                    label: 'Events per Month',
                    data: eventsPerMonth,
                    backgroundColor: 'rgba(54, 162, 235, 0.6)'
                }]
            },
            options: { responsive: true }
        });

    } catch (err) {
        console.error('Error loading events chart:', err);
    }
}

async function loadProfitChart() {
    try {
        const res = await fetch('/payments/');
        const data = await res.json();

        const months = Array.from({ length: 12 }, (_, i) => i + 1);
        const profitPerMonth = months.map(m => data
            .filter(p => new Date(p.date).getMonth() + 1 === m)
            .reduce((sum, p) => sum + p.amount, 0)
        );

        const canvas = document.getElementById('profitChart');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: months.map(m => 'Month ' + m),
                datasets: [{
                    label: 'Profit per Month',
                    data: profitPerMonth,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    fill: true
                }]
            },
            options: { responsive: true }
        });

    } catch (err) {
        console.error('Error loading profit chart:', err);
    }
}

async function loadAvgProfitChart() {
    try {
        const paymentsRes = await fetch('/payments/');
        const clientsRes = await fetch('/clients/');
        const payments = await paymentsRes.json();
        const clients = await clientsRes.json();

        const months = Array.from({ length: 12 }, (_, i) => i + 1);
        const avgProfitPerMonth = months.map(m => {
            const monthPayments = payments.filter(p => new Date(p.date).getMonth() + 1 === m);
            return clients.length
                ? monthPayments.reduce((sum, p) => sum + p.amount, 0) / clients.length
                : 0;
        });

        const canvas = document.getElementById('avgProfitChart');
        if (canvas) {
            const ctx = canvas.getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: months.map(m => 'Month ' + m),
                    datasets: [{
                        label: 'Avg Profit per Customer',
                        data: avgProfitPerMonth,
                        backgroundColor: 'rgba(153, 102, 255, 0.6)'
                    }]
                },
                options: { responsive: true }
            });
        }

        // KPI
        const totalProfit = payments.reduce((sum, p) => sum + p.amount, 0);
        const overallAvg = clients.length ? totalProfit / clients.length : 0;
        const kpi = document.getElementById('avgProfitKPI');
        if (kpi) {
            kpi.textContent = '$' + overallAvg.toFixed(2);
        }

    } catch (err) {
        console.error('Error loading avg profit chart:', err);
    }
}

async function loadCustomerChart() {
    try {
        const res = await fetch('/clients/');
        const data = await res.json();

        const months = Array.from({ length: 12 }, (_, i) => i + 1);
        const customersPerMonth = months.map(m =>
            data.filter(c => new Date(c.registered_date).getMonth() + 1 === m).length
        );

        const canvas = document.getElementById('customerChart');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: months.map(m => 'Month ' + m),
                datasets: [{
                    label: 'Customers per Month',
                    data: customersPerMonth,
                    borderColor: 'rgba(255, 159, 64, 1)',
                    backgroundColor: 'rgba(255, 159, 64, 0.2)',
                    fill: true
                }]
            },
            options: { responsive: true }
        });

    } catch (err) {
        console.error('Error loading customer chart:', err);
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

        const canvas = document.getElementById('incomeChart');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');

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

async function loadMyInvoices() {
    const table = document.getElementById("paymentsTable");
    if (!table) return;

    try {
        const res = await fetch("/invoices/my");

        if (!res.ok) {
            table.innerHTML = `
                <tr>
                    <td colspan="3" style="text-align:center;color:#999;">
                        No invoices available
                    </td>
                </tr>`;
            return;
        }

        const invoices = await res.json();

        if (invoices.length === 0) {
            table.innerHTML = `
                <tr>
                    <td colspan="3" style="text-align:center;color:#999;">
                        No open invoices
                    </td>
                </tr>`;
            return;
        }

        table.innerHTML = "";

        invoices.forEach(inv => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${inv.invoice_number}</td>
                <td>${inv.due_date ?? "-"}</td>
                <td>$${inv.amount_total.toFixed(2)}</td>
            `;
            table.appendChild(tr);
        });

    } catch (err) {
        console.error("Failed to load invoices", err);
        table.innerHTML = `
            <tr>
                <td colspan="3" style="text-align:center;color:#999;">
                    Error loading invoices
                </td>
            </tr>`;
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

        const canvas = document.getElementById('expensesChart');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');

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

        const months = Array.from({ length: 12 }, (_, i) => i + 1);

        const datasets = eventTypes.map(t => {
            const dataPerMonth = months.map(m =>
                events.filter(ev =>
                    ev.event_type_id === t.id &&
                    new Date(ev.date).getMonth() + 1 === m
                ).length
            );

            return {
                label: t.title,
                data: dataPerMonth,
                backgroundColor: getRandomColor()
            };
        });

        const canvas = document.getElementById('eventsByTypeChart');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');

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

async function loadEventManagementTickets() {
    const section = document.getElementById("eventMgmtTickets");
    const body = document.getElementById("eventMgmtTicketsBody");
    if (!section || !body) return;

    const res = await fetch("/ticket/event-management");
    const tickets = await res.json();

    body.innerHTML = "";

    if (tickets.length === 0) {
        body.innerHTML = `<tr><td colspan="3">No tickets</td></tr>`;
    } else {
        tickets.forEach(t => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${t.title}</td>
                <td>${t.type}</td>
                <td style="max-width:400px; color:#bdbdbd;">${t.description || "-"}</td>
                <td>${t.status}</td>
            `;
            body.appendChild(tr);
        });
    }

    section.style.display = "block";
}

async function loadITTickets() {
    const section = document.getElementById("itTickets");
    const body = document.getElementById("itTicketsBody");
    if (!section || !body) return;

    const res = await fetch("/ticket/it");
    const tickets = await res.json();

    body.innerHTML = "";

    if (tickets.length === 0) {
        body.innerHTML = `<tr><td colspan="3">No tickets</td></tr>`;
    } else {
        tickets.forEach(t => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${t.title}</td>
                <td>${t.type}</td>
                <td style="max-width:400px; color:#bdbdbd;">${t.description || "-"}</td>
                <td>${t.status}</td>
            `;
            body.appendChild(tr);
        });
    }

    section.style.display = "block";
}

async function sendMessage(event) {
    event.preventDefault();

    const categoryEl = document.getElementById("category");
    const titleEl = document.getElementById("title");
    const messageEl = document.getElementById("message");

    if (!categoryEl || !titleEl || !messageEl) {
        console.error("Contact form elements not found");
        return;
    }

    const payload = {
        category: categoryEl.value,      // book | event | tech
        title: titleEl.value.trim(),
        message: messageEl.value.trim()
    };

    try {
        const res = await fetch("/ticket", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const err = await res.json();
            alert(err.error || "Failed to send ticket");
            return;
        }

        alert("Ticket submitted successfully!");
        event.target.reset();

    } catch (err) {
        console.error("Ticket submission failed", err);
        alert("Server error while sending ticket");
    }
}


function getRandomColor() {
    const r = Math.floor(Math.random() * 200);
    const g = Math.floor(Math.random() * 200);
    const b = Math.floor(Math.random() * 200);
    return `rgba(${r},${g},${b},0.6)`;
}
