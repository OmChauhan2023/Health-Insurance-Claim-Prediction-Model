import React from 'react';
import { GitBranch, Layers, Shuffle, Target, Cpu, Activity, Database, Zap, Settings, ArrowDown } from 'lucide-react';

const pipeline = [
  { 
    step: '01', 
    title: 'Data & Feature Engineering', 
    icon: Database, 
    theme: 'pink', 
    gradient: 'from-pink-500 to-rose-500', 
    glow: 'shadow-pink-500/20',
    desc: 'ZebraFeatureEngineer creates complex interaction terms. ZebraImputer resolves missing data.' 
  },
  { 
    step: '02', 
    title: '5-Fold Stratified CV', 
    icon: Shuffle, 
    theme: 'orange', 
    gradient: 'from-orange-400 to-amber-500', 
    glow: 'shadow-orange-500/20',
    desc: 'OOF Target Encoding, SMOTE, and strict in-fold Feature Selection to prevent leakage.' 
  },
  { 
    step: '03', 
    title: 'Base Models (OOF)', 
    icon: Cpu, 
    theme: 'cyan', 
    gradient: 'from-cyan-400 to-blue-500', 
    glow: 'shadow-cyan-500/20',
    desc: 'LightGBM, XGBoost, and CatBoost generate Out-Of-Fold predictions.' 
  },
  { 
    step: '04', 
    title: 'Stacking Meta-Learner', 
    icon: Layers, 
    theme: 'indigo', 
    gradient: 'from-indigo-500 to-violet-500', 
    glow: 'shadow-indigo-500/20',
    desc: 'A secondary LightGBM model learns complex patterns from the base model outputs.' 
  },
  { 
    step: '05', 
    title: 'Isotonic Calibration', 
    icon: Target, 
    theme: 'emerald', 
    gradient: 'from-emerald-400 to-teal-500', 
    glow: 'shadow-emerald-500/20',
    desc: 'Probabilities are calibrated to maximize the final Gini coefficient accurately.' 
  },
];

