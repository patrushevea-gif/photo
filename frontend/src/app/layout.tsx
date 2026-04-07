import type { ReactNode } from 'react';

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ru">
      <body style={{ margin: 0, fontFamily: 'Arial, sans-serif', padding: 20 }}>{children}</body>
    </html>
  );
}
