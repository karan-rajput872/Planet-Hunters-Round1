import { DOCUMENTATION_LINKS, PLATFORM_INFO } from '@/lib/data';
import { FileText, ExternalLink, Cpu } from 'lucide-react';

export default function Artifacts() {
  const engineeringSpecs = [
    { label: "Core Runtime", value: "Python 3.11.17 • Next.js 16 (App Router)" },
    { label: "ML Libraries", value: "LightGBM 4.3 • Scikit-Learn 1.4 • CatBoost 1.2" },
    { label: "Evaluation Metric", value: "8-Class Macro F1 (Stratified 5-Fold CV)" },
    { label: "Frontend Stack", value: "Next.js, TypeScript, Tailwind CSS, Recharts" },
    { label: "Seed / Random State", value: "42 (Deterministic cross-validation)" },
    { label: "Approved Checksum", value: "6A378EAE...330E (SHA-256 Verified)" },
  ];

  return (
    <section id="artifacts" className="py-8 border-t border-creamy">
      <div className="flex flex-wrap items-baseline justify-between gap-2 mb-6">
        <div>
          <span className="text-xs font-bold uppercase tracking-wider text-creamy-accent">
            Resources &amp; Specifications
          </span>
          <h2 className="text-2xl font-bold tracking-tight text-creamy-primary mt-0.5">
            Artifacts, Documentation &amp; Engineering Specs
          </h2>
          <p className="text-xs text-creamy-secondary mt-1">
            Complete technical documentation, reproducibility manifests, and pipeline governance references.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <a
            href={PLATFORM_INFO.repoUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-creamy-accent text-white text-xs font-semibold hover:bg-creamy-accent-hover transition-colors"
          >
            <span>GitHub Repository</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>
      </div>

      {/* Engineering Specs Table Card */}
      <div className="scientific-card p-5 mb-6">
        <div className="flex items-center justify-between pb-3 border-b border-creamy mb-4">
          <div className="flex items-center gap-2">
            <Cpu className="w-4 h-4 text-creamy-accent" />
            <h3 className="text-xs font-bold uppercase tracking-wider text-creamy-primary">
              Scientific Pipeline Engineering Specifications
            </h3>
          </div>
          <span className="text-xs font-mono text-creamy-muted">
            Reproducible Environment
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {engineeringSpecs.map((spec, idx) => (
            <div key={idx} className="p-3 rounded border border-creamy bg-[#FFFDF8]">
              <div className="text-[11px] font-semibold text-creamy-muted uppercase tracking-wider mb-1">
                {spec.label}
              </div>
              <div className="font-mono text-xs font-semibold text-creamy-primary truncate">
                {spec.value}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Real Documentation Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {DOCUMENTATION_LINKS.map((doc, idx) => {
          const docUrl = `${PLATFORM_INFO.repoUrl}/blob/main/${doc.path}`;

          return (
            <div
              key={idx}
              className="scientific-card p-5 flex flex-col justify-between hover:border-creamy-accent transition-colors"
            >
              <div>
                <div className="flex items-center justify-between gap-1 mb-2">
                  <span className="text-[10px] font-semibold uppercase tracking-wider text-creamy-muted">
                    {doc.category}
                  </span>
                  <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-[#F0EBDD] text-creamy-secondary">
                    {doc.badge}
                  </span>
                </div>

                <h4 className="text-sm font-bold text-creamy-primary mb-1.5 flex items-center gap-1.5">
                  <FileText className="w-4 h-4 text-creamy-accent shrink-0" />
                  <span>{doc.title}</span>
                </h4>

                <p className="text-xs text-creamy-secondary leading-relaxed mb-3">
                  {doc.description}
                </p>
              </div>

              <div className="pt-3 border-t border-creamy flex items-center justify-between text-xs">
                <span className="font-mono text-[11px] text-creamy-muted truncate">
                  {doc.path}
                </span>

                <a
                  href={docUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 text-xs font-semibold text-creamy-accent hover:underline shrink-0"
                >
                  <span>Read Doc</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
