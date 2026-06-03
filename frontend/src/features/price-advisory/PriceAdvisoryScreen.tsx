import React, { useState } from "react";
import PriceInputForm from "./components/PriceInputForm";
import PriceResultCard from "./components/PriceResultCard";
import { fetchPrediction } from "../../shared/api/prediction-api";
import {
  PredictionResponse,
  PredictionRequest,
} from "../../shared/api/prediction-types";
import { buildPricePredictionPayload } from "./helpers/price-payload-builder";
import { saveResult } from "../../shared/storage/saved-results-repository";

const PriceAdvisoryScreen: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [lastRequest, setLastRequest] = useState<PredictionRequest | null>(
    null,
  );
  const [isSaved, setIsSaved] = useState(false);

  const handleSubmit = async (formData: Partial<PredictionRequest>) => {
    setIsLoading(true);
    setError(null);
    setIsSaved(false);

    try {
      const payload = buildPricePredictionPayload(formData);
      setLastRequest(payload);

      const response = await fetchPrediction(payload);
      setResult(response);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Có lỗi xảy ra.");
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
      type: "price",
      request: lastRequest,
      response: result,
    });
    setIsSaved(true);
  };

  return (
    <div className="flex flex-col gap-8 py-8">
      <header>
        <h2 className="text-2xl font-extrabold text-coffee-900">Dự báo Giá Cà Phê</h2>
        <p className="mt-2 text-coffee-700">
          Nhập thông tin cơ bản để nhận dự báo giá và mức độ biến động trong
          thời gian tới.
        </p>
      </header>

      {error && (
        <div className="rounded-lg border-l-4 border-red-600 bg-red-50 p-4 text-red-800">
          <strong>Lỗi:</strong> {error}
        </div>
      )}

      {!result && (
        <PriceInputForm onSubmit={handleSubmit} isLoading={isLoading} />
      )}

      {result && lastRequest && (
        <div className="flex flex-col gap-8">
          <PriceResultCard
            response={result}
            onSave={handleSave}
            isSaved={isSaved}
            province={lastRequest.province}
          />
          <button
            onClick={() => setResult(null)}
            className="self-center border-0 bg-transparent font-semibold text-coffee-600 underline"
          >
            Tạo dự báo mới
          </button>
        </div>
      )}
    </div>
  );
};

export default PriceAdvisoryScreen;
