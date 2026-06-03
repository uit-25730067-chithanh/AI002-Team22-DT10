import React, { useState } from 'react';
import FarmingInputForm from './components/FarmingInputForm';
import FarmingResultCard from './components/FarmingResultCard';
import { fetchPrediction } from '../../shared/api/prediction-api';
import { PredictionResponse, PredictionRequest } from '../../shared/api/prediction-types';
import { buildFarmingPredictionPayload } from './helpers/farming-payload-builder';
import { saveResult } from '../../shared/storage/saved-results-repository';

const FarmingAdvisoryScreen: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [lastRequest, setLastRequest] = useState<PredictionRequest | null>(null);
  const [isSaved, setIsSaved] = useState(false);

  const handleSubmit = async (formData: Partial<PredictionRequest>) => {
    setIsLoading(true);
    setError(null);
    setIsSaved(false);
    
    try {
      const payload = buildFarmingPredictionPayload(formData);
      setLastRequest(payload);
      
      const response = await fetchPrediction(payload);
      setResult(response);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Có lỗi xảy ra.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = () => {
    if (!result || !lastRequest) return;
    
    saveResult({
      id: crypto.randomUUID(),
      date: new Date().toISOString(),
      type: 'farming',
      request: lastRequest,
      response: result,
    });
    setIsSaved(true);
  };

  return (
    <div className="flex flex-col gap-8 py-8">
      <header>
        <h2 className="text-2xl font-extrabold text-coffee-900">Khuyến Nghị Canh Tác</h2>
        <p className="mt-2 text-coffee-700">Nhập thông tin thời tiết dự kiến để nhận khuyến nghị hành động chăm sóc cà phê phù hợp.</p>
      </header>

      {error && (
        <div className="rounded-lg border-l-4 border-red-600 bg-red-50 p-4 text-red-800">
          <strong>Lỗi:</strong> {error}
        </div>
      )}

      {!result && (
        <FarmingInputForm onSubmit={handleSubmit} isLoading={isLoading} />
      )}

      {result && lastRequest && (
        <div className="flex flex-col gap-8">
          <FarmingResultCard 
            response={result} 
            onSave={handleSave} 
            isSaved={isSaved} 
          />
          <button 
            onClick={() => setResult(null)}
            className="self-center border-0 bg-transparent font-semibold text-leaf-600 underline"
          >
            Tạo khuyến nghị mới
          </button>
        </div>
      )}
    </div>
  );
};

export default FarmingAdvisoryScreen;
