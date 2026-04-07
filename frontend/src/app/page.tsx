'use client';

import { useState } from 'react';
import { ImageBeforeAfter } from '../components/ImageBeforeAfter';
import { MachineSelector } from '../components/MachineSelector';
import { Toolbar } from '../components/Toolbar';
import { UploadBox } from '../components/UploadBox';
import { useImageProcessing } from '../hooks/useImageProcessing';

export default function Page() {
  const { sourceFile, sourceUrl, resultUrl, loading, setSourceFile, runStage, runExport } = useImageProcessing();
  const [machine, setMachine] = useState('sauno');

  return (
    <main style={{ display: 'grid', gap: 16 }}>
      <h1>Memorial Photo Pro</h1>
      <UploadBox onFile={setSourceFile} />
      <Toolbar
        disabled={!sourceFile || loading}
        onEnhance={() => runStage('/pipeline/enhance')}
        onRemoveBg={() => runStage('/pipeline/remove-bg')}
        onOutfit={() => runStage('/pipeline/outfit', { prompt: 'black business suit, tie, highly detailed' })}
        onMockup={() => runStage('/pipeline/mockup', { stone: 'gabbro' })}
      />
      <div style={{ display: 'flex', gap: 8 }}>
        <MachineSelector disabled={!sourceFile || loading} onSelect={setMachine} />
        <button disabled={!sourceFile || loading} onClick={() => runExport(machine, '90')}>Экспорт</button>
      </div>
      <ImageBeforeAfter before={sourceUrl} after={resultUrl} />
    </main>
  );
}
