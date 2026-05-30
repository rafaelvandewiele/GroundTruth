const API_BASE = 'https://your-backend.railway.app/api/v1'; // change after deploy

export interface Source {
  url: string;
  title: string;
  snippet: string;
}

export interface ClaimResult {
  claim: string;
  verdict: 'waar' | 'onwaar' | 'genuanceerd' | 'onverifieerbaar';
  verdict_en: 'true' | 'false' | 'nuanced' | 'unverifiable';
  explanation: string;
  confidence: number;
  sources: Source[];
}

export interface CheckResponse {
  id: string;
  original_text: string;
  language: string;
  claims: ClaimResult[];
  created_at: string;
  cached: boolean;
}

export async function checkText(
  text: string,
  userId?: string,
  imageBase64?: string
): Promise<CheckResponse> {
  const response = await fetch(`${API_BASE}/check`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text,
      user_id: userId,
      image_base64: imageBase64,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Something went wrong');
  }

  return response.json();
}
