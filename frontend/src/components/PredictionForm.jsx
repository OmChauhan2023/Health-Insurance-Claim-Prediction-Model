import React, { useState } from 'react';
import axios from 'axios';

const PredictionForm = () => {
  const [formData, setFormData] = useState({
    feature_1: '',
    feature_2: '',
    feature_3: '',
    feature_4: '',
  });
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      // Send mock request to FastAPI backend
      const response = await axios.post('http://localhost:8000/api/predict', {
        features: formData
      });
      setResult(response.data);
    } catch (error) {
      console.error('Prediction failed', error);
      setResult({ error: 'Failed to connect to model API.' });
    }
    setLoading(false);
  };

  return (
    <div className="w-full">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-medium text-zinc-500 mb-1.5">Patient Age (Feature 1)</label>
            <input
              type="number"
              name="feature_1"
              value={formData.feature_1}
              onChange={handleChange}
              className="w-full bg-[#ffffff] dark:bg-[#09090b] border border-zinc-200 dark:border-zinc-800 rounded-[8px] px-[12px] py-[8px] text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 text-zinc-950 dark:text-zinc-100 transition-all"
              placeholder="e.g. 45"
              required
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-zinc-500 mb-1.5">BMI (Feature 2)</label>
            <input
              type="number"
              step="0.1"
              name="feature_2"
              value={formData.feature_2}
              onChange={handleChange}
              className="w-full bg-[#ffffff] dark:bg-[#09090b] border border-zinc-200 dark:border-zinc-800 rounded-[8px] px-[12px] py-[8px] text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 text-zinc-950 dark:text-zinc-100 transition-all"
              placeholder="e.g. 28.5"
              required
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-zinc-500 mb-1.5">Pre-existing Conditions (Feature 3)</label>
            <select
              name="feature_3"
              value={formData.feature_3}
              onChange={handleChange}
              className="w-full bg-[#ffffff] dark:bg-[#09090b] border border-zinc-200 dark:border-zinc-800 rounded-[8px] px-[12px] py-[8px] text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 text-zinc-950 dark:text-zinc-100 transition-all"
              required
            >
              <option value="" disabled>Select...</option>
              <option value="0">None</option>
              <option value="1">Mild</option>
              <option value="2">Severe</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-zinc-500 mb-1.5">Previous Claims Count (Feature 4)</label>
            <input
              type="number"
              name="feature_4"
              value={formData.feature_4}
              onChange={handleChange}
              className="w-full bg-[#ffffff] dark:bg-[#09090b] border border-zinc-200 dark:border-zinc-800 rounded-[8px] px-[12px] py-[8px] text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 text-zinc-950 dark:text-zinc-100 transition-all"
              placeholder="e.g. 2"
              required
            />
          </div>
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-[#059669] hover:bg-[#047857] text-[#ffffff] rounded-[8px] px-[16px] py-[10px] font-[500] transition-colors shadow-sm disabled:opacity-50 mt-4"
        >
          {loading ? 'Analyzing...' : 'Predict Claim Risk'}
        </button>
      </form>

      {result && (
        <div className={`mt-6 p-4 rounded-xl border ${result.error ? 'bg-rose-50 border-rose-200 dark:bg-rose-900/20 dark:border-rose-800/30' : 'bg-zinc-50 border-zinc-200 dark:bg-zinc-800/30 dark:border-zinc-700'}`}>
          {result.error ? (
            <p className="text-rose-600 dark:text-rose-400 text-sm font-medium">{result.error}</p>
          ) : (
            <div>
               <h4 className="text-sm font-bold text-zinc-950 dark:text-zinc-50 mb-2">Prediction Results</h4>
               <div className="flex justify-between items-center">
                 <span className="text-zinc-500 dark:text-zinc-400 text-sm">Risk Probability:</span>
                 <span className="text-2xl font-black text-zinc-950 dark:text-zinc-50">{(result.probability * 100).toFixed(1)}%</span>
               </div>
               <div className="flex justify-between items-center mt-2">
                 <span className="text-zinc-500 dark:text-zinc-400 text-sm">Risk Category:</span>
                 <span className={`px-2 py-1 rounded text-xs font-bold ${
                    result.risk_level === 'High' ? 'bg-rose-100 text-rose-700 dark:bg-rose-900/50 dark:text-rose-400' :
                    result.risk_level === 'Medium' ? 'bg-orange-100 text-orange-700 dark:bg-orange-900/50 dark:text-orange-400' :
                    'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/50 dark:text-emerald-400'
                  }`}>
                   {result.risk_level} Risk
                 </span>
               </div>
               <p className="text-xs text-zinc-400 mt-4 italic">{result.note}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default PredictionForm;
