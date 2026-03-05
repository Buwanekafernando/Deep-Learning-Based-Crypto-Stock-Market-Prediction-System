import React from 'react';
import { Sparkles, Info, MessageSquareQuote } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export const RagExplainer = ({ explanation }) => {
    return (
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl h-full flex flex-col relative overflow-hidden group">
            {/* Decorative accent */}
            <div className="absolute top-0 right-0 w-32 h-32 bg-purple-500/5 blur-3xl" />

            <div className="flex items-center gap-3 mb-6">
                <div className="p-3 bg-purple-500/10 border border-purple-500/20 rounded-2xl text-purple-500">
                    <Sparkles className="w-5 h-5" />
                </div>
                <div>
                    <h2 className="text-xl font-bold text-white">Model Reasoning</h2>
                    <p className="text-xs text-slate-500 tracking-wide">Contextual RAG-based analysis</p>
                </div>
            </div>

            <div className="flex-1 overflow-y-auto space-y-4 pr-2">
                <AnimatePresence mode='wait'>
                    {explanation ? (
                        <motion.div
                            key={explanation}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            className="relative p-5 bg-slate-800/40 border border-slate-700/50 rounded-2xl"
                        >
                            <MessageSquareQuote className="absolute -top-2 -left-2 w-6 h-6 text-slate-700 bg-slate-900 rounded-full p-1" />
                            <p className="text-sm text-slate-300 leading-relaxed indent-4">
                                {explanation}
                            </p>
                        </motion.div>
                    ) : (
                        <div className="flex flex-col items-center justify-center h-full text-center space-y-3 py-10 opacity-40">
                            <Info className="w-10 h-10 text-slate-500" />
                            <p className="text-sm text-slate-500 px-10">
                                Waiting for the next market tick to generate reasoning insights...
                            </p>
                        </div>
                    )}
                </AnimatePresence>
            </div>

            {/* Action Footer */}
            <div className="mt-6 pt-6 border-t border-slate-800/60 flex items-center justify-between text-[10px] text-slate-500 uppercase tracking-widest font-bold">
                <span>Sentiment Source: NewsAPI</span>
                <span>Confidence: 94.2%</span>
            </div>
        </div>
    );
};
