import React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs) {
    return twMerge(clsx(inputs));
}

export const StatCard = ({ label, value, subValue, trend, icon: Icon, color = "blue" }) => {
    const isPositive = trend > 0;
    const isNegative = trend < 0;

    const colorVariants = {
        blue: "text-blue-500 bg-blue-500/10 border-blue-500/20",
        emerald: "text-emerald-500 bg-emerald-500/10 border-emerald-500/20",
        rose: "text-rose-500 bg-rose-500/10 border-rose-500/20",
        purple: "text-purple-500 bg-purple-500/10 border-purple-500/20",
        amber: "text-amber-500 bg-amber-500/10 border-amber-500/20",
    };

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl hover:border-slate-700 transition-colors group relative overflow-hidden">
            {/* Background Glow */}
            <div className={cn(
                "absolute -right-4 -top-4 w-24 h-24 blur-3xl rounded-full opacity-10 group-hover:opacity-20 transition-opacity",
                color === "blue" && "bg-blue-500",
                color === "emerald" && "bg-emerald-500",
                color === "rose" && "bg-rose-500",
                color === "purple" && "bg-purple-500",
                color === "amber" && "bg-amber-500"
            )} />

            <div className="flex justify-between items-start mb-4">
                <div className={cn("p-3 rounded-2xl border", colorVariants[color])}>
                    <Icon className="w-5 h-5" />
                </div>

                {trend !== undefined && (
                    <div className={cn(
                        "flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-bold",
                        isPositive ? "bg-emerald-500/10 text-emerald-500" :
                            isNegative ? "bg-rose-500/10 text-rose-500" :
                                "bg-slate-800 text-slate-400"
                    )}>
                        {isPositive && <TrendingUp className="w-3 h-3" />}
                        {isNegative && <TrendingDown className="w-3 h-3" />}
                        {!isPositive && !isNegative && <Minus className="w-3 h-3" />}
                        {Math.abs(trend).toFixed(2)}%
                    </div>
                )}
            </div>

            <div>
                <h3 className="text-slate-500 text-sm font-medium mb-1">{label}</h3>
                <div className="flex items-baseline gap-2">
                    <span className="text-2xl font-bold text-white tracking-tight">
                        {value}
                    </span>
                    {subValue && (
                        <span className="text-xs text-slate-500 font-medium">
                            {subValue}
                        </span>
                    )}
                </div>
            </div>
        </div>
    );
};
