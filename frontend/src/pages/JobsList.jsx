import React, { useEffect, useMemo, useState } from 'react'
import { listJobs, applyToJob, listMyApplications } from '../api/client'

export default function JobsList() {
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [applying, setApplying] = useState(0)
  const [myApps, setMyApps] = useState([])
  const user = useMemo(() => JSON.parse(localStorage.getItem('pms_user') || 'null'), [])

  useEffect(() => {
    const run = async () => {
      setLoading(true)
      setError('')
      try {
        const [{ data: jobsData }, appsData] = await Promise.all([
          listJobs(),
          user?.role === 'student' ? listMyApplications(user.id) : Promise.resolve({ data: [] })
        ])
        setJobs(jobsData)
        setMyApps(appsData?.data || [])
      } catch (err) {
        setError('Failed to load jobs')
      } finally {
        setLoading(false)
      }
    }
    run()
  }, [user])

  const appliedSet = useMemo(() => new Set(myApps.map(a => a.job_id)), [myApps])

  const onApply = async (jobId) => {
    if (!user || user.role !== 'student') {
      setError('Login as student to apply')
      return
    }
    try {
      setApplying(jobId)
      await applyToJob(user.id, jobId)
      const { data } = await listMyApplications(user.id)
      setMyApps(data)
    } catch (err) {
      setError(err?.response?.data?.message || 'Failed to apply')
    } finally {
      setApplying(0)
    }
  }

  return (
    <div className="card">
      <h2>Open Jobs</h2>
      {loading && <div>Loading...</div>}
      {error && <div className="error">{error}</div>}
      {!loading && jobs.length === 0 && <div>No jobs yet.</div>}
      <ul className="list">
        {jobs.map(j => (
          <li key={j.id} className="list-item">
            <div className="job-title">{j.title}</div>
            <div className="job-meta">By {j.recruiter_name}</div>
            <p className="job-desc">{j.description}</p>
            {user?.role === 'student' && (
              <div>
                <button
                  onClick={() => onApply(j.id)}
                  disabled={applying === j.id || appliedSet.has(j.id)}
                  style={{marginTop:8}}
                >
                  {appliedSet.has(j.id) ? 'Applied' : (applying === j.id ? 'Applying...' : 'Apply')}
                </button>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}
