import React, { useState } from 'react';
import { Users, AlertTriangle, CheckCircle, Activity, TrendingUp, Info, HelpCircle } from 'lucide-react';
import PredictionForm from './PredictionForm';

const mockHistory = [
  { id: 'PT-9812', age: 58, bmi: 34.1, conditions: 'Severe', prevClaims: 4, score: 0.89, risk: 'High' },
  { id: 'PT-4321', age: 42, bmi: 27.3, conditions: 'Mild',   prevClaims: 1, score: 0.45, risk: 'Medium' },
  { id: 'PT-1102', age: 28, bmi: 21.8, conditions: 'None',   prevClaims: 0, score: 0.09, risk: 'Low' },
  { id: 'PT-5543', age: 67, bmi: 31.2, conditions: 'Severe', prevClaims: 6, score: 0.82, risk: 'High' },
  { id: 'PT-3311', age: 35, bmi: 24.5, conditions: 'None',   prevClaims: 0, score: 0.15, risk: 'Low' },
  { id: 'PT-7789', age: 51, bmi: 29.7, conditions: 'Mild',   prevClaims: 2, score: 0.58, risk: 'Medium' },
];

const riskColor = (risk) => ({
  High:   'bg-rose-500 text-white shadow-rose-500/30',
  Medium: 'bg-orange-400 text-white shadow-orange-400/30',
  Low:    'bg-emerald-500 text-white shadow-emerald-500/30',
}[risk]);

const barColor = (score) =>
  score > 0.7 ? 'bg-rose-500' : score > 0.4 ? 'bg-orange-400' : 'bg-emerald-500';

const KPICard = ({ title, value, sub, icon: Icon, colorClass }) => (
  <div className="bg-white/80 dark:bg-[#0c0c0f]/80 backdrop-blur-md p-4 rounded-2xl border border-white/20 dark:border-zinc-800/50 shadow-sm flex flex-col gap-2 relative overflow-hidden group">
    <div className={`absolute -right-4 -top-4 w-20 h-20 opacity-10 rounded-full blur-2xl transition-all duration-500 group-hover:scale-150 ${colorClass}`} />
    <div className="flex items-center gap-3">
      <div className={`p-2 rounded-xl ${colorClass} bg-opacity-10 dark:bg-opacity-20 text-opacity-90`}>
        <Icon size={20} className="text-current" />
      </div>
      <div>
        <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-500 dark:text-zinc-400">{title}</p>
        <p className="text-2xl font-extrabold tracking-tight text-zinc-950 dark:text-zinc-50 leading-none mt-1">{value}</p>
      </div>
    </div>
  </div>
);

