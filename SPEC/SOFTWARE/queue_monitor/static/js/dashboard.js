const API_BASE = '';
const UPDATE_INTERVAL = 2000;

let isConnected = false;

function updateConnectionStatus(connected) {
    isConnected = connected;
    const statusDot = document.getElementById('connection-status');
    const statusText = document.getElementById('connection-text');
    
    if (connected) {
        statusDot.classList.add('connected');
        statusText.textContent = 'Connected';
    } else {
        statusDot.classList.remove('connected');
        statusText.textContent = 'Disconnected';
    }
}

async function fetchStats() {
    try {
        const response = await fetch(`${API_BASE}/api/stats`);
        if (!response.ok) throw new Error('Failed to fetch stats');
        
        const data = await response.json();
        updateDashboard(data);
        updateConnectionStatus(true);
    } catch (error) {
        console.error('Error fetching stats:', error);
        updateConnectionStatus(false);
    }
}

function updateDashboard(data) {
    document.getElementById('current-count').innerHTML = data.current_count || 0;
    document.getElementById('queue-count-overlay').textContent = data.current_count || 0;
    document.getElementById('wait-time').innerHTML = `${data.wait_time_minutes || 0} <span>min</span>`;
    document.getElementById('peak-count').textContent = data.peak_count || 0;
    document.getElementById('avg-count').textContent = data.average_count || 0;
    document.getElementById('last-update').textContent = new Date(data.timestamp).toLocaleTimeString();
    
    const statusBadge = document.getElementById('status-badge');
    statusBadge.textContent = data.status || 'UNKNOWN';
    statusBadge.className = `status-badge ${data.status || 'UNKNOWN'}`;
    
    const trendElement = document.getElementById('trend');
    trendElement.textContent = data.trend || 'STABLE';
    trendElement.className = `trend-value ${data.trend || 'STABLE'}`;
    
    if (data.recommendation) {
        updateRecommendation(data.recommendation);
    }
    
    if (data.shelf_status) {
        updateShelfStatus(data.shelf_status);
    }
}

function updateRecommendation(rec) {
    const recElement = document.getElementById('recommendation');
    
    const actionColors = {
        'ADD_STAFF': '#ff4757',
        'MAINTAIN': '#2ed573',
        'REDUCE': '#ffa502'
    };
    
    const actionIcons = {
        'ADD_STAFF': '+',
        'MAINTAIN': '=',
        'REDUCE': '-'
    };
    
    const html = `
        <div class="rec-grid">
            <div class="rec-item">
                <span class="rec-label">Current Staff</span>
                <span class="rec-value">${rec.current_staff}</span>
            </div>
            <div class="rec-item">
                <span class="rec-label">Recommended</span>
                <span class="rec-value" style="color: ${actionColors[rec.action]}">${rec.recommended_staff}</span>
            </div>
            <div class="rec-item">
                <span class="rec-label">Action</span>
                <span class="rec-action" style="background: ${actionColors[rec.action]}">
                    ${actionIcons[rec.action]} ${rec.action.replace('_', ' ')}
                </span>
            </div>
        </div>
        <p class="rec-message">${rec.message}</p>
    `;
    
    recElement.innerHTML = html;
}

function updateShelfStatus(stats) {
    const statusEl = document.getElementById('shelf-overall-status');
    const alertEl = document.getElementById('shelf-alert');
    const alertTextEl = document.getElementById('shelf-alert-text');
    const gridEl = document.getElementById('shelf-grid');
    
    if (!stats || !stats.shelves || stats.shelves.length === 0) {
        statusEl.textContent = 'NO DATA';
        statusEl.className = 'shelf-status-badge ok';
        alertEl.style.display = 'none';
        gridEl.innerHTML = '<p class="loading">Configure shelves in config.yaml</p>';
        return;
    }
    
    statusEl.textContent = stats.overall_status || 'OK';
    statusEl.className = 'shelf-status-badge ' + (stats.overall_status || 'ok').toLowerCase();
    
    if (stats.alerts_needed > 0) {
        alertEl.style.display = 'block';
        let alertMsg = stats.alerts_needed + ' shelf';
        if (stats.alerts_needed > 1) alertMsg += 'es';
        alertMsg += ' need attention';
        if (stats.empty_count > 0) alertMsg += ` (${stats.empty_count} empty)`;
        if (stats.low_stock_count > 0) alertMsg += ` (${stats.low_stock_count} low)`;
        alertTextEl.textContent = alertMsg;
    } else {
        alertEl.style.display = 'none';
    }
    
    let gridHtml = '';
    stats.shelves.forEach(shelf => {
        const statusClass = shelf.status === 'FULL' ? 'full' : (shelf.status === 'LOW STOCK' ? 'low' : 'empty');
        const itemClass = shelf.status === 'FULL' ? '' : (shelf.status === 'LOW STOCK' ? 'low-stock' : 'empty');
        
        gridHtml += `
            <div class="shelf-item ${itemClass}">
                <div class="shelf-item-header">
                    <span class="shelf-item-name">${shelf.name}</span>
                    <span class="shelf-item-status ${statusClass}">${shelf.status}</span>
                </div>
                <div class="shelf-bar">
                    <div class="shelf-fill ${statusClass === 'low' ? 'low' : ''} ${statusClass === 'empty' ? 'empty' : ''}" 
                         style="width: ${shelf.fill_percentage}%"></div>
                </div>
                <div class="shelf-item-footer">
                    <span>Fill Level</span>
                    <span>${shelf.fill_percentage}%</span>
                </div>
            </div>
        `;
    });
    
    gridEl.innerHTML = gridHtml;
}

function refreshVideoFeed() {
    const videoImg = document.getElementById('video-feed');
    const timestamp = new Date().getTime();
    videoImg.src = `${API_BASE}/api/frame/annotated?t=${timestamp}`;
}

async function resetStats() {
    try {
        const response = await fetch(`${API_BASE}/api/reset`, { method: 'POST' });
        if (response.ok) {
            alert('Statistics reset successfully');
        }
    } catch (error) {
        console.error('Error resetting stats:', error);
    }
}

document.getElementById('reset-btn').addEventListener('click', resetStats);

videoImg = document.getElementById('video-feed');
videoImg.addEventListener('error', () => {
    setTimeout(refreshVideoFeed, 1000);
});

setInterval(fetchStats, UPDATE_INTERVAL);
setInterval(refreshVideoFeed, 5000);

fetchStats();
refreshVideoFeed();
