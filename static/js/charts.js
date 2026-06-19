// Charting Utilities for Stock Analyzer using Chart.js

let allocationChartInstance = null;
let stockChartInstance = null;
let rsiChartInstance = null;

// Render Asset Allocation Doughnut Chart on Dashboard
function renderAllocationChart(canvasId, allocationList) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    // Destroy previous instance
    if (allocationChartInstance) {
        allocationChartInstance.destroy();
    }
    
    // Filter out assets with 0 balance
    const activeAssets = allocationList.filter(item => item.value > 0);
    
    const labels = activeAssets.map(item => item.asset);
    const dataValues = activeAssets.map(item => item.value);
    
    // Premium color palette for assets
    const colors = [
        '#10b981', // Cash (Emerald)
        '#3b82f6', // Blue
        '#8b5cf6', // Violet
        '#ec4899', // Pink
        '#f59e0b', // Amber
        '#06b6d4', // Cyan
        '#14b8a6', // Teal
        '#f43f5e', // Rose
        '#a855f7'  /* Purple */
    ];
    
    allocationChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: dataValues,
                backgroundColor: colors.slice(0, labels.length),
                borderWidth: 2,
                borderColor: '#111827',
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#9ca3af',
                        font: {
                            family: 'Plus Jakarta Sans',
                            size: 12
                        },
                        padding: 15
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const val = context.raw;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const pct = ((val / total) * 100).toFixed(1);
                            return ` ${context.label}: ${formatCurrency(val)} (${pct}%)`;
                        }
                    }
                }
            },
            cutout: '65%'
        }
    });
}

// Render historical stock details line chart
function renderStockChart(priceCanvasId, rsiCanvasId, stockData, activeIndicators = {}) {
    const priceCtx = document.getElementById(priceCanvasId);
    if (!priceCtx) return;
    
    if (stockChartInstance) {
        stockChartInstance.destroy();
    }
    if (rsiChartInstance) {
        rsiChartInstance.destroy();
    }
    
    const labels = Array.from({length: stockData.prices.length}, (_, i) => `Day ${i + 1}`);
    
    // Main datasets array starting with Price
    const datasets = [{
        label: `${stockData.ticker} Price`,
        data: stockData.prices,
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.05)',
        borderWidth: 2.5,
        fill: true,
        tension: 0.15,
        pointRadius: 1,
        pointHoverRadius: 5
    }];
    
    // Add Simple Moving Averages if active
    if (activeIndicators.sma_10) {
        datasets.push({
            label: '10-day SMA',
            data: stockData.sma_10,
            borderColor: '#10b981',
            borderWidth: 1.5,
            borderDash: [5, 5],
            pointRadius: 0,
            fill: false,
            tension: 0.1
        });
    }
    if (activeIndicators.sma_20) {
        datasets.push({
            label: '20-day SMA',
            data: stockData.sma_20,
            borderColor: '#f59e0b',
            borderWidth: 1.5,
            borderDash: [5, 5],
            pointRadius: 0,
            fill: false,
            tension: 0.1
        });
    }
    
    // Add Exponential Moving Averages if active
    if (activeIndicators.ema_12) {
        datasets.push({
            label: '12-day EMA',
            data: stockData.ema_12,
            borderColor: '#8b5cf6',
            borderWidth: 1.5,
            pointRadius: 0,
            fill: false,
            tension: 0.1
        });
    }
    if (activeIndicators.ema_26) {
        datasets.push({
            label: '26-day EMA',
            data: stockData.ema_26,
            borderColor: '#ec4899',
            borderWidth: 1.5,
            pointRadius: 0,
            fill: false,
            tension: 0.1
        });
    }
    
    // Create Main Price Chart
    stockChartInstance = new Chart(priceCtx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        color: '#9ca3af',
                        font: { family: 'Plus Jakarta Sans', size: 11 }
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            return ` ${context.dataset.label}: ${formatCurrency(context.raw)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.03)' },
                    ticks: { color: '#6b7280', font: { family: 'Plus Jakarta Sans' } }
                },
                y: {
                    grid: { color: 'rgba(255, 255, 255, 0.03)' },
                    ticks: { 
                        color: '#6b7280', 
                        font: { family: 'Plus Jakarta Sans' },
                        callback: function(value) { return '$' + value; }
                    }
                }
            }
        }
    });

    // Create secondary RSI chart if canvas exists and active
    const rsiCtx = document.getElementById(rsiCanvasId);
    const rsiContainer = rsiCtx ? rsiCtx.parentElement : null;
    
    if (rsiCtx && rsiContainer) {
        if (activeIndicators.rsi) {
            rsiContainer.style.display = 'block';
            rsiChartInstance = new Chart(rsiCtx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'RSI (14)',
                        data: stockData.rsi_14,
                        borderColor: '#a855f7',
                        borderWidth: 2,
                        pointRadius: 0,
                        tension: 0.1,
                        fill: false
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: {
                            grid: { color: 'rgba(255, 255, 255, 0.03)' },
                            ticks: { display: false }
                        },
                        y: {
                            min: 0,
                            max: 100,
                            grid: { color: 'rgba(255, 255, 255, 0.05)' },
                            ticks: { 
                                stepSize: 30,
                                color: '#6b7280',
                                font: { family: 'Plus Jakarta Sans', size: 10 }
                            }
                        }
                    }
                }
            });
        } else {
            rsiContainer.style.display = 'none';
        }
    }
}
