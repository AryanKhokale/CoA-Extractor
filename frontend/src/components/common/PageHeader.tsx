import React from 'react';

interface PageHeaderProps {
  title: string;
  description?: string;
  badge?: React.ReactNode;
  actions?: React.ReactNode;
}

export const PageHeader: React.FC<PageHeaderProps> = ({ title, description, badge, actions }) => {
  return (
    <div style={{
      display: 'flex',
      alignItems: 'flex-start',
      justifyContent: 'space-between',
      flexWrap: 'wrap',
      gap: 'var(--spacing-md)',
      marginBottom: 'var(--spacing-xl)'
    }}>
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)' }}>
          <h1 style={{ 
            fontSize: 'var(--font-size-2xl)', 
            fontWeight: 'var(--font-weight-bold)',
            color: 'var(--color-text-primary)'
          }}>
            {title}
          </h1>
          {badge}
        </div>
        {description && (
          <p style={{ 
            color: 'var(--color-text-secondary)', 
            fontSize: 'var(--font-size-sm)',
            marginTop: '4px',
            maxWidth: '700px'
          }}>
            {description}
          </p>
        )}
      </div>
      {actions && (
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)' }}>
          {actions}
        </div>
      )}
    </div>
  );
};
