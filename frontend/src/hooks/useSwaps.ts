import { useState, useEffect } from 'react'
import api from '../api/client'

export interface Swap {
  id: number
  vehicle_out: string
  vehicle_in: string
  lines_covered?: string
  created_by: number
  created_at: string
}

export function useSwaps() {
  const [swaps, setSwaps] = useState<Swap[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchSwaps = async () => {
    setLoading(true)
    try {
      const res = await api.get('/swaps/')
      setSwaps(res.data)
    } catch {
      setError('Erro ao carregar trocas')
    } finally {
      setLoading(false)
    }
  }

  const createSwap = async (data: Omit<Swap, 'id' | 'created_by' | 'created_at'>) => {
    const res = await api.post('/swaps/', data)
    setSwaps(prev => [res.data, ...prev])
    return res.data
  }

  const updateSwap = async (id: number, data: Partial<Swap>) => {
    const res = await api.put(`/swaps/${id}`, data)
    setSwaps(prev => prev.map(s => s.id === id ? res.data : s))
    return res.data
  }

  const deleteSwap = async (id: number) => {
    await api.delete(`/swaps/${id}`)
    setSwaps(prev => prev.filter(s => s.id !== id))
  }

  useEffect(() => { fetchSwaps() }, [])

  return { swaps, loading, error, fetchSwaps, createSwap, updateSwap, deleteSwap }
}
