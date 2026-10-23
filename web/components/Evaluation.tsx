import { BENCHMARK_PROGRESSION, TAXONOMY, PLATFORM_INFO } from '@/lib/data';
import { Award, ShieldCheck } from 'lucide-react';

export default function Evaluation() {
  return (
    <section id="evaluation" className="py-8 border-t border-creamy">
      <div className="flex flex-wrap items-baseline justify-between gap-2 mb-6">
        <div>
          <span className="text-xs font-bold uppercase tracking-wider text-creamy-accent">
            Validation &amp; Diagnostics
          </span>
          <h2 className="text-2xl font-bold tracking-tight text-creamy-primary mt-0.5">
            Model Evaluation &amp; Error Analysis
          </h2>
          <p className="text-xs text-creamy-secondary mt-1">
            Empirical benchmark progression across iterative modeling phases and per-class performance metrics.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="px-2.5 py-1 text-xs font-mono font-semibold rounded bg-[#EAEFE8] text-[#3F6350] border border-[#C8D7C4]">
            Champion OOF Macro F1: {PLATFORM_INFO.oofF1}
          </span>
        </div>
      </div>

      {/* Benchmark Progression (Phases 1 through 5) */}
      <div className="scientific-card p-6 mb-8">
        <div className="flex items-center justify-between pb-3 border-b border-creamy mb-4">
          <div>
            <h3 className="text-sm font-bold text-creamy-primary">
              Multi-Phase Benchmark Progression
            </h3>
            <p className="text-[11px] text-creamy-muted">
              Macro F1 improvement across development milestones (18,000-star cross-validation)
            </p>
          </div>
          <span className="text-xs font-mono font-bold text-creamy-accent">
            +0.2241 Total F1 Lift
          </span>
        </div>

        <div className="space-y-3">
          {BENCHMARK_PROGRESSION.map((step, idx) => (
            <div
              key={idx}
              className={`p-3.5 rounded-lg border transition-all ${
                step.isChampion
                  ? 'border-creamy-accent bg-[#EAEFE8]/50 ring-1 ring-creamy-accent'
                  : 'border-creamy bg-[#FFFDF8]'
              }`}
            >
              <div className="flex flex-wrap items-center justify-between gap-2 mb-1.5">
                <div className="flex items-center gap-2">
                  <span
                    className={`font-mono text-xs font-bold px-2 py-0.5 rounded ${
                      step.isChampion
                        ? 'bg-creamy-accent text-white'
                        : 'bg-[#F0EBDD] text-creamy-secondary'
                    }`}
                  >
                    {step.phase}
                  </span>
                  <span className="font-semibold text-xs sm:text-sm text-creamy-primary">
                    {step.name}
                  </span>
                  {step.isChampion && (
                    <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-bold bg-[#3F6350] text-white">
                      <Award className="w-3 h-3" />
                      Approved Champion
                    </span>
                  )}
                </div>

                <div className="flex items-center gap-3">
                  <span className="font-mono text-xs text-creamy-muted">
                    {step.gain}
                  </span>
                  <span className="font-mono text-sm sm:text-base font-bold text-creamy-primary">
                    {step.macroF1.toFixed(4)}
                  </span>
                </div>
              </div>

              <p className="text-xs text-creamy-secondary leading-relaxed">
                {step.description}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Per-Class F1 Performance Table & Error Patterns */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Table */}
        <div className="lg:col-span-7 scientific-card p-5">
          <div className="flex items-center justify-between pb-3 border-b border-creamy mb-4">
            <h3 className="text-sm font-bold text-creamy-primary">
              Per-Class Out-Of-Fold F1 Scores
            </h3>
            <span className="text-xs font-mono text-creamy-muted">
              Macro Average: {PLATFORM_INFO.oofF1}
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead>
                <tr className="border-b border-creamy text-creamy-secondary font-mono">
                  <th className="py-2 px-3">Class</th>
                  <th className="py-2 px-3">Type</th>
                  <th className="py-2 px-3 text-right">OOF F1</th>
                  <th className="py-2 px-3 text-right">Test Count</th>
                  <th className="py-2 px-3 text-right">Share</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-creamy-subtle">
                {TAXONOMY.map((c) => (
                  <tr key={c.id} className="hover:bg-[#FAF6ED] transition-colors">
                    <td className="py-2.5 px-3 font-mono font-semibold" style={{ color: c.color }}>
                      {c.name}
                    </td>
                    <td className="py-2.5 px-3 text-creamy-primary font-medium">
                      {c.display}
                    </td>
                    <td className="py-2.5 px-3 font-mono font-bold text-right text-creamy-primary">
                      {c.f1Score.toFixed(3)}
                    </td>
                    <td className="py-2.5 px-3 font-mono text-right text-creamy-secondary">
                      {c.count.toLocaleString()}
                    </td>
                    <td className="py-2.5 px-3 font-mono text-right text-creamy-muted">
                      {c.percentage.toFixed(1)}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Confusion Diagnostics & Research Findings */}
        <div className="lg:col-span-5 space-y-4">
          <div className="scientific-card p-5">
            <h3 className="text-xs font-bold uppercase tracking-wider text-creamy-primary pb-2 border-b border-creamy mb-3">
              Primary Confusion Patterns
            </h3>

            <div className="space-y-3 text-xs text-creamy-secondary leading-relaxed">
              <div className="p-2.5 rounded border border-creamy bg-[#FFFDF8]">
                <strong className="text-creamy-primary block mb-0.5">
                  1. Planet vs. Background Binary:
                </strong>
                The most challenging astrophysical boundary. Without centroid pixel tracking, background blends mimic exoplanetary transit depths. 16 centroid features resolved 74% of these confusions.
              </div>

              <div className="p-2.5 rounded border border-creamy bg-[#FFFDF8]">
                <strong className="text-creamy-primary block mb-0.5">
                  2. Starspots vs. Pulsating Stars:
                </strong>
                Both produce periodic flux modulation. Fourier frequency harmonics and autocorrelation decay times cleanly separate sinusoidal rotational modulation from stellar multi-mode pulsations.
              </div>

              <div className="p-2.5 rounded border border-creamy bg-[#FFFDF8]">
                <strong className="text-creamy-primary block mb-0.5">
                  3. Quiet Stars vs. Minor Instrumental Glitches:
                </strong>
                Photon shot noise occasionally resembles single-cadence glitches. 3-sigma outlier clipping and detector-channel holdout validation prevented over-predicting false glitches.
              </div>
            </div>
          </div>

          {/* Research Note on Experimental Phases */}
          <div className="scientific-card p-4 bg-[#F0EBDD]/50 border-creamy">
            <div className="flex items-center gap-1.5 text-xs font-bold text-creamy-bronze mb-1">
              <ShieldCheck className="w-4 h-4 text-creamy-bronze" />
              <span>Experimental Integrity Note (Phases 6–8)</span>
            </div>
            <p className="text-[11px] text-creamy-secondary leading-relaxed">
              Subsequent experimental phases (6, 7, and 8) tested threshold tuning, deep neural embeddings, and pseudo-labeling. Rigorous detector-channel holdout evaluation proved these techniques introduced cross-fold variance (+0.003 in-fold, -0.015 holdout). In strict accordance with scientific integrity, <strong>Phase 5 was locked as the approved champion</strong>.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
