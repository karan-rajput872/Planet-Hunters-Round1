import { METRIC_CARDS } from '@/lib/data';
import { Info } from 'lucide-react';

export default function Metrics() {
  return (
    <section className="py-4">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-xs font-bold uppercase tracking-wider text-creamy-secondary">
          Platform Performance &amp; Evaluation Benchmarks
        </h2>
        <span className="text-[11px] text-creamy-muted flex items-center gap-1">
          <Info className="w-3.5 h-3.5" />
          <span>F1 scores reflect internal offline validation</span>
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3.5">
        {METRIC_CARDS.map((card, idx) => {
          const isPrimary = card.type === 'primary';
          const isSecondary = card.type === 'secondary';

          return (
            <div
              key={idx}
              className={`scientific-card p-4 flex flex-col justify-between ${
                isPrimary
                  ? 'border-l-4 border-l-creamy-accent'
                  : isSecondary
                  ? 'border-l-4 border-l-creamy-bronze'
                  : ''
              }`}
            >
              <div>
                <div className="flex items-center justify-between gap-1 mb-1.5">
                  <span className="text-[11px] font-semibold tracking-tight text-creamy-secondary">
                    {card.label}
                  </span>
                  {card.badge && (
                    <span
                      className={`text-[9px] font-bold uppercase px-1.5 py-0.5 rounded ${
                        isPrimary
                          ? 'bg-[#EAEFE8] text-[#3F6350]'
                          : isSecondary
                          ? 'bg-[#F0EBDD] text-creamy-bronze'
                          : 'bg-[#F0EBDD] text-creamy-muted'
                      }`}
                    >
                      {card.badge}
                    </span>
                  )}
                </div>

                <div className="font-mono text-2xl font-bold tracking-tight text-creamy-primary">
                  {card.value}
                </div>
              </div>

              <div className="mt-3 pt-2 border-t border-creamy text-[11px] text-creamy-muted leading-tight">
                {card.subtext}
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
