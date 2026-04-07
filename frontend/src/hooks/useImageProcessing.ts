'use client';

import { useMemo, useState } from 'react';
import { postImage } from '../services/api';

export function useImageProcessing() {
  const [sourceFile, setSourceFile] = useState<File | null>(null);
  const [resultUrl, setResultUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const sourceUrl = useMemo(() => (sourceFile ? URL.createObjectURL(sourceFile) : null), [sourceFile]);

  async function runStage(endpoint: string, extra?: Record<string, string>) {
    if (!sourceFile) return;
    setLoading(true);
    try {
      const blob = await postImage(endpoint, sourceFile, extra);
      setResultUrl(URL.createObjectURL(blob));
    } finally {
      setLoading(false);
    }
  }

  return {
    sourceFile,
    sourceUrl,
    resultUrl,
    loading,
    setSourceFile,
    runStage,
  };
}
