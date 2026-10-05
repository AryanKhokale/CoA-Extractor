import React, { useEffect, useState } from 'react';
import { configApi } from '../../api/analytics';
import { SystemConfig } from '../../types';
import { Download, RefreshCw } from 'lucide-react';
import { getExportUrl } from '../../api/client';

export const Navbar: React.FC = () => {
  const [config, setConfig] = useState<SystemConfig | null>(null);

  useEffect(() => {
    configApi.getConfig().then(setConfig).catch(() => null);
  }, []);

  return (
    <header className="navbar">
      <div className="navbar-status">
        <div className={`status-dot ${config?.use_mock_data ? 'mock' : ''}`} />
        <span>
          {config?.use_mock_data 
            ? 'Development Mode (Synthetic / Offline)' 
            : 'Live Pipeline (coa.gov.in Active)'}
        </span>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)' }}>
        <a 
          href={getExportUrl('/export/csv')} 
          className="btn btn-secondary btn-sm"
          download="all_coa_architects.csv"
        >
          <Download size={14} />
          <span>Export All CSV</span>
        </a>

        <a 
          href={getExportUrl('/export/json')} 
          className="btn btn-secondary btn-sm"
          download="all_coa_architects.json"
        >
          <Download size={14} />
          <span>Export JSON</span>
        </a>
      </div>
    </header>
  );
};
