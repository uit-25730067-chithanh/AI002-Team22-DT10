import { PredictionRequest, PredictionResponse } from "./prediction-types";

const getPredictionApiConfig = () => {
  return {
    baseUrl: import.meta.env?.VITE_API_BASE_URL || "http://127.0.0.1:8000",
    apiKey:
      import.meta.env?.VITE_AI002_API_KEY || import.meta.env?.AI002_API_KEY,
  };
};

export async function fetchPrediction(
  payload: PredictionRequest,
): Promise<PredictionResponse> {
  const { baseUrl, apiKey } = getPredictionApiConfig();

  if (!apiKey) {
    throw new Error(
      "VITE_AI002_API_KEY or AI002_API_KEY is missing. Please configure it in your environment.",
    );
  }
  try {
    const response = await fetch(`${baseUrl}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": apiKey,
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      let errorMessage = "Lỗi kết nối đến máy chủ dự báo.";
      try {
        const errorData = await response.json();
        if (errorData.detail) {
          errorMessage =
            typeof errorData.detail === "string"
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
    throw new Error("Đã xảy ra lỗi không xác định khi kết nối API.");
  }
}
