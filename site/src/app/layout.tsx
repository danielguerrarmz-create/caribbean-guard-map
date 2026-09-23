import type { Metadata } from "next";
import { Poppins } from "next/font/google";
import Footer from "@/components/layout/Footer";
import Header from "@/components/layout/Header";
import "./globals.css";

const poppins = Poppins({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  variable: "--font-poppins",
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "Caribbean Guard",
    template: "%s — Caribbean Guard",
  },
  description:
    "Caribbean Guard es una organización sin fines de lucro que salva vidas en el Caribe Sur de Costa Rica a través de guardavidas, natación, freediving y educación en seguridad acuática.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className={poppins.variable}>
      <body className="flex min-h-screen flex-col">
        <Header />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
