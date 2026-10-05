import React from 'react';
import { JobStatus } from '../../types';

interface StatusBadgeProps {
  status: JobStatus | string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const normalized = status.toUpperCase();

  let badgeClass = 'badge-info';
  if (normalized === 'COMPLETED' || normalized === 'ACTIVE') {
    badgeClass = 'badge-success';
  } else if (normalized === 'RUNNING') {
    badgeClass = 'badge-info';
  } else if (normalized === 'FAILED' || normalized === 'DEFAULTER') {
    badgeClass = 'badge-danger';
  } else if (normalized === 'PENDING' || normalized === 'CANCELLED' || normalized === 'INACTIVE') {
    badgeClass = 'badge-warning';
  }

  return (
    <span className={`badge ${badgeClass}`}>
      <span style={{
        width: 6,
        height: 6,
        borderRadius: '50%',
        backgroundColor: 'currentColor'
      }} />
      {normalized}
    </span>
  );
};
