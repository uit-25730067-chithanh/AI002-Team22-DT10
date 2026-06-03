import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  fullWidth?: boolean;
}

const baseClasses =
  'inline-flex min-h-12 items-center justify-center gap-2 rounded-lg border-2 border-coffee-800 px-4 py-2 font-semibold no-underline transition-[transform,box-shadow,background-color] duration-150 focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-offset-2 focus-visible:outline-coffee-500 disabled:cursor-not-allowed disabled:opacity-60';

const variantClasses = {
  primary:
    'bg-coffee-500 text-white shadow-hard hover:enabled:bg-coffee-700 active:enabled:translate-x-1 active:enabled:translate-y-1 active:enabled:shadow-none',
  secondary:
    'bg-white text-coffee-900 shadow-hard hover:enabled:bg-coffee-100 active:enabled:translate-x-1 active:enabled:translate-y-1 active:enabled:shadow-none',
  ghost:
    'border-transparent bg-transparent text-coffee-800 shadow-none hover:enabled:bg-coffee-100',
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
