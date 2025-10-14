import React from 'react'
import { Navigate } from 'react-router-dom'

export default function ProtectedRoute({ children, role }) {
  const user = JSON.parse(localStorage.getItem('pms_user') || 'null')
  if (!user) return <Navigate to={role === 'recruiter' ? '/login/recruiter' : '/login/student'} replace />
  if (role && user.role !== role) return <Navigate to="/" replace />
  return children
}
