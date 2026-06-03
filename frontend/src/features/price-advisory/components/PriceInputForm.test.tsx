import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import PriceInputForm from './PriceInputForm';

describe('PriceInputForm', () => {
  it('renders form fields', () => {
    render(<PriceInputForm onSubmit={vi.fn()} isLoading={false} />);
    expect(screen.getByLabelText(/Tỉnh/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Huyện/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Tháng muốn xem/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Giá mua tại đại lý gần nhất/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Giá trung bình 7 kỳ gần đây/i)).toBeInTheDocument();
  });

  it('shows error if submitting empty form', () => {
    const handleSubmit = vi.fn();
    render(<PriceInputForm onSubmit={handleSubmit} isLoading={false} />);
    
    // Clear initial default values
    fireEvent.change(screen.getByLabelText(/Tỉnh/i), { target: { value: '' } });
    fireEvent.change(screen.getByLabelText(/Huyện/i), { target: { value: '' } });
    fireEvent.change(screen.getByLabelText(/Tháng muốn xem/i), { target: { value: '' } });
    fireEvent.change(screen.getByLabelText(/Giá mua tại đại lý gần nhất/i), { target: { value: '' } });
    fireEvent.change(screen.getByLabelText(/Giá trung bình 7 kỳ gần đây/i), { target: { value: '' } });
    
    fireEvent.click(screen.getByRole('button', { name: /Nhận Dự Báo Giá/i }));
    
    expect(handleSubmit).not.toHaveBeenCalled();
    expect(screen.getByText(/Vui lòng chọn Tỉnh/i)).toBeInTheDocument();
  });
});
