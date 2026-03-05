import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/layout/Sidebar';
import { StatCard } from './components/dashboard/StatCard';
import { ChartPanel } from './components/dashboard/ChartPanel';
import { RagExplainer } from './components/dashboard/RagExplainer';
import { AssetSelector } from './components/dashboard/AssetSelector';
import { BacktestChart } from './components/dashboard/BacktestChart';
import { useWebSocket } from './hooks/useWebSocket';
import {
  CircleDollarSign,
  Cpu,
  Layers,
  ChevronRight,
  Activity,
  Timer
} from 'lucide-react';

function App() {
  const [selectedAsset, setSelectedAsset] = useState('BTCUSDT');
  const { data, status } = useWebSocket('ws://localhost:8000/ws/market');
  const [history, setHistory] = useState([]);

  useEffect(() => {
    if (data?.price) {
      setHistory(prev => [...prev.slice(-29), data]);
    }
  }, [data]);

  const currentPrice = data?.price ? `$${data.price.toLocaleString()}` : '---';
  const prediction = data?.prediction ? `$${data.prediction.toLocaleString()}` : '---';
  const trend = data?.prediction && data?.price
    ? ((data.prediction - data.price) / data.price) * 100
    : 0;

  return (
    <div className="flex min-h-screen bg-[#020617] text-slate-200">
      <Sidebar />

      <main className="flex-1 ml-64 p-8">
        {/* Header Section */}
        <div className="flex justify-between items-center mb-10">
          <div>
            <div className="flex items-center gap-2 text-slate-500 mb-1">
              <span className="text-xs font-bold uppercase tracking-widest">Dashboard</span>
              <ChevronRight className="w-3 h-3" />
              <span className="text-xs font-bold uppercase tracking-widest text-blue-500">{selectedAsset}</span>
            </div>
            <h1 className="text-3xl font-black text-white px-1">Live Market Analysis</h1>
          </div>

          <div className="flex items-center gap-6">
            <AssetSelector selected={selectedAsset} onSelect={setSelectedAsset} />

            <div className="bg-slate-900 border border-slate-800 rounded-2xl px-5 py-2.5 flex items-center gap-3">
              <Timer className="w-4 h-4 text-slate-500" />
              <span className="text-sm font-bold tabular-nums">10:42:05 AM</span>
            </div>
          </div>
        </div>

        {/* Signal & Info Section */}
        <div className="flex items-center gap-4 mb-8">
          <div className={`px-4 py-2.5 rounded-2xl border flex items-center gap-3 font-bold text-sm tracking-wide shadow-xl ${trend > 0.05 ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-500' :
            trend < -0.05 ? 'bg-rose-500/10 border-rose-500/20 text-rose-500' :
              'bg-slate-800 border-slate-700 text-slate-400'
            }`}>
            <Activity className="w-4 h-4" />
            SIGNAL: {trend > 0.05 ? 'STRONG BUY' : trend < -0.05 ? 'STRONG SELL' : 'NEUTRAL / HOLD'}
          </div>

          <div className="bg-slate-900/50 border border-slate-800/60 rounded-2xl px-4 py-2.5 flex items-center gap-3 text-xs font-medium text-slate-400">
            <div className={`w-2 h-2 rounded-full ${status === 'connected' ? 'bg-emerald-500' : 'bg-rose-500'} animate-pulse`} />
            SERVER: {status === 'connected' ? 'OK' : 'DISCONNECTED'}
          </div>
        </div>

        {/* Dashboard Grid */}
        <div className="grid grid-cols-12 gap-8 mb-8">
          <div className="col-span-3">
            <StatCard
              label="Current Market Price"
              value={currentPrice}
              trend={0}
              icon={CircleDollarSign}
              color="blue"
            />
          </div>
          <div className="col-span-3">
            <StatCard
              label="LSTM Next Step Prediction"
              value={prediction}
              subValue="Confidence: High"
              trend={trend}
              icon={Cpu}
              color="purple"
            />
          </div>
          <div className="col-span-3">
            <StatCard
              label="MAE (Sequential Error)"
              value={data?.metrics?.MAE?.toFixed(4) || "---"}
              trend={-1.2}
              icon={Layers}
              color="amber"
            />
          </div>
          <div className="col-span-3">
            <StatCard
              label="RMSE (L2 Variance)"
              value={data?.metrics?.RMSE?.toFixed(4) || "---"}
              trend={-0.8}
              icon={Layers}
              color="emerald"
            />
          </div>

          {/* Main Chart Section */}
          <div className="col-span-8 h-[550px]">
            <ChartPanel dataHistory={history} />
          </div>

          {/* Side Panel Section */}
          <div className="col-span-4 h-[550px]">
            <RagExplainer explanation={data?.explanation} />
          </div>
        </div>

        {/* Backtesting Performance Section */}
        <div className="grid grid-cols-1 gap-8">
          <BacktestChart />
        </div>
      </main>
    </div>
  );
}

export default App;
