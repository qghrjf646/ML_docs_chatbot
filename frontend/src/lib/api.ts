export function buildApiUrl(path: string, baseUrl?: string): string {
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;

  const rawBase = (baseUrl ?? import.meta.env.VITE_API_BASE_URL ?? "").trim();
  if (!rawBase || rawBase === "/") {
    return normalizedPath;
  }

  const normalizedBase = rawBase.endsWith("/") ? rawBase.slice(0, -1) : rawBase;
  return `${normalizedBase}${normalizedPath}`;
}
