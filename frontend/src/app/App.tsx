import React, { useState, useEffect } from 'react';
import AppHeader from '../shared/components/AppHeader';
import AppFooter from '../shared/components/AppFooter';
import WelcomeScreen from '../features/welcome/WelcomeScreen';

import PriceAdvisoryScreen from '../features/price-advisory/PriceAdvisoryScreen';

import FarmingAdvisoryScreen from '../features/farming-advisory/FarmingAdvisoryScreen';

import HistoryScreen from '../features/history/HistoryScreen';

const App: React.FC = () => {
  const [currentRoute, setCurrentRoute] = useState<string>('welcome');

  useEffect(() => {
    const handleHashChange = () => {
      const hash = window.location.hash.replace('#', '') || 'welcome';
      setCurrentRoute(hash);
    };

    window.addEventListener('hashchange', handleHashChange);
    handleHashChange();

    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  const navigate = (route: string) => {
    window.location.hash = route;
  };

  return (
    <div className="flex min-h-dvh flex-col">
      <AppHeader currentRoute={currentRoute} onNavigate={navigate} />
      <main className="flex-1 mx-auto w-full max-w-6xl px-4">
        {currentRoute === 'welcome' && <WelcomeScreen onNavigate={navigate} />}
        {currentRoute === 'price' && <PriceAdvisoryScreen />}
        {currentRoute === 'farming' && <FarmingAdvisoryScreen />}
        {currentRoute === 'history' && <HistoryScreen />}
      </main>
      <AppFooter />
    </div>
  );
};

export default App;
