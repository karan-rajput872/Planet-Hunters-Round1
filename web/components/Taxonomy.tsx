'use client';

import { useState } from 'react';
import { TAXONOMY, PLATFORM_INFO } from '@/lib/data';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from 'recharts';
import { Orbit, Activity, ShieldAlert, Sparkles, Sun, Flame, Wrench, CircleDot } from 'lucide-react';

const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  planet: Orbit,
  eclipsing_binary: Activity,
  background_binary: ShieldAlert,
  starspots: Sun,
  pulsating_star: Sparkles,
  flare_star: Flame,
  instrument_glitch: Wrench,
  quiet_star: CircleDot,
};

export default function Taxonomy() {
  const [selectedClass, setSelectedClass] = useState<string | null>(null);

  const barData = TAXONOMY.map((c) => ({
    name: c.name,
    display: c.display,
    count: c.count,
    percentage: c.percentage,
    color: c.color,
  })).sort((a, b) => a.count - b.count);

  const pieData = TAXONOMY.map((c) => ({
    name: c.display,
    value: c.count,
    percentage: c.percentage,
    color: c.color,
    id: c.id,
  }));

  return (
    <section id="taxonomy" className="py-8 border-t border-creamy">
      <div className="flex flex-wrap items-baseline justify-between gap-2 mb-6">
        <div>
          <span className="text-xs font-bold uppercase tracking-wider text-creamy-accent">
            Taxonomy &amp; Class Distribution
          </span>
          <h2 className="text-2xl font-bold tracking-tight text-creamy-primary mt-0.5">
            Astronomical Classification Taxonomy
          </h2>
          <p className="text-xs text-creamy-secondary mt-1">
            Complete population breakdown across all eight stellar, planetary, and instrumental categories ({PLATFORM_INFO.testSize.toLocaleString()} Test Stars).
          </p>
        </div>

        <div className="px-3 py-1.5 rounded-lg bg-card-creamy border border-creamy text-xs font-mono text-creamy-secondary">
          Distribution Total: <strong className="text-creamy-primary">{PLATFORM_INFO.testSize.toLocaleString()}</strong> Stars
        </div>
      </div>

      {/* Two Interactive Visualizations: Horizontal Bar Chart & Donut Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-8">
        {/* Horizontal Bar Chart */}
        <div className="lg:col-span-7 scientific-card p-5">
          <div className="flex items-center justify-between pb-3 border-b border-creamy mb-4">
            <div>
              <h3 className="text-sm font-bold text-creamy-primary">
                Predicted Class Distribution
              </h3>
              <p className="text-[11px] text-creamy-muted">
                Star count per astronomical class in approved candidate
              </p>
            </div>
            <span className="text-xs font-mono text-creamy-accent font-semibold">
              8 Classes
            </span>
          </div>

          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={barData}
                layout="vertical"
                margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
              >
                <XAxis
                  type="number"
                  domain={[0, 2200]}
                  tick={{ fontSize: 11, fill: '#70736F' }}
                  axisLine={{ stroke: '#E7E0D3' }}
                  tickLine={{ stroke: '#E7E0D3' }}
                />
                <YAxis
                  dataKey="name"
                  type="category"
                  tick={{ fontSize: 11, fill: '#292D32', fontFamily: 'JetBrains Mono' }}
                  axisLine={{ stroke: '#E7E0D3' }}
                  tickLine={{ stroke: '#E7E0D3' }}
                  width={110}
                />
                <Tooltip
                  formatter={(value: unknown, name: unknown) => [
                    `${Number(value).toLocaleString()} stars`,
                    String(name),
                  ]}
                  contentStyle={{
                    backgroundColor: '#FFFDF8',
                    borderColor: '#E7E0D3',
                    borderRadius: '8px',
                    fontSize: '12px',
                    boxShadow: '0 4px 12px rgba(41, 45, 50, 0.08)',
                  }}
                />
                <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                  {barData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Donut Proportions Chart */}
        <div className="lg:col-span-5 scientific-card p-5">
          <div className="flex items-center justify-between pb-3 border-b border-creamy mb-4">
            <div>
              <h3 className="text-sm font-bold text-creamy-primary">
                Astrophysical Population Proportions
              </h3>
              <p className="text-[11px] text-creamy-muted">
                Fractional share of 7,000 blind test predictions
              </p>
            </div>
            <span className="text-xs font-mono text-creamy-accent font-semibold">
              100.0%
            </span>
          </div>

          <div className="h-72 w-full flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={95}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} stroke="#FFFDF8" strokeWidth={2} />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(value: unknown, name: unknown) => [
                    `${Number(value).toLocaleString()} stars`,
                    String(name),
                  ]}
                  contentStyle={{
                    backgroundColor: '#FFFDF8',
                    borderColor: '#E7E0D3',
                    borderRadius: '8px',
                    fontSize: '12px',
                  }}
                />
                <Legend
                  layout="horizontal"
                  verticalAlign="bottom"
                  align="center"
                  wrapperStyle={{ fontSize: '10px', paddingTop: '10px' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* 8-Class Directory & Diagnostic Markers Grid */}
      <div className="mb-4">
        <h3 className="text-sm font-bold uppercase tracking-wider text-creamy-secondary mb-3">
          Astrophysical Class Directory &amp; Diagnostic Markers
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {TAXONOMY.map((c) => {
            const Icon = iconMap[c.id] || CircleDot;
            const isSelected = selectedClass === c.id;

            return (
              <div
                key={c.id}
                onClick={() => setSelectedClass(isSelected ? null : c.id)}
                className={`scientific-card p-4 flex flex-col justify-between cursor-pointer transition-all ${
                  isSelected ? 'ring-2 ring-creamy-accent shadow-md' : ''
                }`}
                style={{ borderTop: `3px solid ${c.color}` }}
              >
                <div>
                  <div className="flex items-center justify-between gap-1 mb-2">
                    <span className="flex items-center gap-1.5 font-mono text-xs font-bold" style={{ color: c.color }}>
                      <Icon className="w-3.5 h-3.5" />
                      <span>{c.name}</span>
                    </span>
                    <span className="text-[11px] font-mono px-1.5 py-0.5 rounded bg-[#F0EBDD] text-creamy-secondary font-semibold">
                      {c.percentage.toFixed(1)}%
                    </span>
                  </div>

                  <h4 className="text-sm font-semibold text-creamy-primary mb-1.5">
                    {c.display}
                  </h4>

                  <p className="text-xs text-creamy-secondary leading-relaxed mb-3">
                    {c.description}
                  </p>
                </div>

                <div className="pt-2 border-t border-creamy text-[11px]">
                  <div className="text-creamy-secondary leading-tight">
                    <strong style={{ color: c.color }}>Key Marker:</strong> {c.diagnosticMarker}
                  </div>
                  <div className="mt-2 flex items-center justify-between text-[10px] font-mono text-creamy-muted">
                    <span>Count: {c.count.toLocaleString()}</span>
                    <span>OOF F1: {c.f1Score.toFixed(3)}</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
