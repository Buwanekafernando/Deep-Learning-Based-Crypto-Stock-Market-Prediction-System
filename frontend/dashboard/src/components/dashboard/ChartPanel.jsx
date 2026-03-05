import React from 'react';
import Chart from 'react-apexcharts';
import { Maximize2, RefreshCw } from 'lucide-react';

export const ChartPanel = ({ dataHistory }) => {
    // dataHistory is an array of market updates from WebSocket

    const options = {
        chart: {
            type: 'candlestick',
            background: 'transparent',
            toolbar: { show: false },
            animations: { enabled: false }
        },
        theme: { mode: 'dark' },
        xaxis: {
            type: 'datetime',
            labels: { style: { colors: '#64748b' } },
            axisBorder: { show: false },
            axisTicks: { show: false }
        },
        yaxis: {
            tooltip: { enabled: true },
            labels: { style: { colors: '#64748b' } }
        },
        grid: {
            borderColor: '#1e293b',
            strokeDashArray: 4,
            xaxis: { lines: { show: true } }
        },
        plotOptions: {
            candlestick: {
                colors: {
                    upward: '#10b981',
                    downward: '#ef4444'
                },
                wick: { useFillColor: true }
            }
        },
        annotations: {
            // Future: Add prediction markers here
        }
    };

    // Convert history into candlestick series
    const series = [{
        name: 'Price',
        data: dataHistory.map(item => ({
            x: new Date().getTime(), // In real app, use timestamp from data
            y: [item.price * 0.999, item.price * 1.001, item.price * 0.998, item.price] // Dummy OHLC if not provided
        }))
    }];

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl h-full flex flex-col">
            <div className="flex justify-between items-center mb-6">
                <div>
                    <h2 className="text-xl font-bold text-white">Market Chart</h2>
                    <p className="text-xs text-slate-500">Real-time BTC/USDT technical analysis</p>
                </div>
                <div className="flex gap-2">
                    <button className="p-2 bg-slate-800 border border-slate-700 rounded-xl text-slate-400 hover:text-white transition-colors">
                        <RefreshCw className="w-4 h-4" />
                    </button>
                    <button className="p-2 bg-slate-800 border border-slate-700 rounded-xl text-slate-400 hover:text-white transition-colors">
                        <Maximize2 className="w-4 h-4" />
                    </button>
                </div>
            </div>

            <div className="flex-1 min-h-[400px]">
                <Chart
                    options={options}
                    series={series}
                    type="candlestick"
                    height="100%"
                />
            </div>
        </div>
    );
};
