import { PLATFORM_INFO } from '@/lib/data';
import { Telescope, ArrowRight, ShieldCheck, FileCheck, Layers, GitBranch } from 'lucide-react';

export default function Hero() {
  return (
    <section id="overview" className="pt-8 pb-10">
      {/* Top Banner / Badges */}
      <div className="flex flex-wrap items-center gap-2 mb-4">
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-semibold bg-[#EAEFE8] text-[#3F6350] border border-[#C8D7C4]">
          <Telescope className="w-3.5 h-3.5" />
          <span>{PLATFORM_INFO.competition}</span>
        </span>

        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium bg-[#F0EBDD] text-creamy-secondary border border-creamy">
          <span>Machine Learning • Astrophysical Time-Series</span>
        </span>

        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-mono font-medium bg-[#FFFDF8] text-creamy-secondary border border-creamy">
          <GitBranch className="w-3 h-3 text-creamy-accent" />
          <span>Branch: main (Approved Phase 5 Champion)</span>
        </span>
      </div>

      {/* Main Title & Problem Framing */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
        <div className="lg:col-span-7 flex flex-col justify-between">
          <div>
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight text-creamy-primary leading-tight">
              {PLATFORM_INFO.title}
            </h1>
            <p className="text-lg sm:text-xl font-medium text-creamy-accent mt-1 tracking-tight">
              {PLATFORM_INFO.subtitle}
            </p>
            <p className="text-xs font-semibold uppercase tracking-wider text-creamy-muted mt-2">
              Engineering Architecture by {PLATFORM_INFO.author}
            </p>

            <p className="mt-4 text-sm sm:text-base text-creamy-secondary leading-relaxed max-w-2xl">
              {PLATFORM_INFO.problemStatement}
            </p>
          </div>

          {/* Action CTAs */}
          <div className="mt-6 flex flex-wrap gap-3">
            <a
              href="#explorer"
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg bg-creamy-accent text-white text-xs sm:text-sm font-semibold hover:bg-creamy-accent-hover shadow-sm transition-colors"
            >
              <span>Explore 7,000 Predictions</span>
              <ArrowRight className="w-4 h-4" />
            </a>

            <a
              href="#verification"
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg border border-creamy bg-card-creamy text-creamy-primary text-xs sm:text-sm font-medium hover:bg-[#F0EBDD]/60 transition-colors"
            >
              <ShieldCheck className="w-4 h-4 text-creamy-accent" />
              <span>Submission Verification</span>
            </a>

            <a
              href="#architecture"
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg border border-creamy bg-card-creamy text-creamy-primary text-xs sm:text-sm font-medium hover:bg-[#F0EBDD]/60 transition-colors"
            >
              <Layers className="w-4 h-4 text-creamy-bronze" />
              <span>Model Pipeline</span>
            </a>
          </div>
        </div>

        {/* Problem Formulation & Diagnostic Highlight Card */}
        <div className="lg:col-span-5">
          <div className="scientific-card p-6 h-full flex flex-col justify-between border-t-4 border-t-creamy-accent">
            <div>
              <div className="flex items-center justify-between pb-3 border-b border-creamy mb-3">
                <span className="text-xs font-bold uppercase tracking-wider text-creamy-accent">
                  Problem Formulation &amp; Physics
                </span>
                <span className="text-[11px] font-mono text-creamy-muted">
                  8-Class Taxonomy
                </span>
              </div>

              <div className="space-y-3 text-xs sm:text-sm text-creamy-secondary leading-relaxed">
                <p>
                  <strong className="text-creamy-primary font-semibold">The Detection Challenge:</strong> Space telescope light curves capture billions of photons across 27-day observation sectors. Identifying true transits requires separating minute planetary dips (~0.1% depth) from background blends, stellar variability, and orbital camera systematics.
                </p>
                <p>
                  <strong className="text-creamy-primary font-semibold">Our Scientific Solution:</strong> A tri-model diversity ensemble combining LightGBM (50%), HistGradientBoosting (40%), and CatBoost (10%) trained on 88 engineered features with common-mode cotrending and centroid pixel displacement tracking.
                </p>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-creamy flex items-center justify-between text-xs font-mono text-creamy-secondary">
              <span className="flex items-center gap-1.5">
                <FileCheck className="w-4 h-4 text-[#3F6350]" />
                <span>SHA-256 Verified Artifact</span>
              </span>
              <span className="text-creamy-accent font-semibold">14/14 Checks</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
