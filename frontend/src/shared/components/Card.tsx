import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

const Card: React.FC<CardProps> = ({ children, className = '', ...props }) => {
  return (
    <div
      className={`rounded-xl border-2 border-coffee-800 bg-white p-4 shadow-hard ${className}`.trim()}
      {...props}
    >
      {children}
    </div>
  );
};

export default Card;
