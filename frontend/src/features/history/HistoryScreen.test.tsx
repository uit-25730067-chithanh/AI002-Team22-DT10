import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import HistoryScreen from './HistoryScreen';
import * as repo from '../../shared/storage/saved-results-repository';

vi.mock('../../shared/storage/saved-results-repository', () => ({
  getResults: vi.fn(),
  deleteResult: vi.fn(),
  clearResults: vi.fn(),
}));

describe('HistoryScreen', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders empty state', () => {
    vi.mocked(repo.getResults).mockReturnValue([]);
    render(<HistoryScreen />);
    expect(screen.getByText('Lịch sử trống')).toBeInTheDocument();
  });

  it('renders list of results', () => {
    vi.mocked(repo.getResults).mockReturnValue([
      {
        id: '1',
        date: new Date().toISOString(),
        type: 'price',
        request: { province: 'Dak Lak', area: 'Buon Ma Thuot', month: 1, year: 2025 } as any,
        response: {
          predicted_price_vnd: 95000,
          confidence_interval: [90000, 100000],
          top_features: [],
          model_version: 'test-model',
          disclaimer: 'Chỉ tham khảo',
        } as any,
      }
    ]);
    render(<HistoryScreen />);
    expect(screen.getByText('Dak Lak - Buon Ma Thuot (Tháng 1/2025)')).toBeInTheDocument();
    expect(screen.getByText('95.000 VND/kg')).toBeInTheDocument();
  });

  it('shows price result details when requested', () => {
    vi.mocked(repo.getResults).mockReturnValue([
      {
        id: '1',
        date: new Date().toISOString(),
        type: 'price',
        request: {
          province: 'Dak Lak',
          area: 'Buon Ma Thuot',
          month: 1,
          year: 2025,
          avg_temperature_c: 24,
          total_rainfall_mm: 120,
          latest_price_vnd_per_kg: 92000,
        } as any,
        response: {
          predicted_price_vnd: 95000,
          confidence_interval: [90000, 100000],
          top_features: [
            {
              feature: 'lag_1d',
              importance: 0.42,
              input_value: 92000,
              explanation: 'Giá tháng trước ảnh hưởng mạnh.',
            },
          ],
          model_version: 'test-model',
          disclaimer: 'Chỉ tham khảo',
        } as any,
      }
    ]);

    render(<HistoryScreen />);
    fireEvent.click(screen.getByText('Xem chi tiết'));

    expect(screen.getByText('Thông tin đã dùng')).toBeInTheDocument();
    expect(screen.getByText('Chi tiết giá')).toBeInTheDocument();
    expect(screen.getByText('Khoảng dao động:')).toBeInTheDocument();
    expect(screen.getByText('Giá tháng trước ảnh hưởng mạnh.')).toBeInTheDocument();
    expect(screen.getByText('Chỉ tham khảo')).toBeInTheDocument();
  });

  it('shows farming result details when requested', () => {
    vi.mocked(repo.getResults).mockReturnValue([
      {
        id: '2',
        date: new Date().toISOString(),
        type: 'farming',
        request: {
          province: 'Lam Dong',
          area: 'Di Linh',
          month: 6,
          year: 2025,
          avg_temperature_c: 22,
          total_rainfall_mm: 180,
        } as any,
        response: {
          predicted_price_vnd: 94000,
          confidence_interval: [90000, 98000],
          top_features: [],
          model_version: 'test-model',
          farming_recommendation: {
            action: 'growth_care',
            season_type: 'rainy_season',
            confidence: 0.8,
            reasoning: 'Mùa mưa cần phòng nấm bệnh.',
            warnings: ['Mưa nhiều, kiểm tra thoát nước.'],
            next_action_month: 7,
            next_action: 'growth_care',
            advisory_type: 'rule_based',
          },
          disclaimer: 'Chỉ tham khảo',
        } as any,
      }
    ]);

    render(<HistoryScreen />);
    fireEvent.click(screen.getByText('Xem chi tiết'));

    expect(screen.getByText('Chi tiết canh tác')).toBeInTheDocument();
    expect(screen.getByText('Mùa mưa cần phòng nấm bệnh.')).toBeInTheDocument();
    expect(screen.getByText('Mưa nhiều, kiểm tra thoát nước.')).toBeInTheDocument();
  });

  it('handles clear all', () => {
    vi.spyOn(window, 'confirm').mockReturnValue(true);
    vi.mocked(repo.getResults).mockReturnValue([
      {
        id: '1',
        date: new Date().toISOString(),
        type: 'price',
        request: { province: 'Dak Lak', area: 'Buon Ma Thuot', month: 1, year: 2025 } as any,
        response: { predicted_price_vnd: 95000 } as any,
      }
    ]);
    
    render(<HistoryScreen />);
    fireEvent.click(screen.getByText('Xóa tất cả'));
    
    expect(repo.clearResults).toHaveBeenCalled();
  });
});
