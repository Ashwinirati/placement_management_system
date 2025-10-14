import React, { useEffect, useState } from 'react'
import { getAnalyticsSummary } from '../api/client'

export default function AdminDashboard() {
  const [stats, setStats] = useState({ jobs: 0, recruiters: 0, students: 0, applications: 0, hired: 0 })

  useEffect(() => {
    const run = async () => {
      try {
        const { data } = await getAnalyticsSummary()
        setStats(data)
      } catch {}
    }
    run()
  }, [])

  return (
    <div className="card">
      <h2>Placement Analytics</h2>
      <div className="stats">
        <div className="stat"><div className="stat-num">{stats.students}</div><div className="stat-label">Students</div></div>
        <div className="stat"><div className="stat-num">{stats.recruiters}</div><div className="stat-label">Recruiters</div></div>
        <div className="stat"><div className="stat-num">{stats.jobs}</div><div className="stat-label">Jobs</div></div>
        <div className="stat"><div className="stat-num">{stats.applications}</div><div className="stat-label">Applications</div></div>
        <div className="stat"><div className="stat-num">{stats.hired}</div><div className="stat-label">Hires</div></div>
      </div>
    </div>
  )
}
