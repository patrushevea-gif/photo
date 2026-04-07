'use client';

type Props = {
  before?: string | null;
  after?: string | null;
};

export function ImageBeforeAfter({ before, after }: Props) {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
      <div>
        <h4>До</h4>
        {before ? <img src={before} alt="before" style={{ width: '100%' }} /> : <p>Нет изображения</p>}
      </div>
      <div>
        <h4>После</h4>
        {after ? <img src={after} alt="after" style={{ width: '100%' }} /> : <p>Нет изображения</p>}
      </div>
    </div>
  );
}
