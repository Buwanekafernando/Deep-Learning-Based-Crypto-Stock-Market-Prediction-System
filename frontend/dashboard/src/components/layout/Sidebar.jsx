import React from 'react';
import {
    LayoutDashboard,
    BarChart3,
    History,
    Settings,
    TrendingUp,
    BrainCircuit,
    PieChart
} from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs) {
    return twMerge(clsx(inputs));
}

const navItems = [
    { icon: LayoutDashboard, label: 'Live Market', active: true },
    { icon: BarChart3, label: 'Model Comparison' },
    { icon: History, label: 'Backtesting' },
    { icon: BrainCircuit, label: 'Sentiment Analysis' },
    { icon: Settings, label: 'Settings' },
];

export const Sidebar = () => {
    return (
        <div className="flex flex-col w-64 h-screen bg-slate-900 border-r border-slate-800 p-4 fixed left-0 top-0">
            <div className="flex items-center gap-3 mb-10 px-2">
                <TrendingUp className="w-8 h-8 text-blue-500" />
                <h1 className="text-xl font-bold bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
                    Antigravity
                </h1>
            </div>

            <nav className="flex-1 space-y-2">
                {navItems.map((item) => (
                    <button
                        key={item.label}
                        className={cn(
                            "flex items-center gap-3 w-full px-4 py-3 rounded-xl transition-all duration-200 group text-sm font-medium",
                            item.active
                                ? "bg-blue-600/10 text-blue-400"
                                : "text-slate-400 hover:bg-slate-800 hover:text-slate-200"
                        )}
                    >
                        <item.icon className={cn(
                            "w-5 h-5 transition-colors",
                            item.active ? "text-blue-500" : "text-slate-500 group-hover:text-slate-300"
                        )} />
                        {item.label}
                    </button>
                ))}
            </nav>

            <div className="mt-auto p-4 bg-slate-800/50 rounded-2xl border border-slate-700/50">
                <div className="flex items-center gap-3 mb-2">
                    <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                    <span className="text-xs font-medium text-slate-300">System Live</span>
                </div>
                <p className="text-[10px] text-slate-500 leading-tight">
                    Binance WebSocket streaming active. Models ready for inference.
                </p>
            </div>
        </div>
    );
};
