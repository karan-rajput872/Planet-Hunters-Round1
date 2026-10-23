'use client';

import { useState } from 'react';
import Link from 'next/link';
import { ExternalLink, Menu, X } from 'lucide-react';
import { PLATFORM_INFO } from '@/lib/data';

interface NavbarProps {
  activeSection?: string;
}

export default function Navbar({ activeSection = 'overview' }: NavbarProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navLinks = [
    { id: 'overview', label: 'Overview', href: '#overview' },
    { id: 'taxonomy', label: 'Taxonomy', href: '#taxonomy' },
    { id: 'architecture', label: 'Architecture', href: '#architecture' },
    { id: 'features', label: 'Features', href: '#features' },
    { id: 'evaluation', label: 'Evaluation', href: '#evaluation' },
    { id: 'verification', label: 'Verification', href: '#verification' },
    { id: 'explorer', label: 'Prediction Explorer', href: '#explorer' },
    { id: 'artifacts', label: 'Documentation', href: '#artifacts' },
  ];

  return (
    <header className="sticky top-0 z-50 bg-[#FFFDF8]/90 backdrop-blur-md border-b border-creamy">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Identity */}
          <Link href="#overview" className="flex items-center gap-3 group">
            <div className="w-9 h-9 rounded-lg bg-creamy-accent text-white flex items-center justify-center font-bold text-sm shadow-sm group-hover:scale-105 transition-transform">
              PH
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-base tracking-tight text-creamy-primary">
                  PLANET HUNTERS
                </span>
                <span className="hidden sm:inline-block px-1.5 py-0.5 text-[10px] font-semibold tracking-wider uppercase rounded bg-[#EAEFE8] text-[#3F6350] border border-[#C8D7C4]">
                  Round 1 Champion
                </span>
              </div>
              <p className="text-xs text-creamy-secondary hidden sm:block">
                Scientific Intelligence Platform • Priyanshu Karan
              </p>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center gap-1">
            {navLinks.map((link) => {
              const isActive = activeSection === link.id;
              return (
                <a
                  key={link.id}
                  href={link.href}
                  className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                    isActive
                      ? 'bg-[#EAEFE8] text-creamy-accent font-semibold'
                      : 'text-creamy-secondary hover:text-creamy-primary hover:bg-[#F0EBDD]/60'
                  }`}
                >
                  {link.label}
                </a>
              );
            })}
          </nav>

          {/* External Links & Actions */}
          <div className="hidden sm:flex items-center gap-2.5">
            <a
              href={PLATFORM_INFO.liveStreamlitUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md border border-creamy bg-[#FFFDF8] hover:bg-[#F0EBDD]/50 text-creamy-secondary transition-colors"
            >
              <span>Streamlit App</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>

            <a
              href={PLATFORM_INFO.repoUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md bg-creamy-accent text-white hover:bg-creamy-accent-hover shadow-sm transition-colors"
            >
              <span>GitHub</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>

          {/* Mobile Menu Button */}
          <div className="flex lg:hidden">
            <button
              type="button"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-md text-creamy-secondary hover:text-creamy-primary hover:bg-[#F0EBDD]"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-b border-creamy bg-[#FFFDF8] px-4 pt-2 pb-4 space-y-1 shadow-lg">
          {navLinks.map((link) => (
            <a
              key={link.id}
              href={link.href}
              onClick={() => setMobileMenuOpen(false)}
              className="block px-3 py-2 rounded-md text-sm font-medium text-creamy-secondary hover:text-creamy-primary hover:bg-[#F0EBDD]"
            >
              {link.label}
            </a>
          ))}
          <div className="pt-3 border-t border-creamy flex gap-2">
            <a
              href={PLATFORM_INFO.liveStreamlitUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 text-center py-2 text-xs font-medium rounded-md border border-creamy text-creamy-secondary"
            >
              Streamlit App
            </a>
            <a
              href={PLATFORM_INFO.repoUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 text-center py-2 text-xs font-medium rounded-md bg-creamy-accent text-white"
            >
              GitHub
            </a>
          </div>
        </div>
      )}
    </header>
  );
}
