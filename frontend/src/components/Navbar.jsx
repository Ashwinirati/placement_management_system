import React from 'react'
import { Link, useNavigate } from 'react-router-dom'

export default function Navbar() {
  const navigate = useNavigate()
  const user = JSON.parse(localStorage.getItem('pms_user') || 'null')

  const logout = () => {
    localStorage.removeItem('pms_user')
    navigate('/jobs')
  }

  return (
    <nav className="nav">
      <div className="nav-left">
        <Link to="/jobs" className="brand">PMS</Link>
        <Link to="/jobs">Jobs</Link>
        <Link to="/ats">ATS Checker</Link>
        {user?.role === 'student' && <Link to="/resume/upload">Upload Resume</Link>}
        {user?.role === 'student' && <Link to="/applications">My Applications</Link>}
        {user?.role === 'recruiter' && <Link to="/jobs/new">Post Job</Link>}
        {user?.role === 'admin' && <Link to="/admin">Admin</Link>}
      </div>
      <div className="nav-right">
        {!user && <>
          <Link to="/login/student">Student Login</Link>
          <Link to="/login/recruiter">Recruiter Login</Link>
        </>}
        {user && <>
          <span className="user">{user.name} ({user.role})</span>
          <button onClick={logout}>Logout</button>
        </>}
      </div>
    </nav>
  )
}
