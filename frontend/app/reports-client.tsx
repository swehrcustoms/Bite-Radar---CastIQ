"use client";

import { useEffect, useMemo, useState } from "react";

import type { Report } from "./types";

function buildPreview(text: string, maxLength = 150): string {
  const normalized = text.replace(/\s+/g, " ").trim();
  if (normalized.length <= maxLength) {
    return normalized;
  }
  return `${normalized.slice(0, maxLength - 1)}…`;
}

function formatReportDate(value: string | null): string {
  if (!value) {
    return "Unknown date";
  }
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return value;
  }
  return parsed.toLocaleString();
}

export default function ReportsClient() {
  const [selectedSource, setSelectedSource] = useState<string>("All");
  const [reports, setReports] = useState<Report[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    const loadReports = async () => {
      try {
        setIsLoading(true);
        setErrorMessage(null);

        const response = await fetch("/api/reports", { cache: "no-store" });
        if (!response.ok) {
          throw new Error(`Request failed (${response.status})`);
        }

        const payload = (await response.json()) as unknown;
        if (!Array.isArray(payload)) {
          throw new Error("Invalid payload shape.");
        }

        setReports(payload as Report[]);
      } catch (error) {
        const message =
          error instanceof Error ? error.message : "Unknown error loading reports.";
        setErrorMessage(message);
      } finally {
        setIsLoading(false);
      }
    };

    void loadReports();
  }, []);

  const sources = useMemo(() => {
    const unique = new Set<string>();
    reports.forEach((report) => unique.add(report.source));
    return ["All", ...Array.from(unique).sort()];
  }, [reports]);

  const filteredReports = useMemo(() => {
    if (selectedSource === "All") {
      return reports;
    }
    return reports.filter((report) => report.source === selectedSource);
  }, [reports, selectedSource]);

  return (
    <div className="mx-auto w-full max-w-7xl p-4 md:p-8">
      <header className="mb-6 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">
            Minnesota Fishing Reports
          </h1>
          <p className="mt-2 text-slate-600">
            Unified inbox of the latest reports from tracked sources.
          </p>
        </div>

        <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
          Filter by source
          <select
            value={selectedSource}
            onChange={(event) => setSelectedSource(event.target.value)}
            className="rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm focus:border-sky-500 focus:outline-none focus:ring-2 focus:ring-sky-500/30"
          >
            {sources.map((source) => (
              <option key={source} value={source}>
                {source}
              </option>
            ))}
          </select>
        </label>
      </header>

      {isLoading ? (
        <div className="rounded-xl border border-slate-200 bg-white p-8 text-center text-slate-600">
          Loading reports...
        </div>
      ) : errorMessage ? (
        <div className="rounded-xl border border-red-300 bg-red-50 p-8 text-center text-red-700">
          Unable to load reports: {errorMessage}
        </div>
      ) : filteredReports.length === 0 ? (
        <div className="rounded-xl border border-dashed border-slate-300 bg-white p-8 text-center text-slate-600">
          No reports found for the selected source.
        </div>
      ) : (
        <section className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
          {filteredReports.map((report) => (
            <article
              key={report.id}
              className="flex h-full flex-col rounded-xl border border-slate-200 bg-white p-5 shadow-sm"
            >
              <div className="mb-3 flex items-center justify-between gap-2">
                <span className="inline-flex rounded-full bg-sky-100 px-2.5 py-1 text-xs font-semibold text-sky-800">
                  {report.source}
                </span>
                <time className="text-xs text-slate-500">
                  {formatReportDate(report.report_date)}
                </time>
              </div>

              <h2 className="mb-2 text-lg font-semibold text-slate-900">
                {report.title}
              </h2>

              <p className="mb-4 text-sm text-slate-700">
                {buildPreview(report.body)}
              </p>

              <div className="mt-auto">
                <a
                  href={report.source_url}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center rounded-md bg-slate-900 px-3 py-2 text-sm font-medium text-white hover:bg-slate-800"
                >
                  Read Full Report
                </a>
              </div>
            </article>
          ))}
        </section>
      )}
    </div>
  );
}