const ModelDev = () => {
  return (
    <div className="flex flex-col gap-10 pb-16">
      
      {/* Sleek inline header */}
      <div className="flex items-end justify-between border-b border-zinc-200 dark:border-zinc-800 pb-4">
        <div>
          <div className="flex items-center gap-2 text-blue-600 dark:text-blue-400 font-bold tracking-widest text-xs uppercase mb-1">
            <Zap size={14} /> Architecture Deep Dive
          </div>
          <h2 className="text-3xl font-extrabold text-zinc-900 dark:text-zinc-50 tracking-tight">
            ZEBRA Training Pipeline
          </h2>
        </div>
        <div className="text-right hidden md:block">
          <p className="text-sm text-zinc-500 dark:text-zinc-400 uppercase tracking-widest font-semibold">Final Gini Score</p>
          <p className="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-500 to-teal-400">0.2860</p>
        </div>
      </div>

      {/* Main Grid: Flowchart + Sidebar */}
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-10">
        
        {/* Left Side: The "Roadmap" Alternating Flowchart (8 cols) */}
        <div className="xl:col-span-8 relative py-8">
          
          {/* Central glowing spine */}
          <div className="absolute left-[24px] md:left-1/2 top-0 bottom-0 w-1.5 -translate-x-1/2 bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-[150%] bg-gradient-to-b from-pink-500 via-cyan-500 to-emerald-500 animate-[spin_4s_linear_infinite] opacity-50 blur-[2px]" />
            <div className="absolute top-0 left-0 w-full h-[150%] bg-gradient-to-b from-pink-500 via-cyan-500 to-emerald-500 opacity-80" />
          </div>

          <div className="flex flex-col gap-12 relative z-10">
            {pipeline.map((p, idx) => {
              const isEven = idx % 2 === 0;
              return (
                <div key={p.step} className={`flex flex-col md:flex-row items-center gap-6 md:gap-12 w-full group ${!isEven ? 'md:flex-row-reverse' : ''}`}>
                  
                  {/* Empty space for alternating layout on desktop */}
                  <div className="hidden md:block flex-1" />

                  {/* Central Node */}
                  <div className={`relative shrink-0 w-12 h-12 rounded-full border-4 border-white dark:border-[#0c0c0f] shadow-xl z-20 flex items-center justify-center bg-gradient-to-br ${p.gradient} transition-transform duration-300 group-hover:scale-125`}>
                    <p className="text-white font-black text-sm">{p.step}</p>
                    {/* Glowing pulse ring */}
                    <div className={`absolute inset-0 rounded-full bg-gradient-to-br ${p.gradient} blur-md opacity-0 group-hover:opacity-100 transition-opacity duration-300 -z-10`} />
                  </div>

                  {/* Content Card */}
                  <div className="flex-1 w-full md:w-auto relative perspective-1000">
                    {/* Connector Arrow (Desktop) */}
                    <div className={`hidden md:block absolute top-1/2 -translate-y-1/2 w-8 border-t-2 border-dashed border-zinc-300 dark:border-zinc-700 ${isEven ? '-left-12' : '-right-12'}`} />
                    
                    <div className={`bg-white dark:bg-[#0c0c0f] border border-zinc-200 dark:border-zinc-800 rounded-[20px] p-6 shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all duration-300 relative overflow-hidden group-hover:border-${p.theme}-400/50`}>
                      {/* Subtle background glow based on theme */}
                      <div className={`absolute -right-12 -top-12 w-32 h-32 bg-${p.theme}-500 opacity-[0.03] dark:opacity-10 rounded-full blur-3xl group-hover:opacity-20 transition-opacity`} />
                      
                      <div className="flex items-center gap-4 mb-3">
                        <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${p.gradient} flex items-center justify-center text-white shadow-lg ${p.glow}`}>
                          <p.icon size={20} />
                        </div>
                        <h4 className="text-xl font-black text-zinc-900 dark:text-zinc-50">{p.title}</h4>
                      </div>
                      <p className="text-sm text-zinc-500 dark:text-zinc-400 leading-relaxed font-medium">
                        {p.desc}
                      </p>
                    </div>
                  </div>
                  
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Side: Informational Sidebar (4 cols) */}
        <div className="xl:col-span-4 flex flex-col gap-6">
          
          {/* Base Models Overhaul */}
          <div className="bg-white dark:bg-[#0c0c0f] rounded-3xl p-1 relative overflow-hidden shadow-xl border border-zinc-200 dark:border-zinc-800">
            {/* Glowing background blob */}
            <div className="absolute -top-20 -right-20 w-64 h-64 bg-gradient-to-br from-blue-400 via-purple-400 to-rose-400 opacity-20 dark:opacity-30 blur-3xl rounded-full" />
            
            <div className="relative bg-white/60 dark:bg-zinc-900/60 backdrop-blur-xl rounded-[22px] p-6 h-full">
              <h3 className="font-bold text-zinc-900 dark:text-white mb-2 flex items-center gap-2">
                <Cpu size={18} className="text-purple-600 dark:text-purple-400" /> Base Meta-Features
              </h3>
              <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed mb-6">
                These three algorithms generate the initial "guesses" (meta-features). The final Stacking model learns which algorithm to trust the most based on their <strong>Importance</strong> weight.
              </p>
              
              <div className="space-y-6">
                {[
                  { name: 'CatBoost', gini: '0.278', weight: '43.4%', color: 'from-emerald-400 to-emerald-500' },
                  { name: 'LightGBM', gini: '0.278', weight: '42.1%', color: 'from-blue-400 to-blue-500' },
                  { name: 'XGBoost',  gini: '0.277', weight: '14.5%', color: 'from-rose-400 to-rose-500' },
                ].map(m => (
                  <div key={m.name} className="group">
                    <div className="flex justify-between items-end mb-2">
                      <span className="font-bold text-zinc-800 dark:text-zinc-200">{m.name}</span>
                      <div className="text-right">
                        <span className="text-[10px] text-zinc-500 uppercase tracking-wider block leading-none mb-1">Importance</span>
                        <span className="text-sm font-black text-zinc-800 dark:text-zinc-200">{m.weight}</span>
                      </div>
                    </div>
                    {/* Glassy progress bar */}
                    <div className="h-2.5 w-full bg-zinc-100 dark:bg-zinc-950 rounded-full overflow-hidden shadow-inner border border-zinc-200/50 dark:border-white/5">
                      <div className={`h-full bg-gradient-to-r ${m.color} rounded-full relative`} style={{ width: m.weight }}>
                        <div className="absolute top-0 right-0 bottom-0 w-4 bg-white/40 rounded-full animate-pulse" />
                      </div>
                    </div>
                    <p className="text-[11px] font-semibold text-zinc-500 dark:text-zinc-400 mt-1.5">OOF Gini: <span className="font-mono text-zinc-700 dark:text-zinc-300">{m.gini}</span></p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Config & Feature Stats */}
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-1 gap-4">
            {/* Settings */}
            <div className="bg-white dark:bg-[#0c0c0f] border border-zinc-200 dark:border-zinc-800 rounded-3xl p-6 shadow-sm">
              <h3 className="font-bold text-zinc-900 dark:text-zinc-100 mb-2 flex items-center gap-2">
                <Settings size={18} className="text-zinc-400" /> Preprocessing
              </h3>
              <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed mb-4">
                Raw data is often imbalanced and noisy. These settings ensure the data is strictly balanced and cleaned to prevent the AI from becoming biased toward the majority class.
              </p>
              <div className="flex flex-col gap-3">
                {[
                  ['SMOTE Ratio', '0.05'],
                  ['Under-sampling', '0.30'],
                  ['Feature Selection', 'Top 180'],
                  ['Target Encoding', 'Smooth=10'],
                ].map(([k, v]) => (
                  <div key={k} className="flex items-center justify-between py-2 border-b border-zinc-100 dark:border-zinc-800/60 last:border-0 last:pb-0">
                    <span className="text-sm font-medium text-zinc-500 dark:text-zinc-400">{k}</span>
                    <span className="text-[11px] font-mono font-bold text-zinc-800 dark:text-zinc-200 bg-zinc-100 dark:bg-zinc-800 px-2 py-1 rounded-md">{v}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Features Breakdown */}
            <div className="bg-white dark:bg-[#0c0c0f] border border-zinc-200 dark:border-zinc-800 rounded-3xl p-6 shadow-sm">
              <h3 className="font-bold text-zinc-900 dark:text-zinc-100 mb-2 flex items-center gap-2">
                <Activity size={18} className="text-rose-500" /> Dataset Split
              </h3>
              <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed mb-4">
                The model analyzes 50 distinct patient attributes. Different data types (like numeric BMI vs. categorical Regions) require entirely different mathematical encodings.
              </p>
              
              <div className="flex h-3 w-full rounded-full overflow-hidden mb-4 bg-zinc-100 dark:bg-zinc-800">
                <div className="bg-indigo-500 h-full" style={{ width: '38%' }} title="Numeric" />
                <div className="bg-pink-500 h-full" style={{ width: '34%' }} title="Binary" />
                <div className="bg-amber-500 h-full" style={{ width: '28%' }} title="Categorical" />
              </div>
              
              <div className="grid grid-cols-3 gap-2 text-center">
                <div>
                  <p className="text-xl font-black text-indigo-500">19</p>
                  <p className="text-[10px] uppercase font-bold text-zinc-400 mt-0.5">Numeric</p>
                </div>
                <div>
                  <p className="text-xl font-black text-pink-500">17</p>
                  <p className="text-[10px] uppercase font-bold text-zinc-400 mt-0.5">Binary</p>
                </div>
                <div>
                  <p className="text-xl font-black text-amber-500">14</p>
                  <p className="text-[10px] uppercase font-bold text-zinc-400 mt-0.5">Categ.</p>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};

export default ModelDev;
