import { useState } from 'react'
import api from '../api/client'
import { useAuthStore } from '../store/auth'

export function useAuth() {
  const { token, role, setAuth, logout } = useAuthStore()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const login = async (cpf: string, password: string) => {
    setLoading(true)
    setError(null)
    try {
      const res = await api.post('/auth/login', { cpf, password })
      // Decode role from JWT payload
      const payload = JSON.parse(atob(res.data.access_token.split('.')[1]))
      setAuth(res.data.access_token, payload.role || 'operator')
      return true
    } catch {
      setError('CPF ou senha inválidos')
      return false
    } finally {
      setLoading(false)
    }
  }

  return { token, role, login, logout, loading, error, isAuthenticated: !!token }
}
