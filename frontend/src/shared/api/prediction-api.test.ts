import { afterEach, describe, expect, it, vi } from 'vitest';
import { fetchPrediction } from './prediction-api';
import { PredictionRequest, PredictionResponse } from './prediction-types';

const payload: PredictionRequest = {
  province: 'Lam Dong',
  area: 'Di Linh',
  avg_temperature_c: 23.5,
  total_rainfall_mm: 150,
  avg_humidity_percent: 75,
  coffee_type: 'robusta',
  price_fill_method: 'observed',
  dominant_soil_type: 'basalt',
  month: 7,
  year: 2026,
  latest_price_vnd_per_kg: 85000,
  rolling_avg_price_vnd_per_kg: 82000,
};

const responseBody: PredictionResponse = {
  predicted_price_vnd: 90000,
  confidence_interval: [85000, 95000],
  top_features: [],
  model_version: 'test-model',
  farming_recommendation: {
    action: 'growth_care',
    season_type: 'rainy_season',
    confidence: 0.8,
    reasoning: 'Test reasoning',
    warnings: [],
    next_action_month: 8,
    next_action: 'growth_care',
    advisory_type: 'rule_based',
  },
  disclaimer: 'Test disclaimer',
};

describe('fetchPrediction', () => {
  afterEach(() => {
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it('uses VITE_AI002_API_KEY for X-API-Key header', async () => {
    vi.stubEnv('VITE_AI002_API_KEY', 'frontend-demo-key');
    vi.stubEnv('AI002_API_KEY', 'legacy-demo-key');
    vi.stubEnv('VITE_API_BASE_URL', 'http://api.test');

    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(responseBody),
    });
    vi.stubGlobal('fetch', fetchMock);

    await fetchPrediction(payload);

    expect(fetchMock).toHaveBeenCalledWith(
      'http://api.test/predict',
      expect.objectContaining({
        headers: expect.objectContaining({
          'X-API-Key': 'frontend-demo-key',
        }),
      }),
    );
  });

  it('falls back to AI002_API_KEY for local env files', async () => {
    vi.stubEnv('VITE_AI002_API_KEY', '');
    vi.stubEnv('AI002_API_KEY', 'local-demo-key');
    vi.stubEnv('VITE_API_BASE_URL', 'http://api.test');

    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(responseBody),
    });
    vi.stubGlobal('fetch', fetchMock);

    await fetchPrediction(payload);

    expect(fetchMock).toHaveBeenCalledWith(
      'http://api.test/predict',
      expect.objectContaining({
        headers: expect.objectContaining({
          'X-API-Key': 'local-demo-key',
        }),
      }),
    );
  });

  it('throws a clear error when both frontend API keys are missing', async () => {
    vi.stubEnv('VITE_AI002_API_KEY', '');
    vi.stubEnv('AI002_API_KEY', '');

    await expect(fetchPrediction(payload)).rejects.toThrow(
      'VITE_AI002_API_KEY or AI002_API_KEY is missing',
    );
  });
});
