import React, { useState } from 'react';
import { AREA_MAPPING, PROVINCE_DISPLAY_MAPPING } from '../../../shared/constants/location-options';
import Button from '../../../shared/components/Button';
import { PredictionRequest } from '../../../shared/api/prediction-types';

interface FarmingInputFormProps {
  onSubmit: (data: Partial<PredictionRequest>) => void;
  isLoading: boolean;
}

const FarmingInputForm: React.FC<FarmingInputFormProps> = ({ onSubmit, isLoading }) => {
  const [province, setProvince] = useState('');
  const [area, setArea] = useState('');
  const [month, setMonth] = useState('');
  const [temp, setTemp] = useState('23.5');
  const [rainfall, setRainfall] = useState('150');
  const [humidity, setHumidity] = useState('75');
  const [errors, setErrors] = useState<Record<string, string>>({});

  const areas = province ? AREA_MAPPING[province] || [] : [];
  const fieldClasses =
    'rounded-lg border border-gray-300 bg-white p-3 font-sans text-base min-h-[48px] focus:outline focus:outline-[2px] focus:-outline-offset-2 focus:outline-green-700 aria-[invalid=true]:border-red-600 disabled:bg-gray-100 disabled:text-gray-500';
  const formGroupClasses = 'flex flex-col gap-2';
  const labelClasses = 'font-semibold text-gray-900';
  const errorClasses = 'text-sm font-semibold text-red-600';

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: Record<string, string> = {};
    if (!province) newErrors.province = 'Vui lòng chọn Tỉnh';
    if (!area) newErrors.area = 'Vui lòng chọn Huyện';
    if (!month) newErrors.month = 'Vui lòng chọn Tháng';
    if (!temp) newErrors.temp = 'Vui lòng nhập Nhiệt độ';
    if (!rainfall) newErrors.rainfall = 'Vui lòng nhập Lượng mưa';
    if (!humidity) newErrors.humidity = 'Vui lòng nhập Độ ẩm';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setErrors({});
    onSubmit({
      province,
      area,
      month: parseInt(month, 10),
      avg_temperature_c: parseFloat(temp),
      total_rainfall_mm: parseFloat(rainfall),
      avg_humidity_percent: parseFloat(humidity),
    });
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4" noValidate>
      <div className={formGroupClasses}>
        <label className={labelClasses} htmlFor="f-province">Tỉnh</label>
        <select
          id="f-province"
          className={fieldClasses}
          value={province}
          onChange={(e) => {
            setProvince(e.target.value);
            setArea('');
          }}
          aria-invalid={!!errors.province}
        >
          <option value="">-- Chọn Tỉnh --</option>
          {Object.keys(AREA_MAPPING).map(p => (
            <option key={p} value={p}>{PROVINCE_DISPLAY_MAPPING[p] || p}</option>
          ))}
        </select>
        {errors.province && <span className={errorClasses}>{errors.province}</span>}
      </div>

      <div className={formGroupClasses}>
        <label className={labelClasses} htmlFor="f-area">Huyện</label>
        <select
          id="f-area"
          className={fieldClasses}
          value={area}
          onChange={(e) => setArea(e.target.value)}
          disabled={!province}
          aria-invalid={!!errors.area}
        >
          <option value="">-- Chọn Huyện --</option>
          {areas.map(a => (
            <option key={a.value} value={a.value}>{a.text}</option>
          ))}
        </select>
        {errors.area && <span className={errorClasses}>{errors.area}</span>}
      </div>

      <div className={formGroupClasses}>
        <label className={labelClasses} htmlFor="f-month">Tháng muốn xem</label>
        <select
          id="f-month"
          className={fieldClasses}
          value={month}
          onChange={(e) => setMonth(e.target.value)}
          aria-invalid={!!errors.month}
        >
          <option value="">-- Chọn Tháng --</option>
          {Array.from({ length: 12 }).map((_, i) => (
            <option key={i + 1} value={i + 1}>Tháng {i + 1}</option>
          ))}
        </select>
        {errors.month && <span className={errorClasses}>{errors.month}</span>}
      </div>

      <div className={formGroupClasses}>
        <label className={labelClasses} htmlFor="f-temp">Nhiệt độ môi trường (°C)</label>
        <input
          id="f-temp"
          className={fieldClasses}
          type="number"
          step="0.1"
          value={temp}
          onChange={(e) => setTemp(e.target.value)}
          onWheel={(e) => e.currentTarget.blur()}
          min="10"
          max="45"
          aria-invalid={!!errors.temp}
        />
        {errors.temp && <span className={errorClasses}>{errors.temp}</span>}
      </div>

      <div className={formGroupClasses}>
        <label className={labelClasses} htmlFor="f-rainfall">Lượng mưa ước tính (mm)</label>
        <input
          id="f-rainfall"
          className={fieldClasses}
          type="number"
          value={rainfall}
          onChange={(e) => setRainfall(e.target.value)}
          onWheel={(e) => e.currentTarget.blur()}
          min="0"
          max="1000"
          aria-invalid={!!errors.rainfall}
        />
        {errors.rainfall && <span className={errorClasses}>{errors.rainfall}</span>}
      </div>

      <div className={formGroupClasses}>
        <label className={labelClasses} htmlFor="f-humidity">Độ ẩm không khí (%)</label>
        <input
          id="f-humidity"
          className={fieldClasses}
          type="number"
          value={humidity}
          onChange={(e) => setHumidity(e.target.value)}
          onWheel={(e) => e.currentTarget.blur()}
          min="0"
          max="100"
          aria-invalid={!!errors.humidity}
        />
        {errors.humidity && <span className={errorClasses}>{errors.humidity}</span>}
      </div>

      <p className="rounded-lg border-l-4 border-leaf-500 bg-green-50 p-3 text-sm text-coffee-700">
        Hệ thống hiện dùng chung lõi dự báo nên dữ liệu thị trường sẽ dùng giá mặc định tự động.
        Bạn không cần quan tâm đến thị trường trong tính năng này.
      </p>

      <Button type="submit" fullWidth disabled={isLoading}>
        {isLoading ? 'Đang phân tích...' : 'Nhận Khuyến Nghị Canh Tác'}
      </Button>
    </form>
  );
};

export default FarmingInputForm;
