const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface SourceRef {
  id: string;
  source_url: string;
  verified: string;
}

export interface AskResponse {
  answer: string;
  sources: SourceRef[];
  grounded: boolean;
  mode?: string;
}

export interface GenerateResponse {
  document: string;
  template: string | null;
  source?: SourceRef;
  grounded: boolean;
  mode?: string;
}

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_URL}/api/v1${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    throw new Error(`API xatosi (${res.status}). Server ishlab turibdimi?`);
  }
  return res.json() as Promise<T>;
}

export interface AssetCard {
  id: string;
  title: string;
  type: string;
  role: string;
  department: string;
  summary: string;
  status: string;
  confidence: number;
  path: string;
}

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${API_URL}/api/v1${path}`);
  if (!res.ok) throw new Error(`API xatosi (${res.status}).`);
  return res.json() as Promise<T>;
}

export const ask = (question: string) =>
  post<AskResponse>("/ask", { question });

export const generate = (instruction: string) =>
  post<GenerateResponse>("/generate", { instruction });

export const listAssets = () => get<AssetCard[]>("/assets");
