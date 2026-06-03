import { describe, it, expect } from 'vitest';
import { buildPricePredictionPayload } from './price-payload-builder';
import { DEFAULT_ENVIRONMENT_CONTEXT } from '../../../shared/constants/defaults';

describe('price-payload-builder', () => {
  it('builds payload with user input and environment defaults', () => {
    const input = {
      province: 'Dak Lak',
      area: "Cu M'gar",
      month: 5,
      year: 2025,
      latest_price_vnd_per_kg: 95000,
      rolling_avg_price_vnd_per_kg: 93000,
    };
    const payload = buildPricePredictionPayload(input);
    
    expect(payload.province).toBe('Dak Lak');
    expect(payload.area).toBe("Cu M'gar");
    expect(payload.month).toBe(5);
    expect(payload.latest_price_vnd_per_kg).toBe(95000);
    expect(payload.avg_temperature_c).toBe(DEFAULT_ENVIRONMENT_CONTEXT.avg_temperature_c);
  });
});
