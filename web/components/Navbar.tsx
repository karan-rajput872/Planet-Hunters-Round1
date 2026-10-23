'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { ExternalLink, Menu, X } from 'lucide-react';
import { PLATFORM_INFO } from '@/lib/data';

interface NavbarProps {
  activeSection?: string;
}

export default function Navbar({ activeSection = 'overview' }: NavbarProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [currentSection, setCurrentSection] = useState(activeSection);

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

  // Dynamic active section scroll-spy
  useEffect(() => {
    const handleScroll = () => {
      const scrollPosition = window.scrollY + 140;
      for (let i = navLinks.length - 1; i >= 0; i--) {
        const el = document.getElementById(navLinks[i].id);
        if (el && el.offsetTop <= scrollPosition) {
          setCurrentSection(navLinks[i].id);
          return;
        }
      }
      setCurrentSection('overview');
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header className="sticky top-0 z-50 bg-[#FFFDF8]/95 backdrop-blur-md border-b border-creamy shadow-xs">
      {/* LEVEL 1 — BRANDING AREA */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14 sm:h-16">
          {/* Left Brand Identity */}
          <Link
            href="#overview"
            className="flex items-center gap-3 shrink-0 group focus:outline-hidden"
            aria-label="Planet Hunters Home"
          >
            {/* Logo */}
            <div className="w-9 h-9 rounded-lg bg-creamy-accent text-white flex items-center justify-center font-bold text-sm shadow-xs shrink-0 group-hover:scale-105 transition-transform select-none">
              PH
            </div>

            {/* Brand Title & Subtitle */}
            <div className="flex flex-col justify-center min-w-0">
              <div className="flex items-center gap-2">
                <span className="font-bold text-[15px] sm:text-base tracking-tight text-creamy-primary whitespace-nowrap leading-tight">
                  PLANET HUNTERS
                </span>
                <span className="hidden sm:inline-flex items-center whitespace-nowrap px-1.5 py-0.5 text-[10px] font-semibold tracking-wider uppercase rounded bg-[#EAEFE8] text-[#3F6350] border border-[#C8D7C4] leading-normal shrink-0">
                  Round 1 Champion
                </span>
              </div>
              <p className="text-[11px] text-creamy-secondary hidden sm:block leading-tight tracking-normal whitespace-nowrap mt-0.5">
                Scientific Intelligence Platform • Priyanshu Karan
              </p>
            </div>
          </Link>

          {/* Mobile Menu Toggle Button */}
          <div className="flex lg:hidden">
            <button
              type="button"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-md text-creamy-secondary hover:text-creamy-primary hover:bg-[#F0EBDD] transition-colors"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {/* LEVEL 2 — NAVIGATION AND ACTION BUTTONS (Desktop & Large Screens) */}
      <div className="hidden lg:block border-t border-creamy-subtle bg-[#FAF7F0]/60">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between py-1.5 gap-4">
            {/* Left / Main Section — Navigation Links */}
            <nav className="flex items-center gap-1 xl:gap-2 flex-wrap min-w-0" aria-label="Main Navigation">
              {navLinks.map((link) => {
                const isActive = currentSection === link.id;
                return (
                  <a
                    key={link.id}
                    href={link.href}
                    className={`px-3 py-1.5 rounded-md text-xs font-medium whitespace-nowrap transition-colors ${
                      isActive
                        ? 'bg-[#EAEFE8] text-creamy-accent font-semibold shadow-xs'
                        : 'text-creamy-secondary hover:text-creamy-primary hover:bg-[#F0EBDD]/60'
                    }`}
                  >
                    {link.label}
                  </a>
                );
              })}
            </nav>

            {/* Right Section — Stacked Action Buttons */}
            <div className="flex flex-col gap-1 shrink-0 w-32 py-0.5">
              {/* TOP BUTTON: Streamlit App */}
              <a
                href={PLATFORM_INFO.liveStreamlitUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-between w-full px-2.5 py-0.5 text-[11px] font-medium rounded border border-creamy bg-[#FFFDF8] hover:bg-[#F0EBDD]/60 text-creamy-secondary hover:text-creamy-primary transition-colors whitespace-nowrap shadow-xs leading-normal"
                title="Open Streamlit Application"
              >
                <span>Streamlit App</span>
                <ExternalLink className="w-3 h-3 text-creamy-muted shrink-0" />
              </a>

              {/* BOTTOM BUTTON: GitHub */}
              <a
                href={PLATFORM_INFO.repoUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-between w-full px-2.5 py-0.5 text-[11px] font-medium rounded bg-creamy-accent text-white hover:bg-creamy-accent-hover transition-colors whitespace-nowrap shadow-xs leading-normal"
                title="View GitHub Repository"
              >
                <span>GitHub</span>
                <ExternalLink className="w-3 h-3 text-white/80 shrink-0" />
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-b border-creamy bg-[#FFFDF8] px-4 pt-2 pb-4 space-y-1 shadow-lg">
          {navLinks.map((link) => {
            const isActive = currentSection === link.id;
            return (
              <a
                key={link.id}
                href={link.href}
                onClick={() => setMobileMenuOpen(false)}
                className={`block px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-[#EAEFE8] text-creamy-accent font-semibold'
                    : 'text-creamy-secondary hover:text-creamy-primary hover:bg-[#F0EBDD]'
                }`}
              >
                {link.label}
              </a>
            );
          })}

          {/* Mobile Stacked Action Buttons: Streamlit App Above GitHub */}
          <div className="pt-3 border-t border-creamy flex flex-col gap-2">
            {/* TOP BUTTON: Streamlit App */}
            <a
              href={PLATFORM_INFO.liveStreamlitUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center gap-1.5 w-full py-2 text-xs font-medium rounded-md border border-creamy bg-[#FFFDF8] text-creamy-secondary hover:bg-[#F0EBDD]/50 transition-colors"
            >
              <span>Streamlit App</span>
              <ExternalLink className="w-3.5 h-3.5 text-creamy-muted" />
            </a>

            {/* BOTTOM BUTTON: GitHub */}
            <a
              href={PLATFORM_INFO.repoUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center gap-1.5 w-full py-2 text-xs font-medium rounded-md bg-creamy-accent text-white hover:bg-creamy-accent-hover shadow-xs transition-colors"
            >
              <span>GitHub</span>
              <ExternalLink className="w-3.5 h-3.5 text-white/80" />
            </a>
          </div>
        </div>
      )}
    </header>
  );
}
