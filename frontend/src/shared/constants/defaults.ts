

export const DEFAULT_ENVIRONMENT_CONTEXT = {
  avg_temperature_c: 23.5,
  total_rainfall_mm: 150,
  avg_humidity_percent: 75,
  avg_soil_moisture_0_7cm: 0.24,
  soil_score: 5.0,
  dominant_soil_type: 'Dat do bazan',
  soil_data_confidence: 'high' as const,
};

export const DEFAULT_MARKET_CONTEXT = {
  latest_price_vnd_per_kg: 90000,
  rolling_avg_price_vnd_per_kg: 90000,
  price_observations: 1,
  price_fill_method: 'observed' as const,
  coffee_type: 'Robusta / ca phe nhan xo noi dia',
};
