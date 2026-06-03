import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import FeatureImpactBars from './FeatureImpactBars';

describe('FeatureImpactBars', () => {
  it('renders features and calculations correctly', () => {
    const features = [
      { feature: 'province', importance: 0.8, input_value: 1, explanation: 'Prov test' },
      { feature: 'area', importance: 0.4, input_value: 2, explanation: 'Area test' }
    ];
    
    render(<FeatureImpactBars features={features} />);
    
    // Checks translations if they exist, or fallback to feature name
    // We didn't mock TRANSLATIONS here, so it relies on the actual constants
    expect(screen.getByText('Yếu tố chênh lệch cung cầu cấp Tỉnh')).toBeInTheDocument();
    expect(screen.getByText('Đặc thù thổ nhưỡng và giao thông cấp Huyện')).toBeInTheDocument();
    
    expect(screen.getByText('Prov test')).toBeInTheDocument();
    expect(screen.getByText('Area test')).toBeInTheDocument();
  });
});
