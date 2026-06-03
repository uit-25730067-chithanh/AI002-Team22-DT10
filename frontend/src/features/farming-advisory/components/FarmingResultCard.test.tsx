import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import FarmingResultCard from './FarmingResultCard';
import { PredictionResponse } from '../../../shared/api/prediction-types';

describe('FarmingResultCard', () => {
  const mockResponse: PredictionResponse = {
    predicted_price_vnd: 95000,
    confidence_interval: [90000, 100000],
    top_features: [],
    model_version: 'v1.0',
    farming_recommendation: {
      action: 'harvest',
      season_type: 'main_season',
      confidence: 0.9,
      reasoning: 'Reasoning test',
      warnings: ['Warning 1'],
      next_action_month: 2,
      next_action: 'post_harvest_care',
      advisory_type: 'rule_based'
    },
    disclaimer: 'This is a test disclaimer'
  };

  it('renders farming recommendation details', () => {
    render(<FarmingResultCard response={mockResponse} onSave={vi.fn()} />);
    
    expect(screen.getByText('Thu hoạch quả chín')).toBeInTheDocument();
    expect(screen.getByText('Mùa vụ chính')).toBeInTheDocument();
    expect(screen.getByText('Reasoning test')).toBeInTheDocument();
    expect(screen.getByText('This is a test disclaimer')).toBeInTheDocument();
  });
});
