import { PredictionRequest, PredictionResponse } from '../api/prediction-types';

const STORAGE_KEY = 'ai002_saved_results_v1';

export interface SavedResult {
  id: string;
  date: string;
  type: 'price' | 'farming';
  request: PredictionRequest;
  response: PredictionResponse;
}

export function saveResult(result: SavedResult): void {
  let results = getResults();
  results.unshift(result);
  if (results.length > 20) {
    results = results.slice(0, 20);
  }
  localStorage.setItem(STORAGE_KEY, JSON.stringify(results));
}

export function getResults(): SavedResult[] {
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    if (!data) return [];
    const parsed = JSON.parse(data);
    if (!Array.isArray(parsed)) return [];
    return parsed.filter((r: any) => r && typeof r === 'object' && 'id' in r && 'type' in r);
  } catch (e) {
    console.error('Failed to parse saved results', e);
    return [];
  }
}

export function deleteResult(id: string): void {
  const results = getResults().filter(r => r.id !== id);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(results));
}

export function clearResults(): void {
  localStorage.removeItem(STORAGE_KEY);
}
