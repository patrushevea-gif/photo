'use client';

type Props = {
  onFile: (file: File) => void;
};

export function UploadBox({ onFile }: Props) {
  return (
    <label style={{ border: '1px dashed #888', padding: 16, display: 'block', cursor: 'pointer' }}>
      Загрузить фото
      <input
        type="file"
        accept="image/*"
        style={{ display: 'none' }}
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) onFile(file);
        }}
      />
    </label>
  );
}
