import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App', () => {
  it('renders welcome screen by default', () => {
    render(<App />);
    expect(screen.getByText('Xin chào nhà nông,')).toBeInTheDocument();
  });

  it('renders persistent AppFooter with disclaimer text', () => {
    render(<App />);
    expect(screen.getByText(/TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM/i)).toBeInTheDocument();
    expect(screen.getByText(/Dự báo giá và gợi ý canh tác chỉ mang tính chất tham khảo học thuật/i)).toBeInTheDocument();
  });
});
