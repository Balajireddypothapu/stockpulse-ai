// StockPulse AI — Frontend JavaScript
const API = '';
let priceChart = null;
let rsiChart = null;

// ===== Initialize =====
document.addEventListener('DOMContentLoaded', async () => {
    await loadTrending();
    await loadCompare();
    document.getElementById('searchBtn').addEventListener('click', handleSearch);
    document.getElementById('searchInput').addEventListener('keydown', (e) => {
        if (e.key === 'Enter') handleSearch();
    });
});

function handleSearch() {
    const symbol = document.getElementById('searchInput').value.trim().toUpperCase();
    if (symbol) analyzeStock(symbol);
}

// ===== Load Trending =====
async function loadTrending() {
    try {
        const res = await fetch(`${API}/api/trending`);
        const data = await res.json();
        if (!data.success) return;

        const grid = document.getElementById('trendingGrid');
        grid.innerHTML = data.data.map(stock => `
            <div class="stock-card" onclick="analyzeStock('${stock.symbol}')">
                <div class="symbol">${stock.symbol}</div>
                <div class="name">${stock.name}</div>
                <div class="price">$${stock.price.toFixed(2)}</div>
                <div class="change ${stock.change >= 0 ? 'positive' : 'negative'}">
                    ${stock.change >= 0 ? '▲' : '▼'} ${Math.abs(stock.change_pct).toFixed(2)}%
                </div>
                <span class="sector-tag">${stock.sector}</span>
            </div>
        `).join('');
    } catch (e) {
        document.getElementById('trendingGrid').innerHTML = '<div class="loading">Failed to load</div>';
    }
}

// ===== Analyze Stock =====
async function analyzeStock(symbol) {
    const panel = document.getElementById('analysisPanel');
    panel.style.display = 'block';
    panel.scrollIntoView({ behavior: 'smooth' });

    try {
        // Fetch analysis and sentiment in parallel
        const [analysisRes, sentimentRes] = await Promise.all([
            fetch(`${API}/api/analyze/${symbol}?period=30`),
            fetch(`${API}/api/sentiment/${symbol}`)
        ]);

        const analysis = await analysisRes.json();
        const sentiment = await sentimentRes.json();

        if (!analysis.success) throw new Error(analysis.error);

        renderAnalysisHeader(analysis.data);
        renderPriceChart(analysis.data);
        renderRSIChart(analysis.data);

        if (sentiment.success) renderSentiment(sentiment.data);
    } catch (e) {
        document.getElementById('analysisHeader').innerHTML = `<p style="color:var(--red)">Error: ${e.message}</p>`;
    }
}

// ===== Render Analysis Header =====
function renderAnalysisHeader(data) {
    const changeClass = data.change >= 0 ? 'positive' : 'negative';
    const signalClass = `signal-${data.signal.toLowerCase()}`;

    document.getElementById('analysisHeader').innerHTML = `
        <div class="stock-info">
            <h2>${data.symbol} — ${data.name}</h2>
            <span class="subtitle">${data.sector} Sector</span>
        </div>
        <div class="price-info">
            <div class="current-price">$${data.current_price.toFixed(2)}</div>
            <div class="change-info ${changeClass}">
                ${data.change >= 0 ? '▲' : '▼'} $${Math.abs(data.change).toFixed(2)} (${Math.abs(data.change_pct).toFixed(2)}%)
            </div>
        </div>
        <span class="signal-badge ${signalClass}">${data.signal}</span>
        <div class="indicator-chips">
            <span class="chip">RSI: <strong>${data.rsi?.toFixed(1) || 'N/A'}</strong></span>
            <span class="chip">SMA5: <strong>$${data.sma_5?.toFixed(2) || 'N/A'}</strong></span>
            <span class="chip">SMA20: <strong>$${data.sma_20?.toFixed(2) || 'N/A'}</strong></span>
            <span class="chip">Vol: <strong>${(data.volume / 1e6).toFixed(1)}M</strong></span>
        </div>
    `;
}

