const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || "dev-key";

const authHeaders = (): Record<string, string> => ({ "X-API-Key": API_KEY });

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
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(body),
  });
  if (res.status === 429) throw new Error("Kredit limiti tugadi.");
  if (res.status === 401) throw new Error("Kirish rad etildi (API kalit).");
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

export interface ModelInfo {
  id: string;
  label: string;
  provider: string;
  available: boolean;
  default: boolean;
}

export const ask = (question: string, model?: string) =>
  post<AskResponse>("/ask", { question, model });

export const generate = (instruction: string, model?: string) =>
  post<GenerateResponse>("/generate", { instruction, model });

export const listAssets = () => get<AssetCard[]>("/assets");

export const listModels = () => get<ModelInfo[]>("/models");
