export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export interface Block {
  type: string;
  [key: string]: unknown;
}

export interface Site {
  id: string;
  name: string;
  theme: { primaryColor: string; fontFamily: string };
  blocks: Block[];
  version: number;
}

export async function createSite(name: string): Promise<Site> {
  const res = await fetch(`${API_URL}/sites?name=${encodeURIComponent(name)}`, {
    method: "POST",
  });
  if (!res.ok) throw new Error(`Site aanmaken mislukt (${res.status})`);
  return res.json();
}

export async function sendPrompt(
  siteId: string,
  message: string
): Promise<{ reply: string; site: Site }> {
  const res = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ siteId, message }),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new Error(body?.detail ?? `AI-opdracht mislukt (${res.status})`);
  }
  return res.json();
}

export function renderUrl(siteId: string): string {
  return `${API_URL}/sites/${siteId}/render`;
}
