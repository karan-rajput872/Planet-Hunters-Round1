import { FEATURE_PILLARS } from '@/lib/data';
import { Check } from 'lucide-react';

export default function Features() {
  return (
    <section id="features" className="py-8 border-t border-creamy">
      <div className="flex flex-wrap items-baseline justify-between gap-2 mb-6">
        <div>
          <span className="text-xs font-bold uppercase tracking-wider text-creamy-accent">
            Domain Engineering &amp; Physics
          </span>
          <h2 className="text-2xl font-bold tracking-tight text-creamy-primary mt-0.5">
            88-Feature Astrophysical Architecture
          </h2>
          <p className="text-xs text-creamy-secondary mt-1">
            Structured feature extraction isolating photometric variations, transit geometry, and sensor pixel drift.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="px-2.5 py-1 text-xs font-mono font-semibold rounded bg-[#EAEFE8] text-[#3F6350] border border-[#C8D7C4]">
            Total Features: 88 Across 4 Pillars
          </span>
        </div>
      </div>

      {/* 4 Feature Pillars Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-6">
        {FEATURE_PILLARS.map((pillar, idx) => (
          <div
            key={idx}
            className="scientific-card p-5 flex flex-col justify-between"
            style={{ borderTop: `3px solid ${pillar.color}` }}
          >
            <div>
              <div className="flex items-center justify-between pb-3 border-b border-creamy mb-3">
                <span className="text-xs font-bold uppercase tracking-wider text-creamy-secondary">
                  Pillar {idx + 1}
                </span>
                <span className="font-mono text-sm font-bold text-creamy-primary px-2 py-0.5 rounded bg-[#F0EBDD]">
                  {pillar.count} Features
                </span>
              </div>

              <h3 className="text-sm font-bold text-creamy-primary mb-2">
                {pillar.title}
              </h3>

              <p className="text-xs text-creamy-secondary leading-relaxed mb-3">
                {pillar.description}
              </p>

              <div className="space-y-1.5 mb-4">
                <div className="text-[11px] font-semibold uppercase tracking-wider text-creamy-muted">
                  Key Indicators:
                </div>
                {pillar.keyFeatures.map((kf, kfIdx) => (
                  <div key={kfIdx} className="flex items-start gap-1.5 text-xs text-creamy-secondary">
                    <Check className="w-3.5 h-3.5 text-creamy-accent shrink-0 mt-0.5" />
                    <span className="leading-tight">{kf}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="pt-3 border-t border-creamy bg-[#FAF6ED] -mx-5 -mb-5 p-4 rounded-b-lg text-[11px] text-creamy-secondary leading-relaxed">
              <strong className="text-creamy-primary block mb-0.5 font-semibold">
                Astrophysical Rationale:
              </strong>
              {pillar.astrophysicalRationale}
            </div>
          </div>
        ))}
      </div>

      {/* Engineering Ablation Summary Card */}
      <div className="scientific-card p-5">
        <div className="flex items-center justify-between pb-3 border-b border-creamy mb-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-creamy-primary">
            Feature Pillar Ablation Impact
          </h3>
          <span className="text-xs font-mono text-creamy-muted">
            Internal Validation Impact (Macro F1)
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 text-xs">
          <div className="p-3 rounded border border-creamy bg-[#FFFDF8]">
            <div className="font-semibold text-creamy-primary mb-1">Cotrended Stats (32)</div>
            <div className="font-mono text-creamy-accent font-bold">+0.054 F1 Gain</div>
            <div className="text-[11px] text-creamy-muted mt-0.5">Removes thermal telescope baseline drift</div>
          </div>

          <div className="p-3 rounded border border-creamy bg-[#FFFDF8]">
            <div className="font-semibold text-creamy-primary mb-1">Distribution Moments (24)</div>
            <div className="font-mono text-creamy-accent font-bold">+0.041 F1 Gain</div>
            <div className="text-[11px] text-creamy-muted mt-0.5">Differentiates dips (transits) from spikes (flares)</div>
          </div>

          <div className="p-3 rounded border border-creamy bg-[#FFFDF8]">
            <div className="font-semibold text-creamy-primary mb-1">Transit Morphology (16)</div>
            <div className="font-mono text-creamy-accent font-bold">+0.062 F1 Gain</div>
            <div className="text-[11px] text-creamy-muted mt-0.5">Separates U-shaped transits from V-shaped eclipses</div>
          </div>

          <div className="p-3 rounded border border-creamy bg-[#FFFDF8]">
            <div className="font-semibold text-creamy-primary mb-1">CCD Centroid Motion (16)</div>
            <div className="font-mono text-creamy-accent font-bold">+0.038 F1 Gain</div>
            <div className="text-[11px] text-creamy-muted mt-0.5">Detects false-positive background blend binaries</div>
          </div>
        </div>
      </div>
    </section>
  );
}
