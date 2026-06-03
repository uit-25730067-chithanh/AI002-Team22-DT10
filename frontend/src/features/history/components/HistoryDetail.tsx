import React from 'react';
import { SavedResult } from '../../../shared/storage/saved-results-repository';
import { FEATURE_EXPLANATIONS } from '../../../shared/constants/feature-explanations';
import { TRANSLATIONS } from '../../../shared/constants/translations';
import { formatPrice } from '../helpers/history-formatters';

interface HistoryDetailProps {
  result: SavedResult;
}

function formatNullable(value: string | number | null | undefined, fallback = 'Không có'): string {
  if (value === null || value === undefined || value === '') return fallback;
  return String(value);
}

function formatPercent(value: number | undefined): string {
  if (typeof value !== 'number') return '0%';
  return `${(value * 100).toFixed(1)}%`;
}

const HistoryDetail: React.FC<HistoryDetailProps> = ({ result }) => {
  const { request, response } = result;
  const recommendation = response.farming_recommendation;
  const confidenceInterval = response.confidence_interval;
  const topFeatures = response.top_features ?? [];

  return (
    <div className="mt-4 space-y-4 rounded-xl border-3 border-coffee-800 bg-coffee-50 p-4 text-coffee-900 shadow-hard">
      <section aria-label="Thông tin đầu vào đã lưu">
        <h4 className="mb-3 text-lg font-extrabold">Thông tin đã dùng</h4>
        <dl className="grid gap-3 sm:grid-cols-2">
          <div>
            <dt className="text-sm font-bold text-coffee-700">Khu vực</dt>
            <dd>{request.province} - {request.area}</dd>
          </div>
          <div>
            <dt className="text-sm font-bold text-coffee-700">Thời gian</dt>
            <dd>Tháng {request.month}/{request.year}</dd>
          </div>
          <div>
            <dt className="text-sm font-bold text-coffee-700">Nhiệt độ</dt>
            <dd>{formatNullable(request.avg_temperature_c)} °C</dd>
          </div>
          <div>
            <dt className="text-sm font-bold text-coffee-700">Lượng mưa</dt>
            <dd>{formatNullable(request.total_rainfall_mm)} mm</dd>
          </div>
          <div>
            <dt className="text-sm font-bold text-coffee-700">Độ ẩm không khí</dt>
            <dd>{formatNullable(request.avg_humidity_percent)}%</dd>
          </div>
          <div>
            <dt className="text-sm font-bold text-coffee-700">Giá gần nhất</dt>
            <dd>
              {typeof request.latest_price_vnd_per_kg === 'number'
                ? formatPrice(request.latest_price_vnd_per_kg)
                : 'Không có'}
            </dd>
          </div>
        </dl>
      </section>

      {result.type === 'price' && (
        <section aria-label="Chi tiết dự báo giá">
          <h4 className="mb-3 text-lg font-extrabold">Chi tiết giá</h4>
          <div className="rounded-lg border-2 border-coffee-800 bg-white p-3">
            <p>
              <strong>Giá dự báo:</strong> {formatPrice(response.predicted_price_vnd)}
            </p>
            {confidenceInterval && (
              <p>
                <strong>Khoảng dao động:</strong> {formatPrice(confidenceInterval[0])} -{' '}
                {formatPrice(confidenceInterval[1])}
              </p>
            )}
            <p>
              <strong>Model:</strong> {formatNullable(response.model_version)}
            </p>
          </div>

          {topFeatures.length > 0 && (
            <div className="mt-3 space-y-2">
              <h5 className="font-bold">Yếu tố ảnh hưởng chính</h5>
              {topFeatures.map((feature) => {
                const label = FEATURE_EXPLANATIONS[feature.feature] || feature.feature;
                return (
                  <div key={`${feature.feature}-${feature.importance}`} className="rounded-lg border-2 border-coffee-800 bg-white p-3">
                    <div className="flex flex-wrap items-center justify-between gap-2 font-bold">
                      <span>{label}</span>
                      <span>{formatPercent(feature.importance)}</span>
                    </div>
                    <p className="mt-1 text-sm text-coffee-700">{feature.explanation}</p>
                  </div>
                );
              })}
            </div>
          )}
        </section>
      )}

      {result.type === 'farming' && recommendation && (
        <section aria-label="Chi tiết khuyến nghị canh tác">
          <h4 className="mb-3 text-lg font-extrabold">Chi tiết canh tác</h4>
          <div className="space-y-2 rounded-lg border-2 border-coffee-800 bg-white p-3">
            <p>
              <strong>Hành động:</strong>{' '}
              {TRANSLATIONS[recommendation.action] || recommendation.action}
            </p>
            <p>
              <strong>Mùa vụ:</strong>{' '}
              {TRANSLATIONS[recommendation.season_type] || recommendation.season_type}
            </p>
            <p>
              <strong>Lý do:</strong> {recommendation.reasoning}
            </p>
            <p>
              <strong>Việc tháng {recommendation.next_action_month}:</strong>{' '}
              {TRANSLATIONS[recommendation.next_action] || recommendation.next_action}
            </p>
            {recommendation.warnings?.length > 0 && (
              <div>
                <strong>Cảnh báo:</strong>
                <ul className="mt-1 list-disc pl-5">
                  {recommendation.warnings.map((warning) => (
                    <li key={warning}>{warning}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </section>
      )}

      {response.disclaimer && (
        <p className="rounded-lg border-2 border-coffee-800 bg-amber-100 p-3 text-sm font-semibold text-coffee-900">
          {response.disclaimer}
        </p>
      )}
    </div>
  );
};

export default HistoryDetail;
