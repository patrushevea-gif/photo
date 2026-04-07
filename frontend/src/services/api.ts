const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function postImage(endpoint: string, file: File, extra?: Record<string, string>): Promise<Blob> {
  const formData = new FormData();
  formData.append('file', file);

  if (extra) {
    Object.entries(extra).forEach(([key, value]) => formData.append(key, value));
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return await response.blob();
}

export function downloadBlob(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
