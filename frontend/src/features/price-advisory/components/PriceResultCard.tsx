import React from 'react';
import Card from '../../../shared/components/Card';
import FeatureImpactBars from './FeatureImpactBars';
import { PredictionResponse } from '../../../shared/api/prediction-types';
import Button from '../../../shared/components/Button';

interface PriceResultCardProps {
  response: PredictionResponse;
  onSave: () => void;
  isSaved?: boolean;
  province: string;
}

const PriceResultCard: React.FC<PriceResultCardProps> = ({ response, onSave, isSaved, province }) => {
  const showBiasWarning = province === 'Dak Nong';

  return (
    <div className="flex flex-col gap-6">
      {showBiasWarning && (
        <div className="rounded-lg border-l-4 border-red-600 bg-red-50 p-4 text-red-800">
          <strong>⚠️ Lưu ý về dữ liệu:</strong> Tỉnh Đắk Nông hiện có ít dữ liệu lịch sử hơn các tỉnh khác, 
          do đó dự báo có thể có sai số lớn hơn bình thường.
        </div>
      )}

      <Card className="border-coffee-500">
        <h3 className="text-xl font-extrabold">Giá Cà Phê Dự Báo (Nhân xô)</h3>
        
        <div className="my-4 flex flex-wrap items-baseline gap-2">
          <span className="text-4xl font-black text-coffee-500 sm:text-5xl">{response.predicted_price_vnd.toLocaleString('vi-VN')}</span>
          <span className="text-xl font-semibold text-coffee-700">VND/kg</span>
        </div>
        
        <div className="mb-4 rounded-lg border-2 border-coffee-800 bg-coffee-50 p-3">
          <strong>Khoảng giá an toàn (Độ tin cậy 95%):</strong>
          <p>{response.confidence_interval[0].toLocaleString('vi-VN')} - {response.confidence_interval[1].toLocaleString('vi-VN')} VND/kg</p>
        </div>

        <div className="flex items-center gap-2 text-sm text-coffee-700">
          <span>Lõi mô hình:</span>
          <span className="rounded-full bg-coffee-100 px-2 py-0.5 font-mono text-coffee-900">{response.model_version}</span>
        </div>
      </Card>

      <Card>
        <h3 className="text-xl font-extrabold">Mức Độ Ảnh Hưởng</h3>
        <p className="mb-4 text-coffee-700">Vì sao AI đưa ra mức giá này?</p>
        <FeatureImpactBars features={response.top_features} />
      </Card>

      <div className="flex flex-col gap-4">
        <p className="text-center text-sm italic text-coffee-700">{response.disclaimer}</p>
        <Button onClick={onSave} disabled={isSaved} variant={isSaved ? 'secondary' : 'primary'} fullWidth>
          {isSaved ? 'Đã lưu kết quả' : 'Lưu kết quả này'}
        </Button>
      </div>
    </div>
  );
};

export default PriceResultCard;
