export interface Transaction {
  id: number;
  description: string;
  amount: number;
  date: string;
  category: string;
  type: string;
}

export type ReportItem = { category: string; total: number; percentage?: string };