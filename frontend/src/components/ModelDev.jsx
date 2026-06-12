import React from 'react';
import { GitBranch, Layers, Shuffle, Target, ChevronRight, CheckCircle2 } from 'lucide-react';

const StepCard = ({ step, title, desc, icon: Icon, color }) => (
  <div className={`relative bg-white dark:bg-[#0c0c0f] rounded-xl border border-zinc-200 dark:border-zinc-800 p-5 shadow-sm`}>
    <div className={`absolute top-0 left-0 w-1 h-full ${color} rounded-l-xl`} />
    <div className="pl-3">
      <div className="flex items-center gap-3 mb-2">
        <div className={`p-2 rounded-lg ${color.replace('bg-', 'bg-').replace('500', '50')} dark:bg-zinc-800`}>
          <Icon size={18} className={color.replace('bg-', 'text-')} />
        </div>
        <span className="text-xs font-bold uppercase tracking-widest text-zinc-400">Step {step}</span>
      </div>
      <h3 className="font-bold text-zinc-950 dark:text-zinc-50 text-base mb-1">{title}</h3>
      <p className="text-sm text-zinc-500 dark:text-zinc-400 leading-relaxed">{desc}</p>
    </div>
  </div>
);

const PipelineArrow = () => (
  <div className="flex justify-center my-1 text-zinc-300 dark:text-zinc-700">
    <ChevronRight size={20} className="rotate-90" />
  </div>
);

const BadgeList = ({ items, color = 'blue' }) => (
  <div className="flex flex-wrap gap-2 mt-3">
    {items.map(item => (
      <span key={item} className={`px-2.5 py-1 rounded-full text-xs font-semibold bg-${color}-50 text-${color}-700 dark:bg-${color}-900/20 dark:text-${color}-400 border border-${color}-200 dark:border-${color}-800/30`}>
        {item}
      </span>
    ))}
  </div>
);

