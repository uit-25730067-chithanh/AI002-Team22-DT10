export type FarmingAction = 
  | 'post_harvest_care'
  | 'flowering_care'
  | 'growth_care'
  | 'harvest'
  | 'off_season';

export type SeasonType = 'dry_season' | 'rainy_season' | 'main_season' | 'off_season';

export interface PredictionRequest {
  province: string;
  area: string;
  avg_temperature_c: number;
  total_rainfall_mm: number;
  avg_humidity_percent?: number | null;
  avg_soil_moisture_0_7cm?: number | null;
  soil_score?: number | null;
  soil_data_confidence?: 'low' | 'medium' | 'high' | null;
  coffee_type: string;
  price_fill_method: 'observed' | 'interpolated_area' | 'province_proxy';
  dominant_soil_type: string;
  month: number;
  year: number;
  latest_price_vnd_per_kg?: number | null;
  rolling_avg_price_vnd_per_kg?: number | null;
  price_observations?: number | null;
}

export interface FeatureExplanation {
  feature: string;
  importance: number;
  input_value: number;
  explanation: string;
}

export interface FarmingRecommendation {
  action: FarmingAction;
  season_type: SeasonType;
  confidence: number;
  reasoning: string;
  warnings: string[];
  next_action_month: number;
  next_action: FarmingAction;
  advisory_type: 'rule_based';
}

export interface PredictionResponse {
  predicted_price_vnd: number;
  confidence_interval: [number, number];
  top_features: FeatureExplanation[];
  model_version: string;
  farming_recommendation: FarmingRecommendation;
  disclaimer: string;
}
