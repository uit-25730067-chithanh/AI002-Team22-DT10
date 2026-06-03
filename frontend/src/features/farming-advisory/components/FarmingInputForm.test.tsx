import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import FarmingInputForm from './FarmingInputForm';

describe('FarmingInputForm', () => {
  it('renders form fields', () => {
    render(<FarmingInputForm onSubmit={vi.fn()} isLoading={false} />);
    expect(screen.getByLabelText(/Tỉnh/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Huyện/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Tháng/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Nhiệt độ/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Lượng mưa/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Độ ẩm/i)).toBeInTheDocument();
  });

  it('shows error if submitting empty form', () => {
    const handleSubmit = vi.fn();
    render(<FarmingInputForm onSubmit={handleSubmit} isLoading={false} />);
    
    fireEvent.click(screen.getByRole('button', { name: /Nhận Khuyến Nghị/i }));
    
    expect(handleSubmit).not.toHaveBeenCalled();
    expect(screen.getByText(/Vui lòng chọn Tỉnh/i)).toBeInTheDocument();
  });
});
