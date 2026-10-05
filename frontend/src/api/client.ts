const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export async function apiClient<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE}/api${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  };

  try {
    const response = await fetch(url, { ...options, headers });
    if (!response.ok) {
      let errorMessage = `HTTP Error ${response.status}`;
      try {
        const errJson = await response.json();
        errorMessage = errJson.detail || errJson.message || errorMessage;
      } catch {
        // use status
      }
      throw new Error(errorMessage);
    }
    return (await response.json()) as T;
  } catch (error: any) {
    console.error(`API Request Failed: ${endpoint}`, error);
    throw error;
  }
}

export function getExportUrl(path: string): string {
  return `${API_BASE}/api${path}`;
}

export function getEventSourceUrl(path: string): string {
  return `${API_BASE}/api${path}`;
}
