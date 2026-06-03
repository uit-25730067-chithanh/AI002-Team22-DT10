import React from 'react';
import Card from '../../../shared/components/Card';
import FarmingWarnings from './FarmingWarnings';
import { PredictionResponse } from '../../../shared/api/prediction-types';
import { TRANSLATIONS } from '../../../shared/constants/translations';
import Button from '../../../shared/components/Button';

interface FarmingResultCardProps {
  response: PredictionResponse;
  onSave: () => void;
  isSaved?: boolean;
}

const FarmingResultCard: React.FC<FarmingResultCardProps> = ({ response, onSave, isSaved }) => {
  const { farming_recommendation: rec } = response;

  const translatedAction = TRANSLATIONS[rec.action] || rec.action;
  const translatedSeason = TRANSLATIONS[rec.season_type] || rec.season_type;
  const translatedAdvisoryType = TRANSLATIONS[rec.advisory_type] || rec.advisory_type;
  const translatedNextAction = TRANSLATIONS[rec.next_action] || rec.next_action;

  return (
    <div className="flex flex-col gap-4">
      <Card className="border-l-4 border-l-green-700">
        <h3 className="text-xl font-bold text-gray-900">Khuyến Nghị Canh Tác Mùa Vụ</h3>
        
        <div className="mb-4 mt-2 flex flex-wrap gap-2">
          <span className="rounded-full bg-green-100 px-3 py-1 text-sm font-semibold text-green-800">{translatedSeason}</span>
          <span className="rounded-full bg-gray-100 px-3 py-1 text-sm text-gray-700">{translatedAdvisoryType}</span>
        </div>

        <div className="flex flex-col gap-4">
          <div className="rounded-lg border border-gray-200 bg-gray-50 p-3">
            <strong>Hành động nên làm:</strong>
            <p className="mt-1 text-xl font-bold text-green-700">{translatedAction}</p>
          </div>

          <div className="py-2 text-gray-800">
            <strong>Ghi chú chuyên gia nông nghiệp:</strong>
            <p>{rec.reasoning}</p>
          </div>

          <FarmingWarnings warnings={rec.warnings} />

          <div className="rounded-lg border border-gray-200 bg-gray-50 p-3">
            <strong>Việc cho tháng {rec.next_action_month}:</strong>
            <p className="mt-1 font-semibold text-gray-900">{translatedNextAction}</p>
          </div>
        </div>
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

export default FarmingResultCard;
