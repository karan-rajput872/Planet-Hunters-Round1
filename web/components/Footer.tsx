import { PLATFORM_INFO } from '@/lib/data';
import { ExternalLink, ShieldCheck } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="mt-16 border-t border-creamy bg-[#FFFDF8]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand & Purpose */}
          <div className="md:col-span-2 space-y-3">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded bg-creamy-accent text-white flex items-center justify-center font-bold text-xs">
                PH
              </div>
              <span className="font-bold text-sm tracking-tight text-creamy-primary">
                PLANET HUNTERS — SCIENTIFIC INTELLIGENCE
              </span>
            </div>

            <p className="text-xs text-creamy-secondary leading-relaxed max-w-md">
              A high-precision machine learning and astronomical intelligence platform distinguishing exoplanetary transit signatures from astronomical variability and instrumental systematics.
            </p>

            <div className="text-[11px] font-mono text-creamy-muted">
              Artifact: submissions/submission_FINAL.csv • SHA-256 Verified
            </div>
          </div>

          {/* Quick Links */}
          <div className="space-y-2">
            <h4 className="text-xs font-bold uppercase tracking-wider text-creamy-primary">
              Scientific Modules
            </h4>
            <ul className="space-y-1.5 text-xs text-creamy-secondary">
              <li><a href="#overview" className="hover:text-creamy-primary transition-colors">Project Overview</a></li>
              <li><a href="#taxonomy" className="hover:text-creamy-primary transition-colors">8-Class Taxonomy</a></li>
              <li><a href="#architecture" className="hover:text-creamy-primary transition-colors">Tri-Model Ensemble</a></li>
              <li><a href="#features" className="hover:text-creamy-primary transition-colors">88 Feature Pillars</a></li>
              <li><a href="#verification" className="hover:text-creamy-primary transition-colors">Verification Center</a></li>
              <li><a href="#explorer" className="hover:text-creamy-primary transition-colors">Prediction Explorer</a></li>
            </ul>
          </div>

          {/* Governance & Attribution */}
          <div className="space-y-2">
            <h4 className="text-xs font-bold uppercase tracking-wider text-creamy-primary">
              Project Governance
            </h4>
            <ul className="space-y-1.5 text-xs text-creamy-secondary">
              <li>Author: <strong>{PLATFORM_INFO.author}</strong></li>
              <li>Competition: {PLATFORM_INFO.competition}</li>
              <li>Runtime: Next.js + Python 3.11</li>
              <li>
                <a
                  href={PLATFORM_INFO.liveStreamlitUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 text-creamy-accent hover:underline"
                >
                  <span>Live Streamlit App</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </li>
              <li>
                <a
                  href={PLATFORM_INFO.repoUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 text-creamy-accent hover:underline"
                >
                  <span>GitHub Repository</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-6 border-t border-creamy flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-creamy-muted">
          <div>
            Planet Hunters • Find New Worlds in Starlight • ML Challenge Hack4Hack 2026 (Round 1)
          </div>
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1">
              <ShieldCheck className="w-3.5 h-3.5 text-[#3F6350]" />
              <span>Deterministic &amp; Audited</span>
            </span>
            <span>•</span>
            <span>Vercel-Ready Frontend</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
