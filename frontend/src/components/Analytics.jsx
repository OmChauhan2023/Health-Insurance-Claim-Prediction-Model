import React, { useState } from 'react';
import ReactECharts from 'echarts-for-react';

const foldData = [
  { fold: 'Fold 1', lgb: 0.2734, xgb: 0.2726, cat: 0.2731, stack: 0.2828 },
  { fold: 'Fold 2', lgb: 0.2713, xgb: 0.2723, cat: 0.2710, stack: 0.2815 },
  { fold: 'Fold 3', lgb: 0.2752, xgb: 0.2734, cat: 0.2722, stack: 0.2842 },
  { fold: 'Fold 4', lgb: 0.2851, xgb: 0.2816, cat: 0.2874, stack: 0.2879 },
  { fold: 'Fold 5', lgb: 0.2896, xgb: 0.2858, cat: 0.2901, stack: 0.2893 },
];

const COLORS = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b'];

const MetricCard = ({ label, value, sub, color }) => (
  <div className={`bg-white dark:bg-[#0c0c0f] rounded-xl border border-zinc-200 dark:border-zinc-800 p-5 shadow-sm border-t-4`} style={{ borderTopColor: color }}>
    <p className="text-xs text-zinc-400 dark:text-zinc-500 uppercase tracking-wider font-semibold mb-2">{label}</p>
    <p className="text-3xl font-extrabold text-zinc-950 dark:text-zinc-50">{value}</p>
    <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-1">{sub}</p>
  </div>
);

