import React, { useState } from 'react';
import { AREA_MAPPING } from '../../../shared/constants/location-options';
import Button from '../../../shared/components/Button';

interface PriceInputFormProps {
  onSubmit: (data: any) => void;
  isLoading: boolean;
}

const PriceInputForm: React.FC<PriceInputFormProps> = ({ onSubmit, isLoading }) => {
  const [province, setProvince] = useState('Lam Dong');
  const [area, setArea] = useState('Di Linh');
  const [month, setMonth] = useState('7');
  const [latestPrice, setLatestPrice] = useState('85000');
  const [rollingPrice, setRollingPrice] = useState('82000');
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
    if (!latestPrice) newErrors.latestPrice = 'Vui lòng nhập Giá gần nhất';
    if (!rollingPrice) newErrors.rollingPrice = 'Vui lòng nhập Giá trung bình';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      // Optional: focus first error field
      return;
    }

    setErrors({});
    onSubmit({
      province,
      area,
      month: parseInt(month, 10),
      latest_price_vnd_per_kg: parseFloat(latestPrice),
      rolling_avg_price_vnd_per_kg: parseFloat(rollingPrice),
    });
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4" noValidate>
      <div className={formGroupClasses}>
        <label className={labelClasses} htmlFor="province">Tỉnh</label>
        <select
          id="province"
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
            <option key={p} value={p}>{p}</option>
          ))}
        </select>
        {errors.province && <span className={errorClasses}>{errors.province}</span>}
      </div>

      <div className={formGroupClasses}>
        <label className={labelClasses} htmlFor="area">Huyện</label>
        <select
          id="area"
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
        <label className={labelClasses} htmlFor="month">Tháng muốn xem</label>
        <select
          id="month"
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
        <label className={labelClasses} htmlFor="latestPrice">Giá mua tại đại lý gần nhất (VND/kg)</label>
        <input
          id="latestPrice"
          className={fieldClasses}
          type="number"
          value={latestPrice}
          onChange={(e) => setLatestPrice(e.target.value)}
          min="30000"
          max="200000"
          aria-invalid={!!errors.latestPrice}
        />
        {errors.latestPrice && <span className={errorClasses}>{errors.latestPrice}</span>}
      </div>

      <div className={formGroupClasses}>
        <label className={labelClasses} htmlFor="rollingPrice">Giá trung bình 7 kỳ gần đây (VND/kg)</label>
        <input
          id="rollingPrice"
          className={fieldClasses}
          type="number"
          value={rollingPrice}
          onChange={(e) => setRollingPrice(e.target.value)}
          min="30000"
          max="200000"
          aria-invalid={!!errors.rollingPrice}
        />
        {errors.rollingPrice && <span className={errorClasses}>{errors.rollingPrice}</span>}
      </div>

      <p className="rounded-lg border-l-4 border-coffee-500 bg-coffee-50 p-3 text-sm text-coffee-700">
        Các thông số về đất đai và thời tiết sẽ được hệ thống tự động sử dụng giá trị an toàn (bình thường) 
        của khu vực để tập trung dự báo giá.
      </p>

      <Button type="submit" fullWidth disabled={isLoading}>
        {isLoading ? 'Đang phân tích...' : 'Nhận Dự Báo Giá'}
      </Button>
    </form>
  );
};

export default PriceInputForm;
