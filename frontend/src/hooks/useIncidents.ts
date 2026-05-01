import { useState, useEffect } from 'react'
import api from '../api/client'

export interface Incident {
  id: number
  prefix_code: string
  incident_type: string
  description?: string
  line?: string
  direction?: string
  created_by: number
  created_at: string
}

export function useIncidents() {
  const [incidents, setIncidents] = useState<Incident[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchIncidents = async () => {
    setLoading(true)
    try {
      const res = await api.get('/incidents/')
      setIncidents(res.data)
    } catch {
      setError('Erro ao carregar ocorrências')
    } finally {
      setLoading(false)
    }
  }

  const createIncident = async (data: Omit<Incident, 'id' | 'created_by' | 'created_at'>) => {
    const res = await api.post('/incidents/', data)
    setIncidents(prev => [res.data, ...prev])
    return res.data
  }

  const updateIncident = async (id: number, data: Partial<Incident>) => {
    const res = await api.put(`/incidents/${id}`, data)
    setIncidents(prev => prev.map(i => i.id === id ? res.data : i))
    return res.data
  }

  const deleteIncident = async (id: number) => {
    await api.delete(`/incidents/${id}`)
    setIncidents(prev => prev.filter(i => i.id !== id))
  }

  useEffect(() => { fetchIncidents() }, [])

  return { incidents, loading, error, fetchIncidents, createIncident, updateIncident, deleteIncident }
}
