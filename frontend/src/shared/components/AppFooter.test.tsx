import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import AppFooter from "./AppFooter";

describe("AppFooter component", () => {
  it("renders disclaimer and copyright information", () => {
    render(<AppFooter />);

    // Kiểm tra có tiêu đề Disclaimer hay không
    expect(
      screen.getByText(/TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM/i),
    ).toBeInTheDocument();

    // Kiểm tra nội dung cảnh báo có được hiển thị
    expect(
      screen.getByText(
        /Dự báo giá và gợi ý canh tác chỉ mang tính chất tham khảo học thuật/i,
      ),
    ).toBeInTheDocument();

    // Kiểm tra có thông tin nhóm thực hiện
    expect(screen.getByText(/Nhóm 22/i)).toBeInTheDocument();
  });
});
