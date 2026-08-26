import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
  display: "swap",
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "AI Daily News – Your Daily AI Briefing",
    template: "%s | AI Daily News",
  },
  description:
    "AI Daily News brings you the 6 most important AI stories every day. Researched, ranked, and summarised by AI – delivered to you at 8 PM.",
  keywords: [
    "AI news",
    "artificial intelligence",
    "daily AI briefing",
    "machine learning",
    "AI research",
    "OpenAI",
    "Anthropic",
    "Google AI",
    "LLM",
  ],
  authors: [{ name: "Jihad Chaalan" }],
  creator: "Jihad Chaalan",
  publisher: "AI Daily News",
  metadataBase: new URL(process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:3000"),
  openGraph: {
    title: "AI Daily News – Your Daily AI Briefing",
    description:
      "The 6 most important AI stories every day, automatically researched, ranked, and summarised by AI.",
    url: "/",
    siteName: "AI Daily News",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "AI Daily News – Your daily briefing",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "AI Daily News – Your Daily AI Briefing",
    description:
      "The 6 most important AI stories every day, automatically researched, ranked, and summarised by AI.",
    images: ["/og-image.png"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  icons: {
    icon: "/favicon.ico",
    apple: "/apple-touch-icon.png",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        <Header />
        <main className="flex-1 container mx-auto px-4 py-8">{children}</main>
        <Footer />
      </body>
    </html>
  );
}