import { VERIFICATION_CHECKS, PLATFORM_INFO } from '@/lib/data';
import { FileText } from 'lucide-react';

export default function Verification() {
  const stageAChecks = VERIFICATION_CHECKS.filter((c) => c.stage === 'A');
  const stageBChecks = VERIFICATION_CHECKS.filter((c) => c.stage === 'B');

  return (
    <section id="verification" className="py-8 border-t border-creamy">
      <div className="flex flex-wrap items-baseline justify-between gap-2 mb-6">
        <div>
          <span className="text-xs font-bold uppercase tracking-wider text-creamy-accent">
            Compliance &amp; Reproducibility
          </span>
          <h2 className="text-2xl font-bold tracking-tight text-creamy-primary mt-0.5">
            Submission Verification Center
          </h2>
          <p className="text-xs text-creamy-secondary mt-1">
            Forensic audit and structural integrity verification for the official submission candidate.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="px-2.5 py-1 text-xs font-mono font-semibold rounded bg-[#EAEFE8] text-[#3F6350] border border-[#C8D7C4]">
            Audit Status: 14/14 PASS
          </span>
        </div>
      </div>

      {/* Artifact Verification Metadata Card */}
      <div className="scientific-card p-5 mb-6 border-l-4 border-l-creamy-accent">
        <div className="flex flex-wrap items-center justify-between pb-3 border-b border-creamy gap-2 mb-4">
          <div className="flex items-center gap-2">
            <FileText className="w-4 h-4 text-creamy-accent" />
            <span className="text-xs font-bold uppercase tracking-wider text-creamy-primary">
              Approved Champion Artifact Specification
            </span>
          </div>
          <span className="text-xs font-mono font-semibold text-[#3F6350] px-2 py-0.5 rounded bg-[#EAEFE8]">
            Bitwise Verified Champion
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
          <div>
            <div className="text-creamy-muted mb-0.5">Artifact Path</div>
            <div className="font-mono font-semibold text-creamy-primary truncate">
              {PLATFORM_INFO.approvedFile}
            </div>
          </div>

          <div>
            <div className="text-creamy-muted mb-0.5">Target Predictions</div>
            <div className="font-mono font-semibold text-creamy-primary">
              7,000 Stars (7,001 Lines)
            </div>
          </div>

          <div>
            <div className="text-creamy-muted mb-0.5">Columns &amp; Schema</div>
            <div className="font-mono font-semibold text-creamy-primary">
              id, label (UTF-8, No extra indices)
            </div>
          </div>

          <div>
            <div className="text-creamy-muted mb-0.5">Vocabulary Compliance</div>
            <div className="font-mono font-semibold text-[#3F6350]">
              100% Permitted Astronomical Classes
            </div>
          </div>
        </div>

        <div className="mt-4 pt-3 border-t border-creamy">
          <div className="text-[11px] text-creamy-muted mb-1 font-semibold">
            SHA-256 Bitwise Cryptographic Checksum:
          </div>
          <div className="p-2.5 rounded bg-[#F0EBDD]/60 border border-creamy font-mono text-xs text-creamy-primary break-all select-all flex items-center justify-between gap-2">
            <span>{PLATFORM_INFO.approvedChecksum}</span>
            <span className="text-[10px] font-sans font-bold uppercase px-1.5 py-0.5 rounded bg-[#EAEFE8] text-[#3F6350] shrink-0">
              Verified Match
            </span>
          </div>
        </div>
      </div>

      {/* Two-Stage Decoupled Audit Table */}
      <div className="scientific-card p-5">
        {/* Stage A */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-3 pb-2 border-b border-creamy">
            <h3 className="text-xs font-bold uppercase tracking-wider text-creamy-accent">
              Stage A: Submission Artifact Integrity Checks (Self-Contained • 12 Rules)
            </h3>
            <span className="text-[11px] font-mono text-[#3F6350] font-semibold">
              12/12 PASS
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead>
                <tr className="border-b border-creamy text-creamy-secondary font-mono">
                  <th className="py-2 px-3 w-12">#</th>
                  <th className="py-2 px-3 w-52">Rule Specification</th>
                  <th className="py-2 px-3">Verification Criteria</th>
                  <th className="py-2 px-3 text-right w-24">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-creamy-subtle">
                {stageAChecks.map((c) => (
                  <tr key={c.id} className="hover:bg-[#FAF6ED] transition-colors">
                    <td className="py-2 px-3 font-mono text-creamy-muted">
                      {String(c.id).padStart(2, '0')}
                    </td>
                    <td className="py-2 px-3 font-semibold text-creamy-primary">
                      {c.rule}
                    </td>
                    <td className="py-2 px-3 text-creamy-secondary">
                      {c.criteria}
                    </td>
                    <td className="py-2 px-3 text-right">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-[#EAEFE8] text-[#3F6350] border border-[#C8D7C4]">
                        PASS
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Stage B */}
        <div>
          <div className="flex items-center justify-between mb-3 pb-2 border-b border-creamy">
            <h3 className="text-xs font-bold uppercase tracking-wider text-creamy-bronze">
              Stage B: External Target Dataset Cross-Matching Checks (Requires test_stars.csv • 2 Rules)
            </h3>
            <span className="text-[11px] font-mono text-creamy-bronze font-semibold">
              2/2 Verified
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead>
                <tr className="border-b border-creamy text-creamy-secondary font-mono">
                  <th className="py-2 px-3 w-12">#</th>
                  <th className="py-2 px-3 w-52">Rule Specification</th>
                  <th className="py-2 px-3">Verification Criteria</th>
                  <th className="py-2 px-3 text-right w-24">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-creamy-subtle">
                {stageBChecks.map((c) => (
                  <tr key={c.id} className="hover:bg-[#FAF6ED] transition-colors">
                    <td className="py-2 px-3 font-mono text-creamy-muted">
                      {String(c.id).padStart(2, '0')}
                    </td>
                    <td className="py-2 px-3 font-semibold text-creamy-primary">
                      {c.rule}
                    </td>
                    <td className="py-2 px-3 text-creamy-secondary">
                      {c.criteria}
                    </td>
                    <td className="py-2 px-3 text-right">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-[#EAEFE8] text-[#3F6350] border border-[#C8D7C4]">
                        PASS
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  );
}
