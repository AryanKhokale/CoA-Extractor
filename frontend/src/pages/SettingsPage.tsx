import React, { useEffect, useState } from 'react';
import { PageHeader } from '../components/common/PageHeader';
import { configApi } from '../api/analytics';
import { SystemConfig } from '../types';
import { Settings as SettingsIcon, Shield, Server, CheckCircle2, RefreshCw } from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const [config, setConfig] = useState<SystemConfig | null>(null);
  const [testing, setTesting] = useState(false);
  const [healthStatus, setHealthStatus] = useState<string | null>(null);

  const loadConfig = async () => {
    try {
      const data = await configApi.getConfig();
      setConfig(data);
    } catch (err) {
      console.error('Failed to load system config', err);
    }
  };

  useEffect(() => {
    loadConfig();
  }, []);

  const testConnection = async () => {
    setTesting(true);
    setHealthStatus(null);
    try {
      const res = await fetch(`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/health`);
      if (res.ok) {
        const json = await res.json();
        setHealthStatus(`Connected! Service: ${json.service} v${json.version}`);
      } else {
        setHealthStatus(`Server responded with HTTP ${res.status}`);
      }
    } catch (err: any) {
      setHealthStatus(`Connection failed: ${err.message}`);
    } finally {
      setTesting(false);
    }
  };

  return (
    <div>
      <PageHeader 
        title="Settings & System Configuration"
        description="Inspect pipeline configuration, network boundaries, and deployment parameters."
      />

      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-lg)', maxWidth: '800px' }}>
        
        {/* Runtime Configuration */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-xs)' }}>
              <Server size={18} />
              <span>Extraction Engine Settings</span>
            </h2>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 'var(--spacing-md)' }}>
            <div>
              <span className="stat-label">Target Portal URL</span>
              <p style={{ marginTop: '4px', fontWeight: 'var(--font-weight-medium)' }}>
                {config?.coa_base_url || 'https://www.coa.gov.in'}
              </p>
            </div>

            <div>
              <span className="stat-label">Max Concurrency Limit</span>
              <p style={{ marginTop: '4px', fontWeight: 'var(--font-weight-medium)' }}>
                {config?.max_concurrency || 5} concurrent workers
              </p>
            </div>

            <div>
              <span className="stat-label">Default Request Rate</span>
              <p style={{ marginTop: '4px', fontWeight: 'var(--font-weight-medium)' }}>
                {config?.default_requests_per_second || 2.0} requests / sec
              </p>
            </div>

            <div>
              <span className="stat-label">Request Timeout</span>
              <p style={{ marginTop: '4px', fontWeight: 'var(--font-weight-medium)' }}>
                {config?.default_timeout_seconds || 30} seconds
              </p>
            </div>

            <div>
              <span className="stat-label">Active Operational Mode</span>
              <div style={{ marginTop: '4px' }}>
                <span className={`badge ${config?.use_mock_data ? 'badge-warning' : 'badge-success'}`}>
                  {config?.use_mock_data ? 'MOCK / OFFLINE' : 'LIVE PRODUCTION'}
                </span>
              </div>
            </div>

            <div>
              <span className="stat-label">Backend Version</span>
              <p style={{ marginTop: '4px', fontWeight: 'var(--font-weight-medium)' }}>
                v{config?.version || '1.0.0'}
              </p>
            </div>
          </div>
        </div>

        {/* Connectivity Diagnostics */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-xs)' }}>
              <Shield size={18} />
              <span>Backend Connectivity Diagnostics</span>
            </h2>
          </div>

          <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)', marginBottom: 'var(--spacing-md)' }}>
            Verify API health endpoint responsiveness and latency from your current environment.
          </p>

          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-md)' }}>
            <button className="btn btn-secondary" onClick={testConnection} disabled={testing}>
              <RefreshCw size={14} className={testing ? 'animate-spin' : ''} />
              <span>{testing ? 'Testing...' : 'Test Connection'}</span>
            </button>

            {healthStatus && (
              <span style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-success)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                <CheckCircle2 size={16} />
                <span>{healthStatus}</span>
              </span>
            )}
          </div>
        </div>

        {/* Deployment Metadata */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Production Infrastructure</h2>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-sm)', fontSize: 'var(--font-size-sm)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--color-border-subtle)', paddingBottom: 'var(--spacing-xs)' }}>
              <span style={{ color: 'var(--color-text-muted)' }}>Frontend Host:</span>
              <strong>Vercel (Edge CDN)</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--color-border-subtle)', paddingBottom: 'var(--spacing-xs)' }}>
              <span style={{ color: 'var(--color-text-muted)' }}>Backend Host:</span>
              <strong>Render (FastAPI Web Service)</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--color-text-muted)' }}>Database:</span>
              <strong>PostgreSQL / SQLite Zero-Cost Persistence</strong>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};
