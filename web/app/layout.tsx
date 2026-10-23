import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-sans",
  subsets: ["latin"],
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Planet Hunters — Scientific Intelligence Platform",
  description: "Exoplanet detection and astrophysical classification platform for photometric stellar light curves. Engineered by Priyanshu Karan for Hack4Hack 2026.",
  keywords: ["exoplanet", "astrophysics", "machine learning", "astronomy", "time-series", "light curves", "hack4hack"],
  authors: [{ name: "Priyanshu Karan" }],
  openGraph: {
    title: "Planet Hunters — Find New Worlds in Starlight",
    description: "Multi-class astronomical intelligence platform detecting exoplanets and stellar phenomena.",
    url: "https://planet-hunters-round1-3bvwv7d4umhsshfcvsvc8h.streamlit.app/",
    siteName: "Planet Hunters",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable}`}>
      <body className="min-h-screen bg-canvas text-creamy-primary selection:bg-creamy-accent selection:text-white">
        {children}
      </body>
    </html>
  );
}
