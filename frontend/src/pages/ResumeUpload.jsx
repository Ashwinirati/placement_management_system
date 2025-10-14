import React, { useMemo, useState } from 'react'
import { uploadResume } from '../api/client'
import { atsAnalyzeFile } from '../api/client'

export default function ResumeUpload() {
  const user = useMemo(() => JSON.parse(localStorage.getItem('pms_user') || 'null'), [])
  const [file, setFile] = useState(null)
  const [msg, setMsg] = useState('')
  const [loading, setLoading] = useState(false)
  const [jd, setJd] = useState('')
  const [result, setResult] = useState(null)

  const submit = async (e) => {
    e.preventDefault()
    if (!file) return setMsg('Select a file')
    setMsg('')
    setLoading(true)
    try {
      const { data } = await uploadResume(user.id, file)
      setMsg(data.message)
      // Immediately analyze the uploaded file using backend ATS file analyzer
      const { data: analysis } = await atsAnalyzeFile(file, jd)
      setResult(analysis)
      setFile(null)
    } catch (err) {
      setMsg(err?.response?.data?.message || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2>Upload Resume + ATS Score</h2>
      <form onSubmit={submit}>
        <label>Job Description<textarea rows={6} value={jd} onChange={e=>setJd(e.target.value)} placeholder="Paste the target job description here..."/></label>
        <input type="file" accept=".pdf,.doc,.docx" onChange={e=>setFile(e.target.files?.[0])} />
        {msg && <div className="info">{msg}</div>}
        <button disabled={loading || !file || !jd}>{loading ? 'Uploading & Analyzing...' : 'Upload & Analyze'}</button>
      </form>
      {result && (
        <div className="ats" style={{marginTop:12}}>
          <div className="score">Score: <strong>{result.score}%</strong></div>
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
        </div>
      )}
    </div>
  )
}
