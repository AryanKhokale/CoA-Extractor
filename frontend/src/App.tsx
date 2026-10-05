import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/layout/Layout';
import { DashboardPage } from './pages/DashboardPage';
import { DirectoryPage } from './pages/DirectoryPage';
import { JobsPage } from './pages/JobsPage';
import { JobDetailPage } from './pages/JobDetailPage';
import { DataPreviewPage } from './pages/DataPreviewPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { DocumentationPage } from './pages/DocumentationPage';
import { SettingsPage } from './pages/SettingsPage';
import './styles/globals.css';

export function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="directory" element={<DirectoryPage />} />
          <Route path="jobs" element={<JobsPage />} />
          <Route path="jobs/:id" element={<JobDetailPage />} />
          <Route path="data" element={<DataPreviewPage />} />
          <Route path="analytics" element={<AnalyticsPage />} />
          <Route path="docs" element={<DocumentationPage />} />
          <Route path="settings" element={<SettingsPage />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
