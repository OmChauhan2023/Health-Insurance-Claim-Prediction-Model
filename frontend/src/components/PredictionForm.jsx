import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Download, Activity, FileText } from 'lucide-react';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';

const PredictionForm = ({ onNewPrediction }) => {
  const [formData, setFormData] = useState({
    feature_1: 45, // Age
    feature_2: 28.5, // BMI
    feature_3: 0, // Conditions
    feature_4: 0, // Claims
  });
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const reportRef = useRef(null);

  // Trigger prediction whenever inputs change
  useEffect(() => {
    runPrediction(formData);
  }, [formData]);

  const runPrediction = async (data) => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/predict', {
        features: data
      });
      setResult(response.data);
      if (onNewPrediction) onNewPrediction(); // Trigger dashboard history refresh
    } catch (error) {
      console.error('Prediction failed', error);
      setResult({ error: 'Failed to connect to model API.' });
    }
    setLoading(false);
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: Number(e.target.value) });
  };

  const handleExportPDF = async () => {
    if (!reportRef.current) return;
    try {
      const canvas = await html2canvas(reportRef.current, { scale: 2 });
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
      
      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save(`Underwriting_Report_${Date.now()}.pdf`);
    } catch (err) {
      console.error("PDF Export failed", err);
    }
  };

  return (
    <div className="w-full flex flex-col md:flex-row gap-6">
      
      {/* What-If Interactive Controls */}
      <div className="flex-1 bg-zinc-50 dark:bg-zinc-900/40 p-4 rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm flex flex-col justify-between">
        <div className="flex items-center gap-1.5 mb-3 text-zinc-800 dark:text-zinc-200 font-bold text-sm">
          <Activity size={16} className="text-blue-500" /> What-If Scenario Builder
        </div>
        
        <form className="space-y-4">
          {/* Age Slider */}
          <div>
            <div className="flex justify-between items-end mb-1">
              <label className="text-xs font-semibold text-zinc-500 uppercase tracking-wider">Patient Age</label>
              <span className="text-sm font-bold text-blue-600 dark:text-blue-400">{formData.feature_1} yrs</span>
            </div>
            <input type="range" name="feature_1" min="18" max="90" value={formData.feature_1} onChange={handleChange}
              className="w-full h-2 bg-zinc-200 rounded-lg appearance-none cursor-pointer dark:bg-zinc-700 accent-blue-600" />
          </div>

          {/* BMI Slider */}
          <div>
            <div className="flex justify-between items-end mb-1">
              <label className="text-xs font-semibold text-zinc-500 uppercase tracking-wider">BMI</label>
              <span className="text-sm font-bold text-blue-600 dark:text-blue-400">{formData.feature_2}</span>
            </div>
            <input type="range" name="feature_2" min="15" max="50" step="0.5" value={formData.feature_2} onChange={handleChange}
              className="w-full h-2 bg-zinc-200 rounded-lg appearance-none cursor-pointer dark:bg-zinc-700 accent-blue-600" />
          </div>

          {/* Conditions Selector */}
          <div>
            <div className="flex justify-between items-end mb-1">
              <label className="text-xs font-semibold text-zinc-500 uppercase tracking-wider">Pre-existing Conditions</label>
              <span className="text-sm font-bold text-blue-600 dark:text-blue-400">
                {formData.feature_3 === 0 ? 'None' : formData.feature_3 === 1 ? 'Mild' : 'Severe'}
              </span>
            </div>
            <input type="range" name="feature_3" min="0" max="2" step="1" value={formData.feature_3} onChange={handleChange}
              className="w-full h-2 bg-zinc-200 rounded-lg appearance-none cursor-pointer dark:bg-zinc-700 accent-blue-600" />
          </div>

          {/* Claims Slider */}
          <div>
            <div className="flex justify-between items-end mb-1">
              <label className="text-xs font-semibold text-zinc-500 uppercase tracking-wider">Prior Claims</label>
              <span className="text-sm font-bold text-blue-600 dark:text-blue-400">{formData.feature_4} claims</span>
            </div>
            <input type="range" name="feature_4" min="0" max="10" step="1" value={formData.feature_4} onChange={handleChange}
              className="w-full h-2 bg-zinc-200 rounded-lg appearance-none cursor-pointer dark:bg-zinc-700 accent-blue-600" />
          </div>
        </form>
      </div>

      {/* Results & SHAP Explanations */}
      {result && !result.error && (
        <div ref={reportRef} className="flex-1 shrink-0 bg-white dark:bg-[#0c0c0f] p-4 rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-lg relative overflow-hidden flex flex-col justify-between">
          
          {/* Background Risk Glow */}
          <div className={`absolute -right-10 -top-10 w-32 h-32 blur-3xl opacity-20 rounded-full ${
            result.risk_level === 'High' ? 'bg-rose-500' : result.risk_level === 'Medium' ? 'bg-orange-500' : 'bg-emerald-500'
          }`} />

          <div className="relative z-10 flex-1">
            <h4 className="text-base font-black text-zinc-950 dark:text-zinc-50 mb-1 border-b border-zinc-100 dark:border-zinc-800/60 pb-1.5">
              Underwriting Prediction
            </h4>
            
            {/* Probability Output */}
            <div className="flex justify-between items-end mt-3 mb-4">
              <div>
                <p className="text-xs text-zinc-500 uppercase tracking-widest font-semibold mb-1">Calibrated Risk</p>
                <span className={`px-2.5 py-0.5 rounded text-xs font-bold uppercase tracking-wider ${
                    result.risk_level === 'High' ? 'bg-rose-100 text-rose-700 dark:bg-rose-900/50 dark:text-rose-400 border border-rose-200 dark:border-rose-800' :
                    result.risk_level === 'Medium' ? 'bg-orange-100 text-orange-700 dark:bg-orange-900/50 dark:text-orange-400 border border-orange-200 dark:border-orange-800' :
                    'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/50 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800'
                  }`}>
                    {result.risk_level} Priority
                </span>
              </div>
              <div className="text-right">
                <span className="text-3xl font-black text-zinc-950 dark:text-zinc-50 leading-none">
                  {(result.probability * 100).toFixed(1)}%
                </span>
              </div>
            </div>

            {/* Explainable AI (SHAP Values) */}
            {result.shap_values && (
              <div className="mt-3 pt-3 border-t border-zinc-100 dark:border-zinc-800/60">
                <p className="text-xs text-zinc-500 uppercase tracking-widest font-bold mb-2 flex items-center gap-1">
                  <Activity size={10} /> Top Risk Factors
                </p>
                <div className="space-y-2">
                  {result.shap_values.map((item, idx) => {
                    const isPositive = item.contribution > 0;
                    const widthPct = Math.min(100, Math.abs(item.contribution * 300)); // scaling for visual bar
                    return (
                      <div key={idx} className="flex flex-col gap-1">
                        <div className="flex justify-between text-xs font-semibold">
                          <span className="text-zinc-700 dark:text-zinc-300">{item.feature}</span>
                          <span className={isPositive ? 'text-rose-500' : 'text-emerald-500'}>
                            {isPositive ? '+' : ''}{(item.contribution * 100).toFixed(1)}%
                          </span>
                        </div>
                        <div className="w-full h-1.5 bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden flex">
                          <div 
                            className={`h-full rounded-full transition-all duration-300 ${isPositive ? 'bg-rose-500' : 'bg-emerald-500'}`} 
                            style={{ width: `${widthPct}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
          
          {/* PDF Export Button */}
          <button
            onClick={handleExportPDF}
            className="w-full flex items-center justify-center gap-2 bg-zinc-900 hover:bg-zinc-800 dark:bg-zinc-100 dark:hover:bg-white dark:text-zinc-900 text-white rounded-xl px-4 py-2.5 text-sm font-semibold transition-colors shadow-sm mt-4"
          >
            <FileText size={16} /> Export Underwriting PDF
          </button>
        </div>
      )}

      {/* Error State */}
      {result?.error && (
        <div className="p-4 rounded-xl border bg-rose-50 border-rose-200 text-rose-600 text-sm font-medium">
          {result.error}
        </div>
      )}

    </div>
  );
};

export default PredictionForm;
