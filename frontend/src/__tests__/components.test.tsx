import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';
import { StatCard } from '../components/common/StatCard';
import { StatusBadge } from '../components/common/StatusBadge';
import { ProgressBar } from '../components/common/ProgressBar';
import { EmptyState } from '../components/common/EmptyState';
import { LoadingSkeleton } from '../components/common/LoadingSkeleton';

describe('Common UI Components', () => {
  it('renders StatCard correctly', () => {
    render(<StatCard label="Total Records" value="10,245" helper="Persisted" />);
    expect(screen.getByText('Total Records')).toBeDefined();
    expect(screen.getByText('10,245')).toBeDefined();
    expect(screen.getByText('Persisted')).toBeDefined();
  });

  it('renders StatusBadge with correct classes', () => {
    const { container: c1 } = render(<StatusBadge status="COMPLETED" />);
    expect(c1.querySelector('.badge-success')).toBeDefined();

    const { container: c2 } = render(<StatusBadge status="RUNNING" />);
    expect(c2.querySelector('.badge-info')).toBeDefined();

    const { container: c3 } = render(<StatusBadge status="FAILED" />);
    expect(c3.querySelector('.badge-danger')).toBeDefined();
  });

  it('renders ProgressBar percentage', () => {
    render(<ProgressBar percentage={72.5} />);
    expect(screen.getByText('72.5%')).toBeDefined();
  });

  it('renders EmptyState title and action', () => {
    render(
      <EmptyState 
        title="No Records" 
        message="Please start a job" 
        action={<button>Create Job</button>} 
      />
    );
    expect(screen.getByText('No Records')).toBeDefined();
    expect(screen.getByText('Please start a job')).toBeDefined();
    expect(screen.getByText('Create Job')).toBeDefined();
  });

  it('renders LoadingSkeleton with correct row count', () => {
    const { container } = render(<LoadingSkeleton rows={4} height={30} />);
    const skeletons = container.querySelectorAll('.skeleton');
    expect(skeletons.length).toBe(4);
  });
});
