'use client';

type Props = {
  disabled?: boolean;
  onSelect: (machine: string) => void;
};

const options = [
  { value: 'sauno', label: 'Sauno (.bmp)' },
  { value: 'mirtels', label: 'Mirtels (.bmp)' },
  { value: 'laser', label: 'Laser (.bmp)' },
  { value: 'diamond', label: 'Diamond (.bmp)' },
];

export function MachineSelector({ disabled, onSelect }: Props) {
  return (
    <select disabled={disabled} onChange={(e) => onSelect(e.target.value)} defaultValue="sauno">
      {options.map((item) => (
        <option key={item.value} value={item.value}>{item.label}</option>
      ))}
    </select>
  );
}
