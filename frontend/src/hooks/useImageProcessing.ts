'use client';

import { useMemo, useState } from 'react';
import { downloadBlob, postImage } from '../services/api';

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
      return blob;
    } finally {
      setLoading(false);
    }
  }

  async function runExport(machine: string, dpi = '90') {
    const blob = await runStage('/export/machine', { machine, dpi });
    if (blob) {
      downloadBlob(blob, `memorial_export_${machine}.bmp`);
    }
  }

  return {
    sourceFile,
    sourceUrl,
    resultUrl,
    loading,
    setSourceFile,
    runStage,
    runExport,
  };
}
