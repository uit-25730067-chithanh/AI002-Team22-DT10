import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import PriceResultCard from './PriceResultCard';
import { PredictionResponse } from '../../../shared/api/prediction-types';

describe('PriceResultCard', () => {
  const mockResponse: PredictionResponse = {
    predicted_price_vnd: 95000,
    confidence_interval: [90000, 100000],
    top_features: [
      { feature: 'province', importance: 0.8, input_value: 1, explanation: 'Test explanation' }
    ],
    model_version: 'v1.0',
    farming_recommendation: {} as any,
    disclaimer: 'This is a test disclaimer'
  };

  it('renders predicted price and intervals', () => {
    render(<PriceResultCard response={mockResponse} onSave={vi.fn()} province="Dak Lak" />);
    expect(screen.getByText('95.000')).toBeInTheDocument();
    expect(screen.getByText('90.000 - 100.000 VND/kg')).toBeInTheDocument();
    expect(screen.getByText('This is a test disclaimer')).toBeInTheDocument();
  });

  it('shows bias warning for Dak Nong', () => {
    render(<PriceResultCard response={mockResponse} onSave={vi.fn()} province="Dak Nong" />);
    expect(screen.getByText(/Lưu ý về dữ liệu/i)).toBeInTheDocument();
  });
});
