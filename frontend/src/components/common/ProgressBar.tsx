import React from 'react';

interface ProgressBarProps {
  percentage: number;
  showLabel?: boolean;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({ percentage, showLabel = true }) => {
  const clamped = Math.min(100, Math.max(0, percentage));
  return (
    <div style={{ width: '100%' }}>
      {showLabel && (
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          fontSize: 'var(--font-size-xs)', 
          fontWeight: 'var(--font-weight-medium)',
          color: 'var(--color-text-secondary)',
          marginBottom: '4px'
        }}>
          <span>Progress</span>
          <span>{clamped.toFixed(1)}%</span>
        </div>
      )}
      <div className="progress-container">
        <div 
          className={`progress-bar ${clamped >= 100 ? 'success' : ''}`} 
          style={{ width: `${clamped}%` }}
        />
      </div>
    </div>
  );
};
