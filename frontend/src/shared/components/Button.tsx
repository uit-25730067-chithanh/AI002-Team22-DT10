import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  fullWidth?: boolean;
}

const baseClasses =
  'inline-flex min-h-[48px] items-center justify-center gap-2 rounded-lg border border-transparent px-4 py-2 font-semibold no-underline transition-colors duration-150 focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-offset-2 focus-visible:outline-green-700 disabled:cursor-not-allowed disabled:opacity-60';

const variantClasses = {
  primary:
    'bg-green-700 text-white shadow-sm hover:enabled:bg-green-800 active:enabled:bg-green-900',
  secondary:
    'bg-white text-gray-900 border-gray-300 shadow-sm hover:enabled:bg-gray-50 active:enabled:bg-gray-100',
  ghost:
    'bg-transparent text-gray-700 shadow-none hover:enabled:bg-gray-100',
};

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ children, variant = 'primary', fullWidth, className = '', ...props }, ref) => {
    const classNames = [
      baseClasses,
      variantClasses[variant],
      fullWidth ? 'w-full' : '',
      className,
    ]
      .filter(Boolean)
      .join(' ');

    return (
      <button ref={ref} className={classNames} {...props}>
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';

export default Button;
