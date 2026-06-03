import React from 'react';
import { AlertTriangle } from 'lucide-react';

interface FarmingWarningsProps {
  warnings: string[];
}

const FarmingWarnings: React.FC<FarmingWarningsProps> = ({ warnings }) => {
  if (!warnings || warnings.length === 0) return null;

  return (
    <div className="rounded-lg border-2 border-amber-600 bg-amber-100 p-3 text-amber-900">
      <div className="mb-2 flex items-center gap-2">
        <AlertTriangle size={20} className="text-amber-600" />
        <strong>Cảnh báo thời tiết/sâu bệnh:</strong>
      </div>
      <ul className="m-0 list-disc pl-6">
        {warnings.map((warning, index) => (
          <li className="mb-1" key={index}>{warning}</li>
        ))}
      </ul>
    </div>
  );
};

export default FarmingWarnings;
