export function formatDate(isoString: string): string {
  const d = new Date(isoString);
  return d.toLocaleDateString('vi-VN', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

export function formatPrice(vnd: number): string {
  return `${vnd.toLocaleString('vi-VN')} VND/kg`;
}
