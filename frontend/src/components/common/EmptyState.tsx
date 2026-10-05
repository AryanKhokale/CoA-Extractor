import React from 'react';
import { Inbox } from 'lucide-react';

interface EmptyStateProps {
  title: string;
  message: string;
  action?: React.ReactNode;
  icon?: React.ReactNode;
}

export const EmptyState: React.FC<EmptyStateProps> = ({ 
  title, 
  message, 
  action, 
  icon = <Inbox size={48} color="var(--color-text-muted)" /> 
}) => {
  return (
    <div className="empty-state">
      {icon}
      <h3>{title}</h3>
      <p style={{ maxWidth: '400px', marginBottom: 'var(--spacing-md)' }}>{message}</p>
      {action}
    </div>
  );
};
