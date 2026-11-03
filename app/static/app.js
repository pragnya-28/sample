const authCard = document.getElementById('loginCard');
const dashboardSection = document.getElementById('dashboard');
const logoutBtn = document.getElementById('logoutBtn');
const loginForm = document.getElementById('loginForm');
const loginError = document.getElementById('loginError');

function updateSummary(summary) {
  document.getElementById('totalTokens').textContent = Number(summary.total_tokens).toLocaleString();
  document.getElementById('computeHours').textContent = Number(summary.total_compute_hours).toFixed(1);
  document.getElementById('electricity').textContent = `${Number(summary.estimated_electricity_kwh).toFixed(1)} kWh`;
  document.getElementById('resourceIndex').textContent = Number(summary.resource_exhaustion_index).toFixed(1);
}

function renderSourceList(topSources) {
  const list = document.getElementById('sourceList');
  list.innerHTML = topSources
    .map(([source, count]) => `<li><span>${source}</span><strong>${count}</strong></li>`)
    .join('');
}

function renderUsageTable(usageEvents) {
  const body = document.getElementById('usageTableBody');
  body.innerHTML = usageEvents
    .slice(0, 6)
    .map((event) => `
      <tr>
        <td>${event.source}</td>
        <td>${event.model}</td>
        <td>${Number(event.tokens).toLocaleString()}</td>
        <td>${((event.tokens / 100000) + (event.compute_hours * 1.2)).toFixed(1)}</td>
      </tr>
    `)
    .join('');
}

function renderAuditTable(auditEvents) {
  const body = document.getElementById('auditTableBody');
  body.innerHTML = auditEvents
    .slice(-5)
    .reverse()
    .map((event) => `
      <tr>
        <td>${event.user}</td>
        <td>${event.action}</td>
        <td>${event.resource}</td>
        <td>${event.timestamp}</td>
      </tr>
    `)
    .join('');
}

async function loadDashboard() {
  const response = await fetch('/api/v1/dashboard', { credentials: 'same-origin' });
  if (!response.ok) {
    showLogin();
    return;
  }

  const data = await response.json();
  updateSummary(data.summary);
  renderSourceList(data.top_sources);
  renderUsageTable(data.usage_events);

  const auditsResponse = await fetch('/api/v1/audits', { credentials: 'same-origin' });
  if (auditsResponse.ok) {
    const audits = await auditsResponse.json();
    renderAuditTable(audits.audit_events);
  }

  showDashboard();
}

async function handleLogin(event) {
  event.preventDefault();
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  const response = await fetch('/api/v1/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'same-origin',
    body: JSON.stringify({ username, password })
  });

  const data = await response.json();
  if (!response.ok) {
    loginError.textContent = data.error || 'Login failed';
    loginError.classList.remove('hidden');
    return;
  }

  loginError.classList.add('hidden');
  loadDashboard();
}

async function handleLogout() {
  await fetch('/api/v1/logout', {
    method: 'POST',
    credentials: 'same-origin'
  });
  showLogin();
}

function showDashboard() {
  authCard.classList.add('hidden');
  dashboardSection.classList.remove('hidden');
  logoutBtn.classList.remove('hidden');
}

function showLogin() {
  authCard.classList.remove('hidden');
  dashboardSection.classList.add('hidden');
  logoutBtn.classList.add('hidden');
}

loginForm.addEventListener('submit', handleLogin);
logoutBtn.addEventListener('click', handleLogout);

showLogin();