const Dashboard = () => {
  const [selectedRow, setSelectedRow] = useState(null);

  return (
    <div className="flex flex-col gap-8">
      
      {/* 1. Hero Section: The Predictor */}
      <div className="relative rounded-3xl overflow-hidden shadow-2xl border border-white/10 dark:border-zinc-800/50 bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-700">
        {/* Decorative background shapes */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-pink-500/20 rounded-full blur-[100px] pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-blue-400/20 rounded-full blur-[100px] pointer-events-none" />
        
        <div className="relative z-10 p-8 md:p-12 flex flex-col xl:flex-row gap-10 items-center">
          <div className="flex-1 text-white space-y-6">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 bg-white/10 backdrop-blur-md rounded-full text-xs font-semibold tracking-wider text-blue-100 border border-white/20 mb-6">
                <TrendingUp size={14} /> LIVE INFERENCE
              </div>
              <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4 leading-tight">
                Predict Claim <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-200 to-pink-200">Risk Instantly.</span>
              </h1>
              <p className="text-blue-100/80 text-lg leading-relaxed max-w-xl">
                Enter patient features below to calculate their probability of filing an insurance claim. Our Stacking Ensemble model analyzes 50 distinct data points to output a highly calibrated risk score.
              </p>
            </div>
            
            <div className="bg-black/20 backdrop-blur-sm rounded-xl p-4 border border-white/10 flex gap-4 items-start max-w-xl">
              <Info className="text-blue-300 shrink-0 mt-0.5" size={20} />
              <p className="text-sm text-blue-50/90 leading-relaxed">
                <strong>How does this work?</strong> This tool uses historical patient health data (BMI, age, prior conditions) to identify patterns that lead to claims. It helps insurers proactively offer wellness programs to high-risk patients before expensive claims occur!
              </p>
            </div>
          </div>

          <div className="w-full xl:w-[480px] bg-white dark:bg-[#0c0c0f] rounded-2xl p-6 shadow-2xl border border-zinc-200/50 dark:border-zinc-800 relative z-20">
            <h2 className="text-xl font-bold text-zinc-900 dark:text-zinc-50 mb-4">Run Prediction</h2>
            <PredictionForm />
          </div>
        </div>
      </div>

      {/* 2. KPIs (moved below hero, made colorful) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        <KPICard title="Total Analyzed" value="124,592" icon={Users} colorClass="bg-blue-500 text-blue-600 dark:text-blue-400" />
        <KPICard title="High Risk" value="4,821" icon={AlertTriangle} colorClass="bg-rose-500 text-rose-600 dark:text-rose-400" />
        <KPICard title="Gini Score" value="0.2860" icon={CheckCircle} colorClass="bg-emerald-500 text-emerald-600 dark:text-emerald-400" />
        <KPICard title="Avg Probability" value="23.4%" icon={Activity} colorClass="bg-purple-500 text-purple-600 dark:text-purple-400" />
      </div>

      {/* 3. History Table with Context */}
      <div className="grid grid-cols-1 xl:grid-cols-4 gap-8">
        
        {/* Educational Sidebar */}
        <div className="xl:col-span-1 space-y-6">
          <div className="bg-blue-50 dark:bg-blue-900/10 border border-blue-100 dark:border-blue-900/30 rounded-2xl p-6">
            <h3 className="font-bold text-blue-900 dark:text-blue-100 flex items-center gap-2 mb-3">
              <HelpCircle size={18} /> Understanding the Results
            </h3>
            <p className="text-sm text-blue-800/80 dark:text-blue-200/70 leading-relaxed mb-4">
              The table shows recent patients evaluated by the model. The <strong>Risk Score</strong> is the probability (from 0% to 100%) that the patient will file a claim.
            </p>
            <ul className="space-y-3 text-sm">
              <li className="flex gap-3 items-start">
                <span className="w-2.5 h-2.5 rounded-full bg-rose-500 mt-1 shrink-0 shadow-sm shadow-rose-500/50" />
                <span className="text-blue-900/90 dark:text-blue-100/80"><strong>High Risk (&gt;70%)</strong>: Immediate wellness intervention recommended.</span>
              </li>
              <li className="flex gap-3 items-start">
                <span className="w-2.5 h-2.5 rounded-full bg-orange-400 mt-1 shrink-0 shadow-sm shadow-orange-400/50" />
                <span className="text-blue-900/90 dark:text-blue-100/80"><strong>Medium Risk (40-70%)</strong>: Monitor health indicators over time.</span>
              </li>
              <li className="flex gap-3 items-start">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 mt-1 shrink-0 shadow-sm shadow-emerald-500/50" />
                <span className="text-blue-900/90 dark:text-blue-100/80"><strong>Low Risk (&lt;40%)</strong>: Standard policy coverage applies.</span>
              </li>
            </ul>
          </div>
          
          <div className="bg-white dark:bg-[#0c0c0f] border border-zinc-200 dark:border-zinc-800 rounded-2xl p-6 shadow-sm">
             <h3 className="text-sm font-bold text-zinc-900 dark:text-zinc-100 mb-2">Model Performance Context</h3>
             <p className="text-sm text-zinc-500 dark:text-zinc-400 leading-relaxed">
               This model achieved a <strong>0.2860 Gini score</strong>. In insurance analytics, this means our AI is about 28.6% better at perfectly ranking patients by risk compared to random guessing!
             </p>
          </div>
        </div>

        {/* Table */}
        <div className="xl:col-span-3 bg-white dark:bg-[#0c0c0f] rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-sm overflow-hidden flex flex-col">
          <div className="px-6 py-5 border-b border-zinc-100 dark:border-zinc-800 bg-zinc-50/50 dark:bg-zinc-900/20">
            <h2 className="text-lg font-bold tracking-tight text-zinc-950 dark:text-zinc-50">Recent Patient Evaluations</h2>
            <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">Live feed of predictions made by the Stacking Ensemble</p>
          </div>

          <div className="overflow-x-auto flex-1">
            <table className="w-full text-sm">
              <thead className="bg-zinc-50 dark:bg-zinc-900/80 border-b border-zinc-100 dark:border-zinc-800">
                <tr>
                  {['Patient ID','Age','BMI','Conditions','Prev Claims','Risk Score','Status'].map(h => (
                    <th key={h} className="px-5 py-4 text-left text-xs font-bold uppercase tracking-wider text-zinc-500 dark:text-zinc-400 whitespace-nowrap">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-100 dark:divide-zinc-800/50">
                {mockHistory.map((row, i) => (
                  <tr
                    key={i}
                    onClick={() => setSelectedRow(selectedRow?.id === row.id ? null : row)}
                    className={`cursor-pointer transition-all duration-200 ${
                      selectedRow?.id === row.id
                        ? 'bg-blue-50 dark:bg-blue-900/20'
                        : 'hover:bg-zinc-50 dark:hover:bg-zinc-800/50'
                    }`}
                  >
                    <td className="px-5 py-4 font-mono text-xs font-medium text-zinc-600 dark:text-zinc-300">{row.id}</td>
                    <td className="px-5 py-4 text-zinc-700 dark:text-zinc-300 font-medium">{row.age}</td>
                    <td className="px-5 py-4 text-zinc-700 dark:text-zinc-300">{row.bmi}</td>
                    <td className="px-5 py-4 text-zinc-700 dark:text-zinc-300">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        row.conditions === 'Severe' ? 'bg-rose-50 text-rose-700 dark:bg-rose-900/20 dark:text-rose-400' :
                        row.conditions === 'Mild' ? 'bg-orange-50 text-orange-700 dark:bg-orange-900/20 dark:text-orange-400' :
                        'bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-400'
                      }`}>{row.conditions}</span>
                    </td>
                    <td className="px-5 py-4 text-zinc-700 dark:text-zinc-300">{row.prevClaims}</td>
                    <td className="px-5 py-4">
                      <div className="flex items-center gap-3">
                        <span className="text-xs w-8 font-mono font-semibold text-zinc-700 dark:text-zinc-300">{(row.score * 100).toFixed(1)}%</span>
                        <div className="w-24 h-2 bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden shadow-inner">
                          <div className={`h-full ${barColor(row.score)} rounded-full transition-all duration-1000 ease-out`} style={{ width: `${row.score * 100}%` }} />
                        </div>
                      </div>
                    </td>
                    <td className="px-5 py-4">
                      <span className={`px-2.5 py-1 rounded-full text-xs font-bold shadow-sm ${riskColor(row.risk)}`}>{row.risk}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Detail panel */}
          {selectedRow && (
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-zinc-900 dark:to-zinc-900 border-t border-zinc-200 dark:border-zinc-800 px-6 py-5 shadow-[inset_0_4px_6px_-4px_rgba(0,0,0,0.1)]">
              <div className="flex justify-between items-center mb-4">
                <p className="text-sm font-bold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
                  <Activity size={16} className="text-blue-600" /> Patient Snapshot: {selectedRow.id}
                </p>
                <button onClick={() => setSelectedRow(null)} className="text-xs font-medium text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors">Dismiss</button>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-6 gap-3">
                {[
                  ['Age', selectedRow.age + ' yrs'],
                  ['BMI', selectedRow.bmi],
                  ['Conditions', selectedRow.conditions],
                  ['Prev Claims', selectedRow.prevClaims],
                  ['Risk Score', (selectedRow.score * 100).toFixed(1) + '%'],
                  ['Category', selectedRow.risk + ' Risk'],
                ].map(([k, v]) => (
                  <div key={k} className="bg-white dark:bg-[#0c0c0f] border border-zinc-200/60 dark:border-zinc-800 rounded-xl p-3 shadow-sm hover:border-blue-300 transition-colors">
                    <p className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 mb-1">{k}</p>
                    <p className="text-sm font-black text-zinc-900 dark:text-zinc-50">{v}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
