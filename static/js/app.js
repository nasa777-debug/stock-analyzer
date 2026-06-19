// Common Application Scripts for Stock Analyzer

// Formatting helpers
function formatCurrency(val) {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(val);
}

function formatPercent(val) {
    const sign = val >= 0 ? '+' : '';
    return `${sign}${val.toFixed(2)}%`;
}

// Global Poll interval
let pricePollInterval = null;

// Start price polling to update the top ticker marquee
function startPriceTicker() {
    fetchTickerData();
    // Poll every 4 seconds to simulate real-time updates
    pricePollInterval = setInterval(fetchTickerData, 4000);
}

function fetchTickerData() {
    fetch('/api/stocks')
        .then(response => {
            if (!response.ok) throw new Error('Network error');
            return response.json();
        })
        .then(stocks => {
            updateTickerUI(stocks);
            // Fire custom event so pages can listen to price updates
            const event = new CustomEvent('pricesUpdated', { detail: stocks });
            document.dispatchEvent(event);
        })
        .catch(err => console.error('Error fetching ticker:', err));
}

function updateTickerUI(stocks) {
    const tickerContent = document.getElementById('ticker-content');
    if (!tickerContent) return;
    
    // Clear old elements
    tickerContent.innerHTML = '';
    
    // We duplicate the list to make the marquee scrolling seamless
    const doubleStocks = [...stocks, ...stocks];
    
    doubleStocks.forEach(stock => {
        const item = document.createElement('div');
        item.className = 'ticker-item';
        item.onclick = () => {
            window.location.href = `/market?symbol=${stock.ticker}`;
        };
        
        const isUp = stock.change_pct >= 0;
        const changeClass = isUp ? 'up' : 'down';
        const icon = isUp ? '▲' : '▼';
        
        item.innerHTML = `
            <span class="ticker-symbol">${stock.ticker}</span>
            <span class="ticker-price">${formatCurrency(stock.price)}</span>
            <span class="ticker-change ${changeClass}">${icon} ${Math.abs(stock.change_pct).toFixed(2)}%</span>
        `;
        tickerContent.appendChild(item);
    });
}

// Show standard toast/alert notifications
function showNotification(message, type = 'info') {
    // Check if toast container exists, if not create it
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.style.position = 'fixed';
        container.style.bottom = '20px';
        container.style.right = '20px';
        container.style.zIndex = '9999';
        container.style.display = 'flex';
        container.style.flexDirection = 'column';
        container.style.gap = '10px';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `flash-msg ${type}`;
    toast.style.margin = '0';
    toast.style.boxShadow = '0 4px 12px rgba(0,0,0,0.5)';
    toast.style.minWidth = '280px';
    
    const icon = type === 'success' ? '✓' : type === 'error' ? '✗' : 'ℹ';
    
    toast.innerHTML = `
        <span style="font-weight: bold; font-size: 16px;">${icon}</span>
        <span>${message}</span>
    `;
    
    container.appendChild(toast);
    
    // Auto-remove after 4 seconds
    setTimeout(() => {
        toast.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        setTimeout(() => toast.remove(), 500);
    }, 4000);
}

// Initialize Ticker when DOM loaded
document.addEventListener('DOMContentLoaded', () => {
    startPriceTicker();
});
