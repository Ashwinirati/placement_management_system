import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Navbar from './components/Navbar'
import ProtectedRoute from './components/ProtectedRoute'
import LoginStudent from './pages/LoginStudent'
import LoginRecruiter from './pages/LoginRecruiter'
import RegisterStudent from './pages/RegisterStudent'
import RegisterRecruiter from './pages/RegisterRecruiter'
import JobsList from './pages/JobsList'
import JobCreate from './pages/JobCreate'
import ResumeUpload from './pages/ResumeUpload'
import ATSAnalyzer from './pages/ATSAnalyzer'
import AdminDashboard from './pages/AdminDashboard'
import MyApplications from './pages/MyApplications'

export default function App() {
  return (
    <div className="container">
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to="/jobs" replace />} />
        <Route path="/login/student" element={<LoginStudent />} />
        <Route path="/login/recruiter" element={<LoginRecruiter />} />
        <Route path="/register/student" element={<RegisterStudent />} />
        <Route path="/register/recruiter" element={<RegisterRecruiter />} />
        <Route path="/jobs" element={<JobsList />} />
        <Route path="/jobs/new" element={<ProtectedRoute role="recruiter"><JobCreate /></ProtectedRoute>} />
        <Route path="/resume/upload" element={<ProtectedRoute role="student"><ResumeUpload /></ProtectedRoute>} />
        <Route path="/ats" element={<ATSAnalyzer />} />
        <Route path="/applications" element={<ProtectedRoute role="student"><MyApplications /></ProtectedRoute>} />
        <Route path="/admin" element={<ProtectedRoute role="admin"><AdminDashboard /></ProtectedRoute>} />
        <Route path="*" element={<div style={{padding:16}}>Page not found</div>} />
      </Routes>
    </div>
  )
}
