import { ENSEMBLE_MODELS, PIPELINE_STEPS } from '@/lib/data';
import { ArrowRight, GitMerge, CheckCircle2, Cpu } from 'lucide-react';

export default function Architecture() {
  return (
    <section id="architecture" className="py-8 border-t border-creamy">
      <div className="flex flex-wrap items-baseline justify-between gap-2 mb-6">
        <div>
          <span className="text-xs font-bold uppercase tracking-wider text-creamy-accent">
            System Design &amp; Model Diversity
          </span>
          <h2 className="text-2xl font-bold tracking-tight text-creamy-primary mt-0.5">
            Tri-Model Diversity Ensemble Architecture
          </h2>
          <p className="text-xs text-creamy-secondary mt-1">
            Weighted probabilistic voting combining three distinct gradient boosted decision tree implementations.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="px-2.5 py-1 text-xs font-mono font-semibold rounded bg-[#EAEFE8] text-[#3F6350] border border-[#C8D7C4]">
            Ensemble: 50% LGBM • 40% HGB • 10% CatBoost
          </span>
        </div>
      </div>

      {/* 3 Ensemble Member Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-8">
        {ENSEMBLE_MODELS.map((model, idx) => (
          <div
            key={idx}
            className="scientific-card p-5 flex flex-col justify-between"
            style={{ borderTop: `4px solid ${model.color}` }}
          >
            <div>
              <div className="flex items-center justify-between pb-3 border-b border-creamy mb-3">
                <div className="flex items-center gap-2">
                  <Cpu className="w-4 h-4" style={{ color: model.color }} />
                  <span className="text-xs font-bold uppercase tracking-wider text-creamy-secondary">
                    {model.role}
                  </span>
                </div>
                <span className="font-mono text-base font-bold text-creamy-primary px-2 py-0.5 rounded bg-[#F0EBDD]">
                  {model.weight}
                </span>
              </div>

              <h3 className="text-base font-bold text-creamy-primary mb-2">
                {model.name}
              </h3>

              <p className="text-xs text-creamy-secondary leading-relaxed">
                {model.details}
              </p>
            </div>

            <div className="mt-4 pt-3 border-t border-creamy flex items-center justify-between text-[11px] font-mono text-creamy-muted">
              <span>5-Fold Stratified CV</span>
              <span className="text-creamy-accent font-semibold">Calibrated Softmax</span>
            </div>
          </div>
        ))}
      </div>

      {/* Visual Sequence Pipeline (5 Stages) */}
      <div className="scientific-card p-6">
        <div className="flex items-center justify-between pb-4 border-b border-creamy mb-6">
          <div className="flex items-center gap-2">
            <GitMerge className="w-4 h-4 text-creamy-accent" />
            <h3 className="text-sm font-bold uppercase tracking-wider text-creamy-primary">
              End-to-End Scientific Inference Pipeline
            </h3>
          </div>
          <span className="text-xs font-mono text-creamy-muted">
            18,000 Train → 88 Features → 7,000 Predictions
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-4 relative">
          {PIPELINE_STEPS.map((step, idx) => (
            <div
              key={idx}
              className="p-3.5 rounded-lg border border-creamy bg-[#FFFDF8] flex flex-col justify-between relative"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="w-6 h-6 rounded-full bg-[#EAEFE8] text-creamy-accent flex items-center justify-center font-mono text-xs font-bold">
                    {step.step}
                  </span>
                  <span className="text-[10px] uppercase font-semibold text-creamy-muted">
                    Stage {idx + 1}
                  </span>
                </div>

                <h4 className="text-xs font-bold text-creamy-primary mb-1.5">
                  {step.title}
                </h4>

                <p className="text-[11px] text-creamy-secondary leading-relaxed">
                  {step.desc}
                </p>
              </div>

              {idx < PIPELINE_STEPS.length - 1 && (
                <div className="hidden md:block absolute -right-2.5 top-1/2 -translate-y-1/2 z-10 text-creamy-muted">
                  <ArrowRight className="w-4 h-4" />
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="mt-5 pt-3 border-t border-creamy flex flex-wrap items-center justify-between text-xs text-creamy-muted gap-2">
          <span className="flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5 text-[#3F6350]" />
            <span>Deterministic Seed: 42 • Fully Reproducible Inference</span>
          </span>
          <span className="font-mono text-[11px] text-creamy-secondary">
            Output: submissions/submission_FINAL.csv (Verified SHA-256)
          </span>
        </div>
      </div>
    </section>
  );
}
