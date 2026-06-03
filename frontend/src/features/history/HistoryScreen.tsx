import React, { useState, useEffect } from 'react';
import HistoryCard from './components/HistoryCard';
import Button from '../../shared/components/Button';
import { getResults, deleteResult, clearResults, SavedResult } from '../../shared/storage/saved-results-repository';

const HistoryScreen: React.FC = () => {
  const [results, setResults] = useState<SavedResult[]>([]);

  useEffect(() => {
    setResults(getResults());
  }, []);

  const handleDelete = (id: string) => {
    deleteResult(id);
    setResults(getResults());
  };

  const handleClear = () => {
    if (window.confirm('Bạn có chắc chắn muốn xóa tất cả lịch sử không?')) {
      clearResults();
      setResults([]);
    }
  };

  if (results.length === 0) {
    return (
      <div className="px-4 py-16 text-center">
        <h2 className="mb-4 text-2xl font-extrabold text-coffee-900">Lịch sử trống</h2>
        <p className="mb-8 text-coffee-700">
          Bạn chưa lưu kết quả dự báo nào. Hãy thực hiện dự báo và nhấn "Lưu kết quả này".
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-8 py-8">
      <header className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-extrabold text-coffee-900">Lịch Sử Đã Lưu</h2>
          <p className="mt-2 text-coffee-700">Xem lại các kết quả dự báo bạn đã lưu (tối đa 20 kết quả mới nhất).</p>
        </div>
        <Button variant="secondary" onClick={handleClear}>Xóa tất cả</Button>
      </header>

      <div className="flex flex-col gap-4">
        {results.map(r => (
          <HistoryCard key={r.id} result={r} onDelete={handleDelete} />
        ))}
      </div>
    </div>
  );
};

export default HistoryScreen;
