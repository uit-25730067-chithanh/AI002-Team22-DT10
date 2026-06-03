import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import PriceAdvisoryScreen from './PriceAdvisoryScreen';
import { PredictionResponse } from '../../shared/api/prediction-types';

const responseBody: PredictionResponse = {
  predicted_price_vnd: 90000,
  confidence_interval: [85000, 95000],
  top_features: [
    {
      feature: 'rolling_avg_7d',
      importance: 0.72,
      input_value: 82000,
      explanation: 'Giá gần đây ảnh hưởng mạnh đến dự báo.',
    },
  ],
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

describe('PriceAdvisoryScreen', () => {
  afterEach(() => {
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it('submits prediction using VITE_AI002_API_KEY', async () => {
    vi.stubEnv('VITE_AI002_API_KEY', 'local-demo-key');
    vi.stubEnv('VITE_API_BASE_URL', 'http://api.test');

    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(responseBody),
    });
    vi.stubGlobal('fetch', fetchMock);

    render(<PriceAdvisoryScreen />);

    fireEvent.click(screen.getByRole('button', { name: /Nhận Dự Báo Giá/i }));

    await waitFor(() => {
      expect(screen.getByText('90.000')).toBeInTheDocument();
    });
    expect(screen.queryByText(/Cannot read properties/i)).not.toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledWith(
      'http://api.test/predict',
      expect.objectContaining({
        headers: expect.objectContaining({
          'X-API-Key': 'local-demo-key',
        }),
      }),
    );
  });
});
