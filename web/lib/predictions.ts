import predictionsData from '@/data/predictions.json';

export interface PredictionItem {
  id: string;
  label: string;
}

export interface PredictionFilterResult {
  items: PredictionItem[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
  countsByClass: Record<string, number>;
}

const predictions: PredictionItem[] = predictionsData as PredictionItem[];

export function getPredictionsSummary() {
  const countsByClass: Record<string, number> = {};
  for (const item of predictions) {
    countsByClass[item.label] = (countsByClass[item.label] || 0) + 1;
  }
  return {
    total: predictions.length,
    countsByClass
  };
}

export function queryPredictions(
  query: string = '',
  classFilter: string = 'all',
  page: number = 1,
  pageSize: number = 50
): PredictionFilterResult {
  const normalizedQuery = query.trim().toUpperCase();
  
  let filtered = predictions;
  
  if (classFilter && classFilter !== 'all') {
    filtered = filtered.filter(item => item.label === classFilter);
  }
  
  if (normalizedQuery) {
    filtered = filtered.filter(item => item.id.toUpperCase().includes(normalizedQuery));
  }
  
  const total = filtered.length;
  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  const currentPage = Math.min(Math.max(1, page), totalPages);
  
  const start = (currentPage - 1) * pageSize;
  const items = filtered.slice(start, start + pageSize);
  
  const countsByClass: Record<string, number> = {};
  for (const item of predictions) {
    countsByClass[item.label] = (countsByClass[item.label] || 0) + 1;
  }

  return {
    items,
    total,
    page: currentPage,
    pageSize,
    totalPages,
    countsByClass
  };
}
