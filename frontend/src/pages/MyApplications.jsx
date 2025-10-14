import React, { useEffect, useMemo, useState } from 'react'
import { listMyApplications } from '../api/client'

export default function MyApplications() {
  const user = useMemo(() => JSON.parse(localStorage.getItem('pms_user') || 'null'), [])
  const [apps, setApps] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const run = async () => {
      if (!user) return
      setLoading(true)
      setError('')
      try {
        const { data } = await listMyApplications(user.id)
        setApps(data)
      } catch (err) {
        setError('Failed to load applications')
      } finally {
        setLoading(false)
      }
    }
    run()
  }, [user])

  return (
    <div className="card">
      <h2>My Applications</h2>
      {loading && <div>Loading...</div>}
      {error && <div className="error">{error}</div>}
      <ul className="list">
        {apps.map(a => (
          <li key={a.id} className="list-item">
            <div className="job-title">{a.title}</div>
            <div className="job-meta">By {a.recruiter_name} • Status: {a.status}</div>
            <p className="job-desc">{a.description}</p>
          </li>
        ))}
      </ul>
      {!loading && apps.length === 0 && <div>No applications yet.</div>}
    </div>
  )
}
