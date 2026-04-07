'use client';

type Props = {
  disabled?: boolean;
  onEnhance: () => void;
  onRemoveBg: () => void;
  onOutfit: () => void;
  onMockup: () => void;
};

export function Toolbar({ disabled, onEnhance, onRemoveBg, onOutfit, onMockup }: Props) {
  return (
    <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
      <button disabled={disabled} onClick={onEnhance}>Enhance</button>
      <button disabled={disabled} onClick={onRemoveBg}>Remove BG</button>
      <button disabled={disabled} onClick={onOutfit}>Outfit</button>
      <button disabled={disabled} onClick={onMockup}>Mockup</button>
    </div>
  );
}
