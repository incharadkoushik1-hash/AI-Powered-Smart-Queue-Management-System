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
