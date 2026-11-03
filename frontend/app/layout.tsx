export const metadata = {
  title: "WebBuilder",
  description: "Bouw je website door gewoon te typen wat je wilt.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="nl">
      <body>{children}</body>
    </html>
  );
}
