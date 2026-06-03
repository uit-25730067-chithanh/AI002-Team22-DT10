import React from 'react';
import { FeatureExplanation } from '../../../shared/api/prediction-types';
import { FEATURE_EXPLANATIONS } from '../../../shared/constants/feature-explanations';

interface FeatureImpactBarsProps {
  features: FeatureExplanation[];
}

const FeatureImpactBars: React.FC<FeatureImpactBarsProps> = ({ features }) => {
  if (!features || features.length === 0) return null;

  // Find max importance to calculate relative widths
  const maxImportance = Math.max(...features.map(f => f.importance));

  return (
    <div className="flex flex-col gap-4">
      {features.map((f, i) => {
        const width = `${(f.importance / maxImportance) * 100}%`;
        const translatedName = FEATURE_EXPLANATIONS[f.feature] || f.feature;
        
        return (
          <div key={i} className="flex flex-col gap-1">
            <div className="flex flex-wrap justify-between gap-2 text-sm font-semibold">
              <span>{translatedName}</span>
              <span className="text-coffee-700">Giá trị: {f.input_value}</span>
            </div>
            <div className="h-2 overflow-hidden rounded-full bg-coffee-100">
              <svg
                className="h-full w-full"
                role="img"
                aria-label={`Mức độ ảnh hưởng: ${(f.importance * 100).toFixed(1)}%`}
                preserveAspectRatio="none"
                viewBox="0 0 100 8"
              >
                <rect className="fill-coffee-100" width="100" height="8" rx="4" />
                <rect className="fill-coffee-500" width={width} height="8" rx="4" />
              </svg>
            </div>
            <p className="mt-0.5 text-sm text-coffee-700">{f.explanation}</p>
          </div>
        );
      })}
    </div>
  );
};

export default FeatureImpactBars;
