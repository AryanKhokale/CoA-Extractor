import React from 'react';

interface LoadingSkeletonProps {
  rows?: number;
  height?: number;
}

export const LoadingSkeleton: React.FC<LoadingSkeletonProps> = ({ rows = 5, height = 36 }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-sm)', width: '100%' }}>
      {Array.from({ length: rows }).map((_, i) => (
        <div 
          key={i} 
          className="skeleton" 
          style={{ height: `${height}px`, width: '100%' }}
        />
      ))}
    </div>
  );
};
