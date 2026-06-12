import React, { useState, useEffect } from 'react';
import { ImageIcon, ZoomIn, X } from 'lucide-react';

const plotMeta = {
  'correlation_heatmap.png':    { title: 'Feature Correlation Heatmap', desc: 'Pairwise Pearson correlation between all 50 numeric/binary features.' },
  'numeric_distributions.png':  { title: 'Numeric Feature Distributions', desc: 'KDE distribution plots for all 19 numeric features, split by claim class.' },
  'target_distribution.png':    { title: 'Target Class Distribution', desc: 'Class imbalance overview for binary claim target (0 = no claim, 1 = claim).' },
};

const PlotsGallery = () => {
  const [plots, setPlots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lightbox, setLightbox] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/plots')
      .then(r => r.json())
      .then(data => { setPlots(data.files || []); setLoading(false); })
      .catch(() => { setError('Could not load plots from backend.'); setLoading(false); });
  }, []);

  if (loading) return (
    <div className="flex items-center justify-center h-64 text-zinc-400">
      <div className="flex flex-col items-center gap-3">
        <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
        <p className="text-sm">Loading plots…</p>
      </div>
    </div>
  );

  if (error) return (
    <div className="bg-rose-50 dark:bg-rose-900/20 border border-rose-200 dark:border-rose-800/30 text-rose-700 dark:text-rose-400 rounded-xl p-6 text-sm">
      <strong>Error:</strong> {error} Make sure the FastAPI backend is running on port 8000.
    </div>
  );

  return (
    <>
      <div className="flex flex-col gap-4">
        <div>
          <h2 className="text-2xl font-extrabold tracking-tight text-zinc-950 dark:text-zinc-50">EDA Plots Gallery</h2>
          <p className="text-sm text-zinc-400 dark:text-zinc-500 mt-1">Exploratory data analysis visualizations generated from the training dataset. Click any image to enlarge.</p>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
          {plots.map(fname => {
            const meta = plotMeta[fname] || { title: fname, desc: '' };
            return (
              <div
                key={fname}
                className="bg-white dark:bg-[#0c0c0f] rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm overflow-hidden group"
              >
                <div className="relative overflow-hidden bg-zinc-50 dark:bg-zinc-900 cursor-pointer" onClick={() => setLightbox(fname)}>
                  <img
                    src={`http://localhost:8000/api/plots/${fname}`}
                    alt={meta.title}
                    className="w-full object-contain max-h-72 group-hover:scale-105 transition-transform duration-300"
                    loading="lazy"
                  />
                  <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all duration-200 flex items-center justify-center opacity-0 group-hover:opacity-100">
                    <div className="bg-white dark:bg-zinc-900 rounded-full p-2 shadow-lg">
                      <ZoomIn size={20} className="text-zinc-700 dark:text-zinc-300" />
                    </div>
                  </div>
                </div>
                <div className="px-5 py-4">
                  <div className="flex items-center gap-2 mb-1">
                    <ImageIcon size={14} className="text-blue-500" />
                    <h3 className="font-bold text-zinc-950 dark:text-zinc-50 text-sm">{meta.title}</h3>
                  </div>
                  <p className="text-xs text-zinc-400 dark:text-zinc-500">{meta.desc}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Lightbox */}
      {lightbox && (
        <div
          className="fixed inset-0 bg-zinc-950/80 backdrop-blur-sm z-[100] flex items-center justify-center p-6"
          onClick={() => setLightbox(null)}
        >
          <div className="relative max-w-5xl w-full bg-white dark:bg-zinc-900 rounded-2xl overflow-hidden shadow-2xl" onClick={e => e.stopPropagation()}>
            <button
              onClick={() => setLightbox(null)}
              className="absolute top-3 right-3 z-10 bg-white dark:bg-zinc-800 text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-50 rounded-full p-1.5 shadow transition-colors"
            >
              <X size={18} />
            </button>
            <img
              src={`http://localhost:8000/api/plots/${lightbox}`}
              alt={lightbox}
              className="w-full object-contain max-h-[80vh]"
            />
            <div className="px-6 py-4 border-t border-zinc-100 dark:border-zinc-800">
              <p className="font-semibold text-zinc-950 dark:text-zinc-50 text-sm">{plotMeta[lightbox]?.title || lightbox}</p>
              <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-0.5">{plotMeta[lightbox]?.desc || ''}</p>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default PlotsGallery;
