import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { registerStudent } from '../api/client'

export default function RegisterStudent() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [msg, setMsg] = useState('')
  const navigate = useNavigate()

  const submit = async (e) => {
    e.preventDefault()
    setMsg('')
    setLoading(true)
    try {
      const { data } = await registerStudent(name, email, password)
      setMsg(data.message)
      setTimeout(()=>navigate('/login/student'), 800)
    } catch (err) {
      setMsg(err?.response?.data?.message || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2>Student Registration</h2>
      <form onSubmit={submit}>
        <label>Name<input value={name} onChange={e=>setName(e.target.value)} required /></label>
        <label>Email<input value={email} onChange={e=>setEmail(e.target.value)} type="email" required /></label>
        <label>Password<input value={password} onChange={e=>setPassword(e.target.value)} type="password" required /></label>
        {msg && <div className="info">{msg}</div>}
        <button disabled={loading}>{loading ? 'Registering...' : 'Register'}</button>
      </form>
    </div>
  )
}
