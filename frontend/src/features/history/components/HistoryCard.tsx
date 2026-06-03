import React, { useState } from 'react';
import Card from '../../../shared/components/Card';
import Button from '../../../shared/components/Button';
import { SavedResult } from '../../../shared/storage/saved-results-repository';
import { formatDate, formatPrice } from '../helpers/history-formatters';
import { TRANSLATIONS } from '../../../shared/constants/translations';
import HistoryDetail from './HistoryDetail';

interface HistoryCardProps {
  result: SavedResult;
  onDelete: (id: string) => void;
}

const HistoryCard: React.FC<HistoryCardProps> = ({ result, onDelete }) => {
  const [isDetailOpen, setIsDetailOpen] = useState(false);
  const isPrice = result.type === 'price';
  
  return (
    <Card className="flex flex-col gap-2">
      <div className="flex items-center justify-between gap-3">
        <span className="text-sm text-coffee-700">{formatDate(result.date)}</span>
        <span className={`rounded-full px-2 py-0.5 text-xs font-semibold ${isPrice ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'}`}>
          {isPrice ? 'Giá Cà Phê' : 'Canh Tác'}
        </span>
      </div>
      
      <div className="font-semibold">
        {result.request.province} - {result.request.area} (Tháng {result.request.month}/{result.request.year})
      </div>

      <div className="rounded-lg border-2 border-coffee-800 bg-coffee-50 p-2 text-coffee-600">
        {isPrice ? (
          <strong>{formatPrice(result.response.predicted_price_vnd)}</strong>
        ) : (
          <strong>Hành động: {TRANSLATIONS[result.response.farming_recommendation.action] || result.response.farming_recommendation.action}</strong>
        )}
      </div>

      <div className="mt-2 flex flex-wrap justify-end gap-2">
        <Button
          variant="secondary"
          onClick={() => setIsDetailOpen((value) => !value)}
          aria-expanded={isDetailOpen}
        >
          {isDetailOpen ? 'Ẩn chi tiết' : 'Xem chi tiết'}
        </Button>
        <Button variant="secondary" onClick={() => onDelete(result.id)}>Xóa</Button>
      </div>

      {isDetailOpen && <HistoryDetail result={result} />}
    </Card>
  );
};

export default HistoryCard;
