import React from "react";
import { TrendingUp, Sprout, Clock } from "lucide-react";
import Card from "../../shared/components/Card";

interface WelcomeScreenProps {
  onNavigate: (route: string) => void;
}

const WelcomeScreen: React.FC<WelcomeScreenProps> = ({ onNavigate }) => {
  return (
    <div className="flex flex-col gap-8 py-8">
      <header>
        <h2 className="mb-2 text-2xl font-extrabold text-coffee-900">Xin chào nhà nông,</h2>
        <p className="text-coffee-700">Hôm nay bạn muốn làm gì?</p>
      </header>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
        <button
          className="w-full cursor-pointer border-0 bg-transparent p-0 text-left transition-transform duration-150 hover:-translate-y-1 focus-visible:rounded-xl focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-offset-4 focus-visible:outline-coffee-500"
          onClick={() => onNavigate("price")}
        >
          <Card className="flex h-full flex-col gap-4 active:translate-x-1 active:translate-y-1 active:shadow-none">
            <div className="flex h-16 w-16 items-center justify-center rounded-lg border-2 border-coffee-800 bg-coffee-100 text-coffee-700">
              <TrendingUp size={32} />
            </div>
            <h3 className="text-xl font-bold">Dự báo Giá Cà Phê</h3>
            <p className="text-sm leading-6 text-coffee-700">Xem dự báo giá cà phê trong các tháng tới và mức độ tin cậy.</p>
          </Card>
        </button>

        <button
          className="w-full cursor-pointer border-0 bg-transparent p-0 text-left transition-transform duration-150 hover:-translate-y-1 focus-visible:rounded-xl focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-offset-4 focus-visible:outline-coffee-500"
          onClick={() => onNavigate("farming")}
        >
          <Card className="flex h-full flex-col gap-4 active:translate-x-1 active:translate-y-1 active:shadow-none">
            <div className="flex h-16 w-16 items-center justify-center rounded-lg border-2 border-coffee-800 bg-green-100 text-leaf-600">
              <Sprout size={32} />
            </div>
            <h3 className="text-xl font-bold">Tư vấn Canh tác</h3>
            <p className="text-sm leading-6 text-coffee-700">Nhận lời khuyên chăm sóc vườn dựa trên thời tiết và loại đất.</p>
          </Card>
        </button>

        <button
          className="w-full cursor-pointer border-0 bg-transparent p-0 text-left transition-transform duration-150 hover:-translate-y-1 focus-visible:rounded-xl focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-offset-4 focus-visible:outline-coffee-500"
          onClick={() => onNavigate("history")}
        >
          <Card className="flex h-full flex-col gap-4 active:translate-x-1 active:translate-y-1 active:shadow-none">
            <div className="flex h-16 w-16 items-center justify-center rounded-lg border-2 border-coffee-800 bg-coffee-200 text-coffee-600">
              <Clock size={32} />
            </div>
            <h3 className="text-xl font-bold">Lịch sử Dự báo</h3>
            <p className="text-sm leading-6 text-coffee-700">Xem lại các dự báo và lời khuyên bạn đã lưu trước đó.</p>
          </Card>
        </button>
      </div>
    </div>
  );
};

export default WelcomeScreen;
