import Navbar from '@/components/Navbar';
import Hero from '@/components/Hero';
import Metrics from '@/components/Metrics';
import Taxonomy from '@/components/Taxonomy';
import Architecture from '@/components/Architecture';
import Features from '@/components/Features';
import Evaluation from '@/components/Evaluation';
import Verification from '@/components/Verification';
import Explorer from '@/components/Explorer';
import Artifacts from '@/components/Artifacts';
import Footer from '@/components/Footer';

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />

      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full space-y-4">
        <Hero />
        <Metrics />
        <Taxonomy />
        <Architecture />
        <Features />
        <Evaluation />
        <Verification />
        <Explorer />
        <Artifacts />
      </main>

      <Footer />
    </div>
  );
}
