import { PredictionRequest, PredictionResponse } from './prediction-types';

// Trong môi trường production hoặc testing, ta có thể inject biến môi trường
// Nếu không có, dùng mặc định local
const API_BASE_URL = import.meta.env?.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
const API_KEY = import.meta.env?.VITE_API_KEY;

export async function fetchPrediction(payload: PredictionRequest): Promise<PredictionResponse> {
  if (!API_KEY) {
    throw new Error('VITE_API_KEY is missing. Please configure it in your environment.');
  }
  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY,
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      let errorMessage = 'Lỗi kết nối đến máy chủ dự báo.';
      try {
        const errorData = await response.json();
        if (errorData.detail) {
          errorMessage = typeof errorData.detail === 'string' 
            ? errorData.detail 
            : JSON.stringify(errorData.detail);
        }
      } catch (e) {
        // Ignore JSON parse error for error response
      }
      throw new Error(errorMessage);
    }

    const data: PredictionResponse = await response.json();
    return data;
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Đã xảy ra lỗi không xác định khi kết nối API.');
  }
}
