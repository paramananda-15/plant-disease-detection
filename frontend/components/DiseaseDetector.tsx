'use client';

import { useState } from 'react';

const API_URL = "http://localhost:8000";

interface Product {
  name: string;
  type: string;
  usage: string;
  price: string;
}

interface PredictionResult {
  label: string;
  display_name: string;
  confidence: number;
  top_3: Array<{ label: string; display_name: string; confidence: number }>;
}

interface DiseaseInfo {
  description: string;
  symptoms: string;
  severity: string;
}

interface ApiResponse {
  success: boolean;
  prediction: PredictionResult;
  disease_info: DiseaseInfo;
  products: Product[];
  treatment_advice: string[];
}

export default function DiseaseDetector() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string>('');
  const [result, setResult] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setResult(null);
      setError('');
    }
  };

  const handlePredict = async () => {
    if (!file) return;
    
    setLoading(true);
    setError('');
    
    try {
      const formData = new FormData();
      formData.append('image', file);
      
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Prediction failed');
      }
      
      const data: ApiResponse = await response.json();
      setResult(data);
    } catch (err) {
      setError('Failed to analyze image. Please try again.');
      console.error('Prediction error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity: string) => {
    const colors: Record<string, string> = {
      'Very High': 'text-red-700 bg-red-50 border-red-200',
      'High': 'text-orange-700 bg-orange-50 border-orange-200',
      'Moderate': 'text-yellow-700 bg-yellow-50 border-yellow-200',
      'Low': 'text-green-700 bg-green-50 border-green-200',
      'Unknown': 'text-gray-700 bg-gray-50 border-gray-200'
    };
    return colors[severity] || colors['Unknown'];
  };

  const getProductTypeColor = (type: string) => {
    const colors: Record<string, string> = {
      'Fungicide': 'bg-purple-100 text-purple-800',
      'Insecticide': 'bg-blue-100 text-blue-800',
      'Fertilizer': 'bg-green-100 text-green-800',
      'Organic': 'bg-emerald-100 text-emerald-800',
      'Micronutrient': 'bg-teal-100 text-teal-800',
      'Physical Control': 'bg-amber-100 text-amber-800',
      'Growth Promoter': 'bg-lime-100 text-lime-800',
      'Soil Conditioner': 'bg-yellow-100 text-yellow-800'
    };
    return colors[type] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            🌱 PlantVillage AI
          </h1>
          <p className="text-gray-600 text-lg">
            Detect plant diseases and get treatment product recommendations
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
          <div className="border-2 border-dashed border-gray-300 rounded-xl p-10 text-center hover:border-green-500 transition-colors">
            <input
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              className="hidden"
              id="file-upload"
            />
            <label htmlFor="file-upload" className="cursor-pointer">
              <div className="space-y-4">
                <div className="text-6xl">📸</div>
                <div>
                  <p className="text-lg font-semibold text-gray-700">
                    Click to upload plant image
                  </p>
                  <p className="text-sm text-gray-500 mt-1">
                    PNG, JPG, JPEG up to 10MB
                  </p>
                </div>
              </div>
            </label>
          </div>

          {preview && (
            <div className="mt-6 space-y-4">
              <div className="relative w-full h-96 rounded-xl overflow-hidden">
                <img
                  src={preview}
                  alt="Preview"
                  className="w-full h-full object-contain bg-gray-100"
                />
              </div>
              
              <button
                onClick={handlePredict}
                disabled={loading}
                className="w-full bg-green-600 text-white py-4 rounded-xl font-semibold text-lg hover:bg-green-700 disabled:bg-gray-400 transition-colors shadow-lg"
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    Analyzing...
                  </span>
                ) : '🔍 Detect Disease'}
              </button>
            </div>
          )}

          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {error}
            </div>
          )}
        </div>

        {result && (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                <span className="mr-3">🔬</span>
                Detection Results
              </h2>
              
              <div className="space-y-6">
                <div className="border-l-4 border-green-500 pl-6 py-4 bg-green-50 rounded-r-xl">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <p className="text-sm text-gray-600 mb-1">Detected Disease</p>
                      <p className="text-2xl font-bold text-gray-900 mb-2">
                        {result.prediction.display_name}
                      </p>
                      <div className="flex items-center gap-4">
                        <div>
                          <p className="text-sm text-gray-600">Confidence</p>
                          <p className="text-xl font-semibold text-green-700">
                            {(result.prediction.confidence * 100).toFixed(2)}%
                          </p>
                        </div>
                        <div className={`px-4 py-2 rounded-lg border ${getSeverityColor(result.disease_info.severity)}`}>
                          <p className="text-sm font-semibold">
                            {result.disease_info.severity} Severity
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-4">
                  <div className="p-4 bg-blue-50 rounded-xl">
                    <p className="text-sm font-semibold text-blue-900 mb-2">📖 Description</p>
                    <p className="text-gray-700">{result.disease_info.description}</p>
                  </div>
                  <div className="p-4 bg-amber-50 rounded-xl">
                    <p className="text-sm font-semibold text-amber-900 mb-2">⚠️ Symptoms</p>
                    <p className="text-gray-700">{result.disease_info.symptoms}</p>
                  </div>
                </div>

                <div>
                  <p className="text-sm font-semibold text-gray-700 mb-3">Alternative Possibilities</p>
                  <div className="space-y-2">
                    {result.prediction.top_3.slice(1).map((pred, idx) => (
                      <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <span className="text-gray-700">{pred.display_name}</span>
                        <span className="text-gray-600 font-mono">
                          {(pred.confidence * 100).toFixed(2)}%
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {result.treatment_advice && result.treatment_advice.length > 0 && (
              <div className="bg-white rounded-2xl shadow-lg p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                  <span className="mr-3">💡</span>
                  Treatment Advice
                </h2>
                <ul className="space-y-3">
                  {result.treatment_advice.map((advice, idx) => (
                    <li key={idx} className="flex items-start">
                      <span className="flex-shrink-0 w-6 h-6 bg-green-500 text-white rounded-full flex items-center justify-center text-sm font-bold mr-3 mt-0.5">
                        {idx + 1}
                      </span>
                      <span className="text-gray-700 flex-1">{advice}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {result.products && result.products.length > 0 && (
              <div className="bg-white rounded-2xl shadow-lg p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                  <span className="mr-3">🛒</span>
                  Recommended Products ({result.products.length})
                </h2>
                <div className="grid md:grid-cols-2 gap-4">
                  {result.products.map((product, idx) => (
                    <div key={idx} className="border border-gray-200 rounded-xl p-5 hover:shadow-md transition-shadow">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <h3 className="font-bold text-lg text-gray-900 mb-1">
                            {product.name}
                          </h3>
                          <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${getProductTypeColor(product.type)}`}>
                            {product.type}
                          </span>
                        </div>
                      </div>
                      <div className="space-y-2 text-sm">
                        <div className="flex items-start">
                          <span className="text-gray-500 w-16 flex-shrink-0">Usage:</span>
                          <span className="text-gray-700 flex-1">{product.usage}</span>
                        </div>
                        <div className="flex items-center justify-between pt-2 border-t">
                          <span className="text-gray-500">Price:</span>
                          <span className="text-green-700 font-bold text-lg">{product.price}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
