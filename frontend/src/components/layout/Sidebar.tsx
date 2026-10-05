import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Compass, 
  Layers, 
  Table, 
  BarChart2, 
  BookOpen, 
  Settings as SettingsIcon,
  Building2
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <Building2 size={28} color="var(--color-primary)" />
        <div>
          <h1 className="brand-title">CoA Extractor</h1>
          <span className="brand-subtitle">Architecture Pipeline</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        <NavLink to="/dashboard" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <LayoutDashboard size={18} />
          <span>Dashboard</span>
        </NavLink>

        <NavLink to="/directory" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <Compass size={18} />
          <span>Directory Explorer</span>
        </NavLink>

        <NavLink to="/jobs" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <Layers size={18} />
          <span>Extraction Jobs</span>
        </NavLink>

        <NavLink to="/data" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <Table size={18} />
          <span>Data Preview</span>
        </NavLink>

        <NavLink to="/analytics" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <BarChart2 size={18} />
          <span>Analytics</span>
        </NavLink>

        <NavLink to="/docs" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <BookOpen size={18} />
          <span>Documentation</span>
        </NavLink>

        <NavLink to="/settings" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <SettingsIcon size={18} />
          <span>Settings</span>
        </NavLink>
      </nav>

      <div className="sidebar-footer">
        <p>Council of Architecture</p>
        <p style={{ marginTop: '2px', opacity: 0.8 }}>Statutory Statutory Body, GoI</p>
      </div>
    </aside>
  );
};
