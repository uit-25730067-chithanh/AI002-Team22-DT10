import React from 'react';

const AppFooter: React.FC = () => {
  return (
    <footer className="mt-auto border-t-3 border-coffee-800 bg-white py-6">
      <div className="mx-auto max-w-6xl px-4 text-center">
        <p className="text-sm font-extrabold text-coffee-800 flex items-center justify-center gap-1">
          ⚠️ TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM (DISCLAIMER)
        </p>
        <p className="mt-2 text-xs font-semibold leading-relaxed text-coffee-700 max-w-3xl mx-auto italic">
          Dự báo giá và gợi ý canh tác chỉ mang tính chất tham khảo học thuật phục vụ Đồ án môn AI002 (DT10), 
          không thay thế cho bất kỳ lời khuyên tài chính thương mại hay tư vấn chuyên môn nông nghiệp thực tế nào. 
          Người nông dân nên đối chiếu với giá đại lý thu mua địa phương trước khi đưa ra quyết định.
        </p>
        <p className="mt-4 text-xs font-bold text-coffee-500">
          © 2026 - Nhóm 22 | Đồ án AI002 - Hệ thống Dự báo Canh tác & Giá Cà phê
        </p>
      </div>
    </footer>
  );
};

export default AppFooter;
