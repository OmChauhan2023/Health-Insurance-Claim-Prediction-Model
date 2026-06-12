import React, { useState } from 'react';
import axios from 'axios';
import { Users, AlertTriangle, CheckCircle, Activity, TrendingUp, ArrowUpRight, ArrowDownRight } from 'lucide-react';
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
  High:   'bg-rose-100 text-rose-700 dark:bg-rose-900/30 dark:text-rose-400',
  Medium: 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400',
  Low:    'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400',
}[risk]);

const barColor = (score) =>
  score > 0.7 ? 'bg-rose-500' : score > 0.4 ? 'bg-orange-400' : 'bg-emerald-500';

const KPICard = ({ title, value, sub, icon: Icon, trend }) => (
  <div className="bg-white dark:bg-[#0c0c0f] p-5 rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm flex flex-col gap-3">
    <div className="flex justify-between items-start">
      <p className="text-xs font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">{title}</p>
      <div className="p-2 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-lg">
        <Icon size={18} />
      </div>
    </div>
    <div className="flex items-end justify-between">
      <p className="text-3xl font-extrabold tracking-tight text-zinc-950 dark:text-zinc-50">{value}</p>
      {trend && (
        <span className={`flex items-center gap-0.5 text-xs font-semibold px-2 py-1 rounded-full ${
          trend.dir === 'up'
            ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400'
            : 'bg-rose-100 text-rose-700 dark:bg-rose-900/30 dark:text-rose-400'
        }`}>
          {trend.dir === 'up' ? <ArrowUpRight size={12} /> : <ArrowDownRight size={12} />}
          {trend.label}
        </span>
      )}
    </div>
    {sub && <p className="text-xs text-zinc-400 dark:text-zinc-500">{sub}</p>}
  </div>
);

const Dashboard = () => {
  const [selectedRow, setSelectedRow] = useState(null);

  return (
    <div className="flex flex-col gap-6">
      {/* KPIs */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        <KPICard title="Total Claims Analyzed"  value="124,592" icon={Users}         trend={{ dir: 'up',   label: '+12% MoM' }} />
        <KPICard title="High Risk Detected"     value="4,821"   icon={AlertTriangle}  trend={{ dir: 'down', label: '-3.2%' }} sub="Compared to last quarter" />
        <KPICard title="Model Gini Score"       value="0.842"   icon={CheckCircle}    trend={{ dir: 'up',   label: 'Top 1%' }} sub="5-Fold OOF Calibrated Stacking" />
        <KPICard title="Avg Risk Probability"   value="23.4%"   icon={Activity}                                                sub="Across all evaluated patients" />
      </div>

      {/* Prediction form + History table */}
      <div className="grid grid-cols-1 xl:grid-cols-5 gap-6">
        {/* Form */}
        <div className="xl:col-span-2 bg-white dark:bg-[#0c0c0f] rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm p-6">
          <div className="flex items-center gap-2 mb-1">
            <TrendingUp size={20} className="text-blue-500" />
            <h2 className="text-lg font-bold tracking-tight text-zinc-950 dark:text-zinc-50">Claim Risk Predictor</h2>
          </div>
          <p className="text-xs text-zinc-400 dark:text-zinc-500 mb-5">Enter patient features for a real-time risk probability.</p>
          <PredictionForm />
        </div>

        {/* Table */}
        <div className="xl:col-span-3 bg-white dark:bg-[#0c0c0f] rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm overflow-hidden flex flex-col">
          <div className="px-6 py-4 border-b border-zinc-100 dark:border-zinc-800">
            <h2 className="text-lg font-bold tracking-tight text-zinc-950 dark:text-zinc-50">Recent Prediction History</h2>
            <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-0.5">Click a row for details</p>
          </div>

          <div className="overflow-x-auto flex-1">
            <table className="w-full text-sm">
              <thead className="bg-zinc-50 dark:bg-zinc-900 sticky top-0 z-10">
                <tr>
                  {['Patient ID','Age','BMI','Conditions','Prev Claims','Risk Score','Status'].map(h => (
                    <th key={h} className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 whitespace-nowrap">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {mockHistory.map((row, i) => (
                  <tr
                    key={i}
                    onClick={() => setSelectedRow(selectedRow?.id === row.id ? null : row)}
                    className={`border-b border-zinc-100 dark:border-zinc-800 cursor-pointer transition-colors ${
                      selectedRow?.id === row.id
                        ? 'bg-blue-50 dark:bg-blue-900/20'
                        : 'hover:bg-zinc-50 dark:hover:bg-zinc-800/50'
                    }`}
                  >
                    <td className="px-4 py-3 font-mono text-xs text-zinc-500 dark:text-zinc-400">{row.id}</td>
                    <td className="px-4 py-3 text-zinc-700 dark:text-zinc-300">{row.age}</td>
                    <td className="px-4 py-3 text-zinc-700 dark:text-zinc-300">{row.bmi}</td>
                    <td className="px-4 py-3 text-zinc-700 dark:text-zinc-300">{row.conditions}</td>
                    <td className="px-4 py-3 text-zinc-700 dark:text-zinc-300">{row.prevClaims}</td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <span className="text-xs w-8 font-mono text-zinc-500">{row.score.toFixed(2)}</span>
                        <div className="w-20 h-1.5 bg-zinc-200 dark:bg-zinc-700 rounded-full overflow-hidden">
                          <div className={`h-full ${barColor(row.score)} rounded-full`} style={{ width: `${row.score * 100}%` }} />
                        </div>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${riskColor(row.risk)}`}>{row.risk}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Detail panel for selected row */}
          {selectedRow && (
            <div className="border-t border-zinc-100 dark:border-zinc-800 px-6 py-4 bg-zinc-50 dark:bg-zinc-900/50">
              <div className="flex justify-between items-center mb-3">
                <p className="text-sm font-bold text-zinc-950 dark:text-zinc-50">Details — {selectedRow.id}</p>
                <button onClick={() => setSelectedRow(null)} className="text-xs text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200">Dismiss</button>
              </div>
              <div className="grid grid-cols-3 gap-3">
                {[
                  ['Age', selectedRow.age + ' yrs'],
                  ['BMI', selectedRow.bmi],
                  ['Conditions', selectedRow.conditions],
                  ['Prev Claims', selectedRow.prevClaims],
                  ['Risk Score', (selectedRow.score * 100).toFixed(1) + '%'],
                  ['Category', selectedRow.risk + ' Risk'],
                ].map(([k, v]) => (
                  <div key={k} className="bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-lg p-3">
                    <p className="text-xs text-zinc-400 dark:text-zinc-500 mb-0.5">{k}</p>
                    <p className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">{v}</p>
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
