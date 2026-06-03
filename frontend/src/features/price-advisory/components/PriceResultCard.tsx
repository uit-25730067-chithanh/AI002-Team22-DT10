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
        <div className="rounded-lg border-l-4 border-orange-600 bg-orange-50 p-4 text-orange-900">
          <strong>⚠️ Lưu ý về dữ liệu:</strong> Tỉnh Đắk Nông hiện có ít dữ liệu lịch sử hơn các tỉnh khác, 
          do đó dự báo có thể có sai số lớn hơn bình thường.
        </div>
      )}

      <Card className="border-l-4 border-l-green-700">
        <h3 className="text-xl font-bold text-gray-900">Giá Cà Phê Dự Báo (Nhân xô)</h3>
        
        <div className="my-4 flex flex-wrap items-baseline gap-2">
          <span className="text-4xl font-black text-green-700 sm:text-5xl">{response.predicted_price_vnd.toLocaleString('vi-VN')}</span>
          <span className="text-xl font-semibold text-gray-600">VND/kg</span>
        </div>
        
        <div className="mb-4 rounded-lg border border-gray-200 bg-gray-50 p-3 text-gray-800">
          <strong>Khoảng giá an toàn (Độ tin cậy 95%):</strong>
          <p>{response.confidence_interval[0].toLocaleString('vi-VN')} - {response.confidence_interval[1].toLocaleString('vi-VN')} VND/kg</p>
        </div>

        <div className="flex items-center gap-2 text-sm text-gray-500">
          <span>Lõi mô hình:</span>
          <span className="rounded-full bg-gray-200 px-2 py-0.5 font-mono text-gray-700">{response.model_version}</span>
        </div>
      </Card>

      <Card>
        <h3 className="text-xl font-bold text-gray-900">Mức Độ Ảnh Hưởng</h3>
        <p className="mb-4 text-gray-600">Vì sao AI đưa ra mức giá này?</p>
        <FeatureImpactBars features={response.top_features} />
      </Card>

      <div className="flex flex-col gap-4">
        <div className="rounded-lg bg-green-50 p-4 text-sm text-green-900">
          <strong>🌍 Trục 4: Social Impact (Tác động xã hội)</strong>
          <p className="mt-1">
            Ứng dụng hỗ trợ thiết kế tối ưu hóa hiển thị ngoài trời và khu vực sóng yếu. Kết quả dự báo của bạn có thể được lưu lại thủ công để xem offline khi mất mạng. 
          </p>
        </div>
        
        <p className="text-center text-sm italic text-gray-500">{response.disclaimer}</p>
        <Button onClick={onSave} disabled={isSaved} variant={isSaved ? 'secondary' : 'primary'} fullWidth>
          {isSaved ? 'Đã lưu kết quả (Có thể xem offline)' : 'Lưu kết quả để xem offline'}
        </Button>
      </div>
    </div>
  );
};

export default PriceResultCard;
