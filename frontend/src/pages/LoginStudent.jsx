import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { loginStudent } from '../api/client'

export default function LoginStudent() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const submit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const { data } = await loginStudent(email, password)
      localStorage.setItem('pms_user', JSON.stringify({ ...data.user, role: 'student' }))
      navigate('/jobs')
    } catch (err) {
      setError(err?.response?.data?.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2>Student Login</h2>
      <form onSubmit={submit}>
        <label>Email<input value={email} onChange={e=>setEmail(e.target.value)} type="email" required /></label>
        <label>Password<input value={password} onChange={e=>setPassword(e.target.value)} type="password" required /></label>
        {error && <div className="error">{error}</div>}
        <button disabled={loading}>{loading ? 'Logging in...' : 'Login'}</button>
      </form>
      <div className="muted">No account? <Link to="/register/student">Register</Link></div>
    </div>
  )
}
