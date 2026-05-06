export type Report = {
  id: number;
  source: string;
  title: string;
  body: string;
  report_date: string | null;
  source_url: string;
  scraped_at: string;
};
