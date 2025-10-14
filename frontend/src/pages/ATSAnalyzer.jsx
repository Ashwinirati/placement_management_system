import React, { useEffect, useMemo, useState } from 'react'
import { atsAnalyze, listStudentResumes } from '../api/client'

export default function ATSAnalyzer() {
  const [resumeText, setResumeText] = useState('')
  const [jdText, setJdText] = useState('')
  const [result, setResult] = useState({ score: 0, matched: [], missing: [], checks: { hasEmail:false, hasPhone:false, lengthOk:true } })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [resumes, setResumes] = useState([])
  const user = useMemo(() => JSON.parse(localStorage.getItem('pms_user') || 'null'), [])

  useEffect(() => {
    const run = async () => {
      try {
        if (user?.role === 'student') {
          const { data } = await listStudentResumes(user.id)
          setResumes(data)
        }
      } catch {}
    }
    run()
  }, [user])

  const analyze = async () => {
    setLoading(true)
    setError('')
    try {
      const { data } = await atsAnalyze(resumeText, jdText)
      setResult(data)
    } catch (err) {
      setError(err?.response?.data?.message || 'Analysis failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2>ATS Checker</h2>
      {user?.role === 'student' && resumes.length > 0 && (
        <div className="muted">Uploaded resumes: {resumes.map(r => r.filename).join(', ')}</div>
      )}
      <div className="grid">
        <div>
          <label>Paste Resume Text<textarea rows={12} value={resumeText} onChange={e=>setResumeText(e.target.value)} placeholder="Paste your resume text here for analysis..."/></label>
        </div>
        <div>
          <label>Paste Job Description<textarea rows={12} value={jdText} onChange={e=>setJdText(e.target.value)} placeholder="Paste the job description..."/></label>
        </div>
      </div>
      <button onClick={analyze} disabled={loading || !jdText} style={{marginTop:12}}>{loading ? 'Analyzing...' : 'Analyze'}</button>

      <div className="ats" style={{marginTop:12}}>
        <div className="score">Score: <strong>{result.score}%</strong></div>
        {result.subscores && (
          <div className="muted">Subscores — Keywords: {result.subscores.keywords ?? 0}%, Skills: {result.subscores.skills ?? 0}%, Formatting: {result.subscores.formatting ?? 0}%</div>
        )}
        <div className="checks">
          <div className={result.checks.hasEmail ? 'ok' : 'warn'}>Contact Email {result.checks.hasEmail ? '✓' : '✗'}</div>
          <div className={result.checks.hasPhone ? 'ok' : 'warn'}>Phone {result.checks.hasPhone ? '✓' : '✗'}</div>
          <div className={result.checks.lengthOk ? 'ok' : 'warn'}>Length under ~2 pages {result.checks.lengthOk ? '✓' : '✗'}</div>
        </div>
        <div className="grid">
          <div>
            <h4>Matched Keywords</h4>
            <div className="chips">
              {result.matched.slice(0,100).map(k => <span key={k} className="chip ok">{k}</span>)}
            </div>
          </div>
          <div>
            <h4>Missing Keywords</h4>
            <div className="chips">
              {result.missing.slice(0,100).map(k => <span key={k} className="chip warn">{k}</span>)}
            </div>
          </div>
        </div>
        {Array.isArray(result.suggestions) && result.suggestions.length > 0 && (
          <div style={{marginTop:10}}>
            <h4>Suggestions</h4>
            <ul className="list">
              {result.suggestions.map((s, i) => <li key={i} className="list-item">{s}</li>)}
            </ul>
          </div>
        )}
        {error && <div className="error">{error}</div>}
        <div className="muted">Tip: Incorporate relevant missing keywords naturally in your experience, skills, and projects.</div>
      </div>
    </div>
  )
}
