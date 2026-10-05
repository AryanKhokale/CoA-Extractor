import React from 'react';

interface StatCardProps {
  label: string;
  value: string | number;
  helper?: string;
  icon?: React.ReactNode;
}

export const StatCard: React.FC<StatCardProps> = ({ label, value, helper, icon }) => {
  return (
    <div className="stat-card">
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <span className="stat-label">{label}</span>
        {icon && <div style={{ color: 'var(--color-primary)', opacity: 0.8 }}>{icon}</div>}
      </div>
      <div className="stat-value">{value}</div>
      {helper && <div className="stat-helper">{helper}</div>}
    </div>
  );
};
