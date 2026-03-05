import React from 'react';
import { Search, ChevronDown } from 'lucide-react';

const assets = [
    { symbol: 'BTCUSDT', name: 'Bitcoin', icon: '₿' },
    { symbol: 'ETHUSDT', name: 'Ethereum', icon: 'Ξ' },
    { symbol: 'AAPL', name: 'Apple Inc.', icon: '' },
    { symbol: 'TSLA', name: 'Tesla Inc.', icon: '⚡' },
];

export const AssetSelector = ({ selected, onSelect }) => {
    return (
        <div className="flex items-center gap-4">
            <div className="relative group">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 group-hover:text-blue-500 transition-colors" />
                <input
                    type="text"
                    placeholder="Search symbols..."
                    className="bg-slate-900 border border-slate-800 rounded-2xl py-2.5 pl-11 pr-4 text-sm focus:outline-none focus:border-blue-500/50 focus:ring-4 focus:ring-blue-500/5 transition-all w-64"
                />
            </div>

            <div className="flex gap-2">
                {assets.map((asset) => (
                    <button
                        key={asset.symbol}
                        onClick={() => onSelect(asset.symbol)}
                        className={`px-4 py-2.5 rounded-2xl border text-sm font-bold flex items-center gap-2 transition-all ${selected === asset.symbol
                                ? 'bg-blue-600 border-blue-500 text-white shadow-[0_0_20px_rgba(59,130,246,0.3)]'
                                : 'bg-slate-900 border-slate-800 text-slate-400 hover:border-slate-700 hover:text-slate-200'
                            }`}
                    >
                        <span className="text-lg leading-none opacity-80">{asset.icon}</span>
                        {asset.symbol}
                    </button>
                ))}
            </div>
        </div>
    );
};
