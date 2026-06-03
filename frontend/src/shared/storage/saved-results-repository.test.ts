import { describe, it, expect, beforeEach } from 'vitest';
import { saveResult, getResults, clearResults } from './saved-results-repository';
import { PredictionResponse } from '../api/prediction-types';

describe('saved-results-repository', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('saves and retrieves results', () => {
    const mockResponse: PredictionResponse = {
      predicted_price_vnd: 95000,
      confidence_interval: [90000, 100000],
      top_features: [],
      model_version: 'v1.0',
      farming_recommendation: {
        action: 'harvest',
        season_type: 'dry_season',
        confidence: 0.9,
        reasoning: 'Time to harvest',
        warnings: [],
        next_action_month: 2,
        next_action: 'post_harvest_care',
        advisory_type: 'rule_based'
      },
      disclaimer: 'Test'
    };

    saveResult({ 
      id: 'test-1',
      date: new Date().toISOString(),
      type: 'price',
      request: { province: 'Dak Lak', area: 'Buon Ma Thuot', month: 1, year: 2025 } as any,
      response: mockResponse
    });

    const results = getResults();
    expect(results.length).toBe(1);
    expect(results[0].id).toBe('test-1');
    expect(results[0].response.predicted_price_vnd).toBe(95000);
  });

  it('clears results', () => {
    saveResult({ id: 'test-1', date: '', type: 'price', request: {} as any, response: {} as any });
    clearResults();
    expect(getResults().length).toBe(0);
  });

  it('caps results at 20 items', () => {
    for (let i = 0; i < 25; i++) {
      saveResult({ id: `test-${i}`, date: '', type: 'price', request: {} as any, response: {} as any });
    }
    const results = getResults();
    expect(results.length).toBe(20);
    expect(results[0].id).toBe('test-24'); // Most recent
    expect(results[19].id).toBe('test-5'); // Oldest kept
  });
});
