import React, { useState } from 'react'
import { addJob } from '../api/client'

export default function JobCreate() {
  const user = JSON.parse(localStorage.getItem('pms_user') || 'null')
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [msg, setMsg] = useState('')
  const [loading, setLoading] = useState(false)

  const submit = async (e) => {
    e.preventDefault()
    setMsg('')
    setLoading(true)
    try {
      const { data } = await addJob(title, description, user.id)
      setMsg(data.message)
      setTitle('')
      setDescription('')
    } catch (err) {
      setMsg(err?.response?.data?.message || 'Failed to add job')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2>Post a Job</h2>
      <form onSubmit={submit}>
        <label>Title<input value={title} onChange={e=>setTitle(e.target.value)} required/></label>
        <label>Description<textarea value={description} onChange={e=>setDescription(e.target.value)} rows={6} required/></label>
        {msg && <div className="info">{msg}</div>}
        <button disabled={loading}>{loading ? 'Posting...' : 'Post Job'}</button>
      </form>
    </div>
  )
}
