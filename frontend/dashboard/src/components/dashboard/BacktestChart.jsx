import React from 'react';
import Chart from 'react-apexcharts';
import { TrendingUp, Scale } from 'lucide-react';

export const BacktestChart = () => {
    const options = {
        chart: {
            type: 'area',
            background: 'transparent',
            toolbar: { show: false },
            zoom: { enabled: false }
        },
        colors: ['#3b82f6', '#94a3b8'], // High-contrast Blue and Slate
        dataLabels: { enabled: false },
        stroke: { curve: 'smooth', width: 2 },
        fill: {
            type: 'gradient',
            gradient: {
                shadeIntensity: 1,
                opacityFrom: 0.45,
                opacityTo: 0.05,
                stops: [20, 100]
            }
        },
        xaxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            labels: { style: { colors: '#64748b' } },
            axisBorder: { show: false }
        },
        yaxis: {
            labels: { style: { colors: '#64748b' } }
        },
        grid: {
            borderColor: '#1e293b',
            strokeDashArray: 4
        },
        legend: {
            position: 'top',
            horizontalAlign: 'right',
            labels: { colors: '#f1f5f9' }
        }
    };

    const series = [
        {
            name: 'LSTM Strategy',
            data: [30, 40, 35, 50, 49, 60, 70]
        },
        {
            name: 'Buy & Hold',
            data: [30, 32, 28, 35, 40, 38, 45]
        }
    ];

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-xl">
            <div className="flex justify-between items-center mb-6">
                <div className="flex items-center gap-3">
                    <div className="p-2.5 bg-blue-500/10 border border-blue-500/20 rounded-xl text-blue-500">
                        <TrendingUp className="w-5 h-5" />
                    </div>
                    <div>
                        <h2 className="text-xl font-bold text-white">Backtesting Performance</h2>
                        <p className="text-xs text-slate-500">Equity curve comparison (7-month window)</p>
                    </div>
                </div>
                <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-800/50 rounded-lg text-xs font-bold text-slate-300">
                    <Scale className="w-4 h-4 text-slate-500" />
                    ALPHA: +25.4%
                </div>
            </div>

            <div className="h-[300px]">
                <Chart options={options} series={series} type="area" height="100%" />
            </div>
        </div>
    );
};
