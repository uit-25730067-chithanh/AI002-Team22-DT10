import { PredictionRequest } from '../../../shared/api/prediction-types';
import { DEFAULT_ENVIRONMENT_CONTEXT, DEFAULT_MARKET_CONTEXT } from '../../../shared/constants/defaults';

export function buildPricePredictionPayload(input: Partial<PredictionRequest>): PredictionRequest {
  return {
    province: input.province || '',
    area: input.area || '',
    month: input.month || new Date().getMonth() + 1,
    year: input.year || new Date().getFullYear(),
    latest_price_vnd_per_kg: input.latest_price_vnd_per_kg || DEFAULT_MARKET_CONTEXT.latest_price_vnd_per_kg,
    rolling_avg_price_vnd_per_kg: input.rolling_avg_price_vnd_per_kg || DEFAULT_MARKET_CONTEXT.rolling_avg_price_vnd_per_kg,
    price_observations: input.price_observations ?? DEFAULT_MARKET_CONTEXT.price_observations,
    price_fill_method: input.price_fill_method || DEFAULT_MARKET_CONTEXT.price_fill_method,
    coffee_type: input.coffee_type || DEFAULT_MARKET_CONTEXT.coffee_type,
    
    // Environment defaults for Price Flow
    avg_temperature_c: DEFAULT_ENVIRONMENT_CONTEXT.avg_temperature_c,
    total_rainfall_mm: DEFAULT_ENVIRONMENT_CONTEXT.total_rainfall_mm,
    avg_humidity_percent: DEFAULT_ENVIRONMENT_CONTEXT.avg_humidity_percent,
    avg_soil_moisture_0_7cm: DEFAULT_ENVIRONMENT_CONTEXT.avg_soil_moisture_0_7cm,
    soil_score: DEFAULT_ENVIRONMENT_CONTEXT.soil_score,
    dominant_soil_type: DEFAULT_ENVIRONMENT_CONTEXT.dominant_soil_type,
    soil_data_confidence: DEFAULT_ENVIRONMENT_CONTEXT.soil_data_confidence,
    
    // Override defaults with user input if provided
    ...input,
  } as PredictionRequest;
}
