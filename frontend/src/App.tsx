import React from 'react';
import { Routes, Route } from 'react-router-dom';
import RegisterScreen from './components/RegisterScreen';
import LoginScreen from './components/LoginScreen';
import CreateProjectScreen from './components/CreateProjectScreen';
import LandingScreen from './components/LandingScreen';
import ProjectListScreen from './components/ProjectListScreen';
import ProjectDetailsScreen from './components/ProjectDetailsScreen';
import ApiKeyManagementScreen from './components/ApiKeyManagementScreen';
import ProtectedRoute from './components/ProtectedRoute';
import './App.css';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<LoginScreen />} />
        <Route path="/register" element={<RegisterScreen />} />
        <Route path="/login" element={<LoginScreen />} />
        <Route path="/projects" element={
          <ProtectedRoute>
            <ProjectListScreen />
          </ProtectedRoute>
        } />
        <Route path="/projects/:projectId" element={
          <ProtectedRoute>
            <ProjectDetailsScreen />
          </ProtectedRoute>
        } />
        <Route path="/projects/:projectId/api-keys" element={
          <ProtectedRoute>
            <ApiKeyManagementScreen />
          </ProtectedRoute>
        } />
        <Route path="/create-project" element={
          <ProtectedRoute>
            <CreateProjectScreen />
          </ProtectedRoute>
        } />
        <Route path="/landing" element={
          <ProtectedRoute>
            <LandingScreen />
          </ProtectedRoute>
        } />
      </Routes>
    </div>
  );
}

export default App;