const ModelDev = () => {
  const pipeline = [
    { step: 1, title: 'Data Loading & Global Feature Engineering', icon: GitBranch, color: 'bg-indigo-500',
      desc: 'Load raw training & test CSVs. Apply ZebraFeatureEngineer to create interaction terms and domain-specific features. Fit ZebraImputer for missing value handling (strategy differs for binary, categorical, and numeric columns). Artifacts saved: feat_eng.joblib, imputer.joblib.' },
    { step: 2, title: '5-Fold Stratified Cross-Validation', icon: Shuffle, color: 'bg-blue-500',
      desc: 'StratifiedKFold(n_splits=5) ensures class balance is maintained across folds. For each fold: OOF Target Encoding, SMOTE + undersampling resampling, and percentile-based Feature Selection are applied strictly inside the fold to prevent data leakage.' },
    { step: 3, title: 'OOF Predictions — Base Models', icon: Layers, color: 'bg-violet-500',
      desc: 'Three base models (LightGBM, XGBoost, CatBoost) are trained per fold. OOF predictions accumulate across folds to form a full training meta-feature matrix. Test predictions are averaged across the 5 folds.' },
    { step: 4, title: 'Stacking Meta-Learner', icon: Layers, color: 'bg-purple-500',
      desc: 'A LightGBM meta-learner is trained on the 3-column OOF matrix [lgb_oof, xgb_oof, cat_oof]. It learns to blend the base model outputs in an optimal, non-linear way. Saved as: meta_model.joblib.' },
    { step: 5, title: 'Isotonic Calibration', icon: Target, color: 'bg-emerald-500',
      desc: 'IsotonicRegression(out_of_bounds=clip) is fit on the stacking OOF predictions to calibrate output probabilities. This ensures the final probabilities are well-calibrated and monotone, maximizing the Gini coefficient.' },
  ];

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div className="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-xl p-6 text-white shadow-lg shadow-blue-500/20">
        <h2 className="text-2xl font-extrabold tracking-tight mb-1">ZEBRA Model Architecture</h2>
        <p className="text-blue-100 text-sm max-w-xl">
          5-Fold Stacking Ensemble with OOF Target Encoding, SMOTE resampling, and Isotonic Calibration.
          Final Gini: <strong>0.2860</strong> | Final AUC: <strong>0.6430</strong>
        </p>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Pipeline Steps */}
        <div className="xl:col-span-2 flex flex-col gap-0">
          {pipeline.map((p, i) => (
            <div key={p.step}>
              <StepCard {...p} />
              {i < pipeline.length - 1 && <PipelineArrow />}
            </div>
          ))}
        </div>

        {/* Right side info cards */}
        <div className="flex flex-col gap-4">
          {/* Base Models */}
          <div className="bg-white dark:bg-[#0c0c0f] rounded-xl border border-zinc-200 dark:border-zinc-800 p-5 shadow-sm">
            <h3 className="font-bold text-zinc-950 dark:text-zinc-50 mb-3 flex items-center gap-2">
              <CheckCircle2 size={16} className="text-blue-500" /> Base Models
            </h3>
            {[
              { name: 'LightGBM', gini: '0.278', weight: '42.1%', color: 'bg-blue-500' },
              { name: 'XGBoost',  gini: '0.277', weight: '14.5%', color: 'bg-violet-500' },
              { name: 'CatBoost', gini: '0.278', weight: '43.4%', color: 'bg-emerald-500' },
            ].map(m => (
              <div key={m.name} className="mb-3 last:mb-0">
                <div className="flex justify-between text-xs mb-1">
                  <span className="font-semibold text-zinc-700 dark:text-zinc-300">{m.name}</span>
                  <span className="text-zinc-400">Gini {m.gini} · Weight {m.weight}</span>
                </div>
                <div className="h-2 bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden">
                  <div className={`h-full ${m.color} rounded-full`} style={{ width: m.weight }} />
                </div>
              </div>
            ))}
          </div>

          {/* Config */}
          <div className="bg-white dark:bg-[#0c0c0f] rounded-xl border border-zinc-200 dark:border-zinc-800 p-5 shadow-sm">
            <h3 className="font-bold text-zinc-950 dark:text-zinc-50 mb-3">Preprocessing Config</h3>
            <div className="space-y-2 text-sm">
              {[
                ['CV Strategy', '5-Fold Stratified'],
                ['SMOTE Ratio', '0.05'],
                ['Under-sampling', '0.30'],
                ['Feature Selection', 'Top 65th percentile'],
                ['Target Encoding', 'Smoothing = 10'],
                ['Random State', '42'],
              ].map(([k, v]) => (
                <div key={k} className="flex justify-between">
                  <span className="text-zinc-500 dark:text-zinc-400">{k}</span>
                  <span className="font-mono text-xs font-semibold text-zinc-800 dark:text-zinc-200 bg-zinc-100 dark:bg-zinc-800 px-2 py-0.5 rounded">{v}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Feature types */}
          <div className="bg-white dark:bg-[#0c0c0f] rounded-xl border border-zinc-200 dark:border-zinc-800 p-5 shadow-sm">
            <h3 className="font-bold text-zinc-950 dark:text-zinc-50 mb-2">Feature Breakdown</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between items-center">
                <span className="text-zinc-500">Binary</span><span className="font-bold text-zinc-800 dark:text-zinc-200">17 features</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-zinc-500">Categorical</span><span className="font-bold text-zinc-800 dark:text-zinc-200">14 features</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-zinc-500">Numeric</span><span className="font-bold text-zinc-800 dark:text-zinc-200">19 features</span>
              </div>
              <div className="flex justify-between items-center border-t border-zinc-100 dark:border-zinc-800 pt-2 mt-2">
                <span className="text-zinc-500 font-semibold">Total</span><span className="font-black text-blue-600 dark:text-blue-400">50 features</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModelDev;
