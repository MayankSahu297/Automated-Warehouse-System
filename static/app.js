const API_URL = "http://127.0.0.1:8000";

// DOM Elements
const binGrid = document.getElementById('binGrid');
const queueContainer = document.getElementById('queueContainer');
const stackContainer = document.getElementById('stackContainer');
const logContainer = document.getElementById('logContainer');
const plannerResult = document.getElementById('plannerResult');

// Forms & Buttons
const ingestForm = document.getElementById('ingestForm');
const processBtn = document.getElementById('processBtn');
const checkFitBtn = document.getElementById('checkFitBtn');
const loadTruckBtn = document.getElementById('loadTruckBtn');
const rollbackBtn = document.getElementById('rollbackBtn');

// Init
async function init() {
    await refreshAll();
    setInterval(refreshAll, 2000);
}

async function refreshAll() {
    await Promise.all([
        fetchStatus(),
        fetchQueue(),
        fetchStack(),
        fetchLogs()
    ]);
}

// --- 1. BIN INVENTORY ---
async function fetchStatus() {
    try {
        const res = await fetch(`${API_URL}/status`);
        const data = await res.json();
        renderBins(data.bins);
    } catch (e) { console.error(e); }
}

function renderBins(bins) {
    binGrid.innerHTML = bins.map(bin => {
        const usage = (bin.current_load / bin.capacity) * 100;
        const isFull = usage >= 100;
        return `
            <div class="bin-card ${isFull ? 'full' : ''}">
                <div class="bin-header">
                    <span class="bin-id">#${bin.bin_id}</span>
                    <span class="bin-loc">${bin.location}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${usage}%"></div>
                </div>
                <div class="bin-stats">${bin.current_load}/${bin.capacity}</div>
            </div>
        `;
    }).join('');
}

// --- 2. CONVEYOR QUEUE ---
async function fetchQueue() {
    try {
        const res = await fetch(`${API_URL}/package/queue`);
        const data = await res.json();
        renderQueue(data.queue);
    } catch (e) { console.error(e); }
}

function renderQueue(queue) {
    if (queue.length === 0) {
        queueContainer.innerHTML = '<div class="empty-state">Queue is empty</div>';
        return;
    }
    queueContainer.innerHTML = queue.map(pkg => `
        <div class="queue-item">
            <div class="pkg-icon">📦</div>
            <div class="pkg-info">
                <strong>${pkg.tracking_id}</strong>
                <span>Size: ${pkg.size}</span>
            </div>
        </div>
    `).join('');
}

// --- 3. TRUCK STACK ---
async function fetchStack() {
    try {
        const res = await fetch(`${API_URL}/truck/status`);
        const data = await res.json();
        renderStack(data.stack);
    } catch (e) { console.error(e); }
}

function renderStack(stack) {
    if (stack.length === 0) {
        stackContainer.innerHTML = '<div class="empty-state">Truck is empty</div>';
        return;
    }
    // Stack should be rendered bottom-up visually, so we reverse for display if using flex-col-reverse or just map
    // Let's just map. CSS can handle order if needed, but standard list is fine.
    // LIFO: Last in is on top.
    stackContainer.innerHTML = stack.slice().reverse().map(pkg => `
        <div class="stack-item">
            <span>${pkg.tracking_id} (${pkg.size})</span>
            <span class="dest">${pkg.destination}</span>
        </div>
    `).join('');
}

// --- 4. LOGS ---
async function fetchLogs() {
    try {
        const res = await fetch(`${API_URL}/logs`);
        const data = await res.json();
        logContainer.innerHTML = data.logs.map(log => `<div class="log-entry">${log}</div>`).join('');
        // logContainer.scrollTop = logContainer.scrollHeight; // Auto scroll
    } catch (e) { console.error(e); }
}

// --- ACTIONS ---

// Add to Queue
ingestForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const pkg = {
        tracking_id: document.getElementById('pkgId').value,
        size: parseInt(document.getElementById('pkgSize').value),
        destination: document.getElementById('pkgDest').value
    };
    await fetch(`${API_URL}/package/add`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(pkg)
    });
    ingestForm.reset();
    refreshAll();
});

// Process Queue
processBtn.addEventListener('click', async () => {
    const res = await fetch(`${API_URL}/package/process`, { method: 'POST' });
    const data = await res.json();
    if (data.status === 'success') {
        // alert(data.message);
    } else {
        alert(data.message);
    }
    refreshAll();
});

// Load Truck Item
loadTruckBtn.addEventListener('click', async () => {
    const pkg = {
        tracking_id: document.getElementById('truckPkgId').value,
        size: parseInt(document.getElementById('truckPkgSize').value),
        destination: "Truck" // Dummy dest
    };
    if (!pkg.tracking_id || !pkg.size) return alert("Enter ID and Size");

    await fetch(`${API_URL}/truck/load`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(pkg)
    });
    document.getElementById('truckPkgId').value = '';
    document.getElementById('truckPkgSize').value = '';
    refreshAll();
});

// Rollback Truck
rollbackBtn.addEventListener('click', async () => {
    await fetch(`${API_URL}/truck/rollback?count=1`, { method: 'POST' });
    refreshAll();
});

// Check Fit (Planner)
checkFitBtn.addEventListener('click', async () => {
    const inputStr = document.getElementById('plannerInput').value;
    const capacity = parseInt(document.getElementById('plannerCap').value);

    try {
        // Allow simple format: 10, 20, 30 or JSON
        let packages = [];
        if (inputStr.trim().startsWith('[')) {
            const raw = JSON.parse(inputStr);
            packages = raw.map(p => ({ tracking_id: p.id || "TEST", size: p.size || p, destination: "PLAN" }));
        } else {
            // Assume comma separated sizes
            packages = inputStr.split(',').map((s, i) => ({
                tracking_id: `PLAN-${i}`,
                size: parseInt(s.trim()),
                destination: "PLAN"
            }));
        }

        const res = await fetch(`${API_URL}/truck/can-fit`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ capacity, packages })
        });
        const data = await res.json();

        plannerResult.className = `result-box ${data.status}`;
        plannerResult.innerHTML = `<strong>${data.message}</strong>`;

    } catch (e) {
        plannerResult.className = "result-box error";
        plannerResult.innerText = "Invalid Input Format";
    }
});

init();
