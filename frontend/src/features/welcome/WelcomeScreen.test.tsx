import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import WelcomeScreen from './WelcomeScreen';

describe('WelcomeScreen', () => {
  it('renders title and navigation cards', () => {
    const handleNavigate = vi.fn();
    render(<WelcomeScreen onNavigate={handleNavigate} />);
    
    expect(screen.getByText('Xin chào nhà nông,')).toBeInTheDocument();
    expect(screen.getByText('Hôm nay bạn muốn làm gì?')).toBeInTheDocument();
    
    expect(screen.getByText('Dự báo Giá Cà Phê')).toBeInTheDocument();
    expect(screen.getByText('Tư vấn Canh tác')).toBeInTheDocument();
    expect(screen.getByText('Lịch sử Dự báo')).toBeInTheDocument();
  });
});
