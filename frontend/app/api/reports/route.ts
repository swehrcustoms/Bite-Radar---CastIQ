import { NextResponse } from "next/server";

const DEFAULT_BACKEND_URL = "http://127.0.0.1:8000";

export async function GET() {
  const backendUrl = process.env.BACKEND_API_URL ?? DEFAULT_BACKEND_URL;
  const url = `${backendUrl}/api/reports`;

  try {
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) {
      return NextResponse.json(
        { error: `Backend request failed: ${response.status}` },
        { status: 502 },
      );
    }

    const reports = await response.json();
    return NextResponse.json(reports);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json(
      { error: `Could not reach backend API at ${backendUrl}. ${message}` },
      { status: 502 },
    );
  }
}
