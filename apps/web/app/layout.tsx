import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CoWorker AI — Buxgalter yordamchisi",
  description:
    "O'zbekiston KO'B uchun AI hamkasb: soliq muddatlari va hujjatlar, manba bilan.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="uz">
      <body>{children}</body>
    </html>
  );
}
