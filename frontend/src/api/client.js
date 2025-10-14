import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
})

// Auth helpers
export const loginStudent = (email, password) => api.post('/login/student', { email, password })
export const loginRecruiter = (email, password) => api.post('/login/recruiter', { email, password })
export const registerStudent = (name, email, password) => api.post('/register/student', { name, email, password })
export const registerRecruiter = (name, email, password) => api.post('/register/recruiter', { name, email, password })

// Jobs
export const addJob = (title, description, recruiter_id) => api.post('/add', { title, description, recruiter_id })
export const listJobs = () => api.get('/list')

// Resumes
export const uploadResume = (student_id, file) => {
  const form = new FormData()
  form.append('file', file)
  return api.post(`/upload/${student_id}`, form, { headers: { 'Content-Type': 'multipart/form-data' } })
}
export const listStudentResumes = (student_id) => api.get(`/resumes/student/${student_id}`)

// Applications
export const applyToJob = (student_id, job_id) => api.post('/apply', { student_id, job_id })
export const listMyApplications = (student_id) => api.get(`/applications/student/${student_id}`)

// Interviews (optional usage in UI)
export const scheduleInterview = (application_id, scheduled_at, mode = 'online', notes = '') =>
  api.post('/interviews/schedule', { application_id, scheduled_at, mode, notes })
export const listInterviewsByApplication = (application_id) =>
  api.get(`/interviews/by-application/${application_id}`)

// ATS Analyze
export const atsAnalyze = (resume_text, jd_text) => api.post('/ats/analyze', { resume_text, jd_text })
export const atsAnalyzeFile = (file, jd_text) => {
  const form = new FormData()
  form.append('file', file)
  form.append('jd_text', jd_text)
  return api.post('/ats/analyze-file', form)
}
export const atsAnalyzeByResumeId = (resume_id, jd_text) => {
  const form = new FormData()
  form.append('resume_id', String(resume_id))
  form.append('jd_text', jd_text)
  return api.post('/ats/analyze-file', form)
}

// Analytics
export const getAnalyticsSummary = () => api.get('/analytics/summary')

export default api
