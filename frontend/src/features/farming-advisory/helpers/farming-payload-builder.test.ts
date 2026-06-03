import { describe, it, expect } from 'vitest';
import { buildFarmingPredictionPayload } from './farming-payload-builder';
import { DEFAULT_MARKET_CONTEXT } from '../../../shared/constants/defaults';

describe('farming-payload-builder', () => {
  it('builds payload with user input and market defaults', () => {
    const input = {
      province: 'Lam Dong',
      area: 'Di Linh',
      month: 6,
      year: 2025,
      avg_temperature_c: 24,
      total_rainfall_mm: 200,
    };
    const payload = buildFarmingPredictionPayload(input);
    
    expect(payload.province).toBe('Lam Dong');
    expect(payload.area).toBe('Di Linh');
    expect(payload.month).toBe(6);
    expect(payload.avg_temperature_c).toBe(24);
    expect(payload.latest_price_vnd_per_kg).toBe(DEFAULT_MARKET_CONTEXT.latest_price_vnd_per_kg);
  });
});
