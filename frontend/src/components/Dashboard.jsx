import React from 'react';
import { Activity, Users, AlertTriangle, CheckCircle, TrendingUp } from 'lucide-react';
import PredictionForm from './PredictionForm';

const KPICard = ({ title, value, icon: Icon, trend, trendValue }) => (
  <div className="bg-white dark:bg-[#0c0c0f] p-5 rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm">
    <div className="flex justify-between items-start mb-4">
      <h3 className="text-sm font-medium text-zinc-500 dark:text-zinc-400">{title}</h3>
      <div className="p-2 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-lg">
        <Icon size={20} />
      </div>
    </div>
    <div className="flex items-baseline gap-3">
      <span className="text-3xl font-extrabold text-zinc-950 dark:text-zinc-50">{value}</span>
      <span className={`text-xs font-semibold px-2 py-1 rounded-full ${
        trend === 'up' ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400' :
        trend === 'down' ? 'bg-rose-100 text-rose-700 dark:bg-rose-900/30 dark:text-rose-400' :
        'bg-zinc-100 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-400'
      }`}>
        {trendValue}
      </span>
    </div>
  </div>
);

const Dashboard = () => {
  return (
    <div className="flex flex-col gap-6">
      {/* KPI Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <KPICard title="Total Claims Analyzed" value="124,592" icon={Users} trend="up" trendValue="+12%" />
        <KPICard title="High Risk Detected" value="4,821" icon={AlertTriangle} trend="down" trendValue="-3.2%" />
        <KPICard title="Model Gini Score" value="0.842" icon={CheckCircle} trend="up" trendValue="Top 1%" />
        <KPICard title="Avg Risk Probability" value="23.4%" icon={Activity} trend="neutral" trendValue="Stable" />
      </div>

      {/* Main Panel Area */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-[#0c0c0f] rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm p-6">
          <div className="mb-6">
            <h2 className="text-xl font-bold tracking-tight text-zinc-950 dark:text-zinc-50 flex items-center gap-2">
              <TrendingUp size={24} className="text-blue-500"/>
              New Claim Prediction
            </h2>
            <p className="text-sm text-zinc-500 dark:text-zinc-400">
              Enter patient features below to get a real-time risk probability from the model.
            </p>
          </div>
          <PredictionForm />
        </div>
        
        <div className="bg-white dark:bg-[#0c0c0f] rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm p-6 flex flex-col items-center">
            <h3 className="text-lg font-bold text-zinc-950 dark:text-zinc-50 mb-6 w-full text-left">Recent Prediction History</h3>
            
            {/* Mock Table */}
            <div className="w-full overflow-x-auto">
              <table className="w-full text-sm text-left">
                <thead className="text-xs text-zinc-500 dark:text-zinc-400 uppercase bg-zinc-50 dark:bg-zinc-900 border-b border-zinc-200 dark:border-zinc-800">
                  <tr>
                    <th className="px-4 py-3">Patient ID</th>
                    <th className="px-4 py-3">Risk Score</th>
                    <th className="px-4 py-3">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {[
                    { id: 'PT-9812', score: 0.89, status: 'High Risk' },
                    { id: 'PT-4321', score: 0.45, status: 'Medium Risk' },
                    { id: 'PT-1102', score: 0.12, status: 'Low Risk' },
                    { id: 'PT-5543', score: 0.76, status: 'High Risk' },
                  ].map((row, i) => (
                    <tr key={i} className="border-b border-zinc-100 dark:border-zinc-800 hover:bg-zinc-50 dark:hover:bg-zinc-800/50">
                      <td className="px-4 py-3 font-mono text-zinc-500 dark:text-zinc-400">{row.id}</td>
                      <td className="px-4 py-3">
                        <div className="flex items-center gap-2">
                          <span className="w-8">{row.score.toFixed(2)}</span>
                          <div className="w-24 bg-zinc-200 dark:bg-zinc-700 h-2 rounded-full overflow-hidden">
                            <div 
                              className={`h-full ${row.score > 0.7 ? 'bg-rose-500' : row.score > 0.4 ? 'bg-orange-400' : 'bg-emerald-500'}`} 
                              style={{ width: `${row.score * 100}%` }}
                            ></div>
                          </div>
                        </div>
                      </td>
                      <td className="px-4 py-3">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                          row.status === 'High Risk' ? 'bg-rose-100 text-rose-700 dark:bg-rose-900/30 dark:text-rose-400' :
                          row.status === 'Medium Risk' ? 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400' :
                          'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400'
                        }`}>
                          {row.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