const Analytics = () => {
  const [activeModel, setActiveModel] = useState('all');

  const models = [
    { key: 'lgb',   label: 'LightGBM',        oof_gini: 0.2788, oof_auc: 0.6394, color: COLORS[0] },
    { key: 'xgb',   label: 'XGBoost',          oof_gini: 0.2770, oof_auc: 0.6385, color: COLORS[1] },
    { key: 'cat',   label: 'CatBoost',         oof_gini: 0.2786, oof_auc: 0.6393, color: COLORS[2] },
    { key: 'stack', label: 'Stacking Ensemble',oof_gini: 0.2860, oof_auc: 0.6430, color: COLORS[3] },
  ];

  const giniBarOption = {
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' }, backgroundColor: 'rgba(255,255,255,0.95)', borderColor: '#e2e8f0', textStyle: { color: '#0f172a' } },
    grid: { left: 16, right: 16, top: 16, bottom: 16, containLabel: true },
    xAxis: { type: 'category', data: models.map(m => m.label), axisLine: { lineStyle: { color: '#e2e8f0' } }, axisLabel: { color: '#94a3b8', fontSize: 11 } },
    yAxis: { type: 'value', min: 0.26, max: 0.30, axisLabel: { color: '#94a3b8', fontSize: 11, formatter: v => v.toFixed(3) }, splitLine: { lineStyle: { color: '#f1f5f9' } } },
    series: [{
      type: 'bar', barWidth: '50%',
      data: models.map(m => ({ value: m.oof_gini, itemStyle: { color: m.color, borderRadius: [6, 6, 0, 0] } })),
      label: { show: true, position: 'top', formatter: p => p.value.toFixed(3), color: '#64748b', fontSize: 11, fontWeight: 600 },
    }],
  };

  const foldLineOption = {
    tooltip: { trigger: 'axis', backgroundColor: 'rgba(255,255,255,0.95)', borderColor: '#e2e8f0', textStyle: { color: '#0f172a' } },
    legend: { data: ['LightGBM', 'XGBoost', 'CatBoost', 'Stacking'], top: 0, textStyle: { color: '#94a3b8' }, icon: 'circle' },
    grid: { left: 16, right: 16, top: 40, bottom: 16, containLabel: true },
    xAxis: { type: 'category', data: foldData.map(f => f.fold), axisLabel: { color: '#94a3b8' }, axisLine: { lineStyle: { color: '#e2e8f0' } } },
    yAxis: { type: 'value', min: 0.26, max: 0.30, axisLabel: { color: '#94a3b8', formatter: v => v.toFixed(3) }, splitLine: { lineStyle: { color: '#f1f5f9' } } },
    series: [
      { name: 'LightGBM',         type: 'line', smooth: true, symbol: 'circle', symbolSize: 7, data: foldData.map(f => f.lgb),   lineStyle: { color: COLORS[0], width: 2.5 }, itemStyle: { color: COLORS[0] } },
      { name: 'XGBoost',          type: 'line', smooth: true, symbol: 'circle', symbolSize: 7, data: foldData.map(f => f.xgb),   lineStyle: { color: COLORS[1], width: 2.5 }, itemStyle: { color: COLORS[1] } },
      { name: 'CatBoost',         type: 'line', smooth: true, symbol: 'circle', symbolSize: 7, data: foldData.map(f => f.cat),   lineStyle: { color: COLORS[2], width: 2.5 }, itemStyle: { color: COLORS[2] } },
      { name: 'Stacking',         type: 'line', smooth: true, symbol: 'circle', symbolSize: 7, data: foldData.map(f => f.stack), lineStyle: { color: COLORS[3], width: 2.5 }, itemStyle: { color: COLORS[3] } },
    ],
  };

  const aucRadarOption = {
    tooltip: { backgroundColor: 'rgba(255,255,255,0.95)', borderColor: '#e2e8f0', textStyle: { color: '#0f172a' } },
    radar: {
      indicator: [
        { name: 'Gini Score',   max: 1 },
        { name: 'AUC',          max: 1 },
        { name: 'Stability',    max: 1 },
        { name: 'Calibration',  max: 1 },
        { name: 'Lift @ 10%',   max: 1 },
      ],
      axisLine: { lineStyle: { color: '#e2e8f0' } },
      splitLine: { lineStyle: { color: '#f1f5f9' } },
      axisName: { color: '#94a3b8', fontSize: 11 },
    },
    series: [{
      type: 'radar',
      data: [
        { value: [0.2788, 0.6394, 0.88, 0.80, 0.78], name: 'LightGBM',  areaStyle: { color: COLORS[0] + '30' }, lineStyle: { color: COLORS[0] } },
        { value: [0.2770, 0.6385, 0.91, 0.84, 0.82], name: 'XGBoost',   areaStyle: { color: COLORS[1] + '30' }, lineStyle: { color: COLORS[1] } },
        { value: [0.2786, 0.6393, 0.86, 0.78, 0.76], name: 'CatBoost',  areaStyle: { color: COLORS[2] + '30' }, lineStyle: { color: COLORS[2] } },
        { value: [0.2860, 0.6430, 0.93, 0.91, 0.88], name: 'Stacking',  areaStyle: { color: COLORS[3] + '30' }, lineStyle: { color: COLORS[3] } },
      ],
    }],
  };

  return (
    <div className="flex flex-col gap-6">
      {/* Header metric cards */}
      <div className="grid grid-cols-2 xl:grid-cols-4 gap-4">
        {models.map(m => (
          <MetricCard key={m.key} label={m.label} value={m.oof_gini.toFixed(3)} sub={`AUC: ${m.oof_auc.toFixed(3)} · OOF`} color={m.color} />
        ))}
      </div>

      {/* Charts row 1 */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-[#0c0c0f] rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm p-6">
          <h3 className="font-bold text-zinc-950 dark:text-zinc-50 mb-1">OOF Gini Score — Model Comparison</h3>
          <p className="text-xs text-zinc-400 dark:text-zinc-500 mb-4">Out-of-fold Normalized Gini across all base models and final stacking ensemble.</p>
          <ReactECharts option={giniBarOption} style={{ height: 300 }} />
        </div>

        <div className="bg-white dark:bg-[#0c0c0f] rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm p-6">
          <h3 className="font-bold text-zinc-950 dark:text-zinc-50 mb-1">Gini Stability Across Folds</h3>
          <p className="text-xs text-zinc-400 dark:text-zinc-500 mb-4">Per-fold Gini score for each model to visualize consistency and variance.</p>
          <ReactECharts option={foldLineOption} style={{ height: 300 }} />
        </div>
      </div>

      {/* Charts row 2 */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-[#0c0c0f] rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm p-6">
          <h3 className="font-bold text-zinc-950 dark:text-zinc-50 mb-1">Multi-Metric Radar</h3>
          <p className="text-xs text-zinc-400 dark:text-zinc-500 mb-4">Holistic comparison across Gini, AUC, stability, calibration, and lift metrics.</p>
          <ReactECharts option={aucRadarOption} style={{ height: 320 }} />
        </div>

        <div className="bg-white dark:bg-[#0c0c0f] rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm p-6">
          <h3 className="font-bold text-zinc-950 dark:text-zinc-50 mb-4">Detailed Results Table</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-zinc-100 dark:border-zinc-800">
                  {['Model', 'OOF Gini', 'OOF AUC', 'Blend Weight'].map(h => (
                    <th key={h} className="pb-2 text-left text-xs text-zinc-400 dark:text-zinc-500 font-semibold uppercase tracking-wider">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {[
                  ['LightGBM',         '0.2788', '0.6394', '42.1%', COLORS[0]],
                  ['XGBoost',          '0.2770', '0.6385', '14.5%', COLORS[1]],
                  ['CatBoost',         '0.2786', '0.6393', '43.4%', COLORS[2]],
                  ['Stacking (Final)', '0.2860', '0.6430', '—',     COLORS[3]],
                ].map(([name, gini, auc, wt, color]) => (
                  <tr key={name} className="border-b border-zinc-50 dark:border-zinc-800/50">
                    <td className="py-2.5 pr-4 font-medium text-zinc-800 dark:text-zinc-200 flex items-center gap-2">
                      <span className="w-2.5 h-2.5 rounded-full inline-block shrink-0" style={{ background: color }} />
                      {name}
                    </td>
                    <td className="py-2.5 pr-4 font-mono text-zinc-700 dark:text-zinc-300">{gini}</td>
                    <td className="py-2.5 pr-4 font-mono text-zinc-700 dark:text-zinc-300">{auc}</td>
                    <td className="py-2.5 font-mono text-zinc-700 dark:text-zinc-300">{wt}</td>
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

export default Analytics;
