import React from 'react';
import { Coffee, ArrowLeft } from 'lucide-react';

interface AppHeaderProps {
  currentRoute: string;
  onNavigate: (route: string) => void;
}

const AppHeader: React.FC<AppHeaderProps> = ({ currentRoute, onNavigate }) => {
  return (
    <header className="sticky top-0 z-50 border-b-2 border-coffee-800 bg-white shadow-[0_4px_0_rgba(47,32,24,0.12)]">
      <div className="mx-auto flex max-w-6xl items-center justify-between p-4">
        <div className="flex items-center gap-4">
          {currentRoute !== 'welcome' && (
            <button 
              onClick={() => onNavigate('welcome')}
              className="flex h-10 w-10 cursor-pointer items-center justify-center rounded-lg border-2 border-coffee-800 bg-coffee-100 transition-[transform,background-color] duration-150 hover:bg-white active:translate-x-0.5 active:translate-y-0.5 focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-offset-2 focus-visible:outline-coffee-500"
              aria-label="Quay lại màn hình chính"
            >
              <ArrowLeft size={24} />
            </button>
          )}
          <div className="flex items-center gap-2">
            <Coffee className="text-coffee-500" size={28} />
            <h1 className="m-0 text-xl font-bold">AI Trợ Lý Cà Phê</h1>
          </div>
        </div>
      </div>
    </header>
  );
};

export default AppHeader;