// ===== Price Chart =====
function renderPriceChart(data) {
    if (priceChart) priceChart.destroy();
    const ctx = document.getElementById('priceChart').getContext('2d');
    const labels = data.prices.map(p => p.date.slice(5));
    const closes = data.prices.map(p => p.close);
    const sma5 = data.sma_5_series;
    const sma20 = data.sma_20_series;

    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: [
                { label: 'Close', data: closes, borderColor: '#6C63FF', borderWidth: 2, pointRadius: 0, fill: true, backgroundColor: 'rgba(108,99,255,0.08)' },
                { label: 'SMA 5', data: sma5, borderColor: '#22c55e', borderWidth: 1.5, pointRadius: 0, borderDash: [5, 3] },
                { label: 'SMA 20', data: sma20, borderColor: '#ef4444', borderWidth: 1.5, pointRadius: 0, borderDash: [5, 3] }
            ]
        },
        options: {
            responsive: true,
            plugins: { legend: { labels: { color: '#9ca3af', font: { size: 11 } } } },
            scales: {
                x: { ticks: { color: '#6b7280', maxTicksLimit: 8 }, grid: { color: 'rgba(255,255,255,0.03)' } },
                y: { ticks: { color: '#6b7280', callback: v => '$' + v.toFixed(0) }, grid: { color: 'rgba(255,255,255,0.03)' } }
            }
        }
    });
}

// ===== RSI Chart =====
function renderRSIChart(data) {
    if (rsiChart) rsiChart.destroy();
    const ctx = document.getElementById('rsiChart').getContext('2d');
    const labels = data.prices.map(p => p.date.slice(5));
    const rsi = data.rsi_series;

    rsiChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: [
                { label: 'RSI', data: rsi, borderColor: '#a855f7', borderWidth: 2, pointRadius: 0, fill: true, backgroundColor: 'rgba(168,85,247,0.08)' }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { labels: { color: '#9ca3af' } },
                annotation: { annotations: {} }
            },
            scales: {
                x: { ticks: { color: '#6b7280', maxTicksLimit: 8 }, grid: { color: 'rgba(255,255,255,0.03)' } },
                y: { min: 0, max: 100, ticks: { color: '#6b7280' }, grid: { color: 'rgba(255,255,255,0.03)' } }
            }
        }
    });
}

// ===== Sentiment =====
function renderSentiment(data) {
    document.getElementById('sentimentPanel').innerHTML = `
        <div class="sentiment-header">
            <h3><i class="fas fa-brain"></i> Sentiment Analysis — ${data.symbol}</h3>
            <span class="signal-badge signal-${data.overall.toLowerCase() === 'bullish' ? 'buy' : data.overall.toLowerCase() === 'bearish' ? 'sell' : 'hold'}">${data.overall}</span>
        </div>
        <div class="sentiment-bar-container">
            <div class="bullish" style="width:${data.bullish}%"></div>
            <div class="neutral" style="width:${data.neutral}%"></div>
            <div class="bearish" style="width:${data.bearish}%"></div>
        </div>
        <div class="sentiment-labels">
            <span style="color:var(--green)">🟢 Bullish ${data.bullish}%</span>
            <span>⚪ Neutral ${data.neutral}%</span>
            <span style="color:var(--red)">🔴 Bearish ${data.bearish}%</span>
        </div>
        <div class="headlines">
            <h4>Recent Headlines</h4>
            <ul>${data.headlines.map(h => `<li>${h}</li>`).join('')}</ul>
        </div>
    `;
}

// ===== Compare =====
async function loadCompare() {
    try {
        const res = await fetch(`${API}/api/compare?symbols=AAPL,GOOGL,MSFT,TSLA,NVDA`);
        const data = await res.json();
        if (!data.success) return;

        document.getElementById('compareTable').innerHTML = `
            <table>
                <thead>
                    <tr><th>Symbol</th><th>Name</th><th>Price</th><th>Change</th><th>RSI</th><th>Signal</th><th>Volume</th></tr>
                </thead>
                <tbody>
                    ${data.data.map(s => `
                        <tr onclick="analyzeStock('${s.symbol}')" style="cursor:pointer">
                            <td><strong style="color:var(--accent)">${s.symbol}</strong></td>
                            <td>${s.name}</td>
                            <td>$${s.price.toFixed(2)}</td>
                            <td style="color:${s.change_pct >= 0 ? 'var(--green)' : 'var(--red)'}">
                                ${s.change_pct >= 0 ? '▲' : '▼'} ${Math.abs(s.change_pct).toFixed(2)}%
                            </td>
                            <td>${s.rsi?.toFixed(1) || 'N/A'}</td>
                            <td><span class="signal-badge signal-${s.signal.toLowerCase()}">${s.signal}</span></td>
                            <td>${(s.volume / 1e6).toFixed(1)}M</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (e) {
        document.getElementById('compareTable').innerHTML = '<div class="loading">Failed to load</div>';
    }
}
