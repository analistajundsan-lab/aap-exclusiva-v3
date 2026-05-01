import { useEffect, useState } from 'react'
import { Layout } from '../components/Layout'
import api from '../api/client'

export function Dashboard() {
  const [stats, setStats] = useState({ incidents: 0, swaps: 0 })

  useEffect(() => {
    Promise.all([
      api.get('/incidents/?limit=1'),
      api.get('/swaps/?limit=1'),
    ]).then(([inc, swp]) => {
      setStats({ incidents: inc.data.length, swaps: swp.data.length })
    }).catch(() => {})
  }, [])

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-6 text-gray-800">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-2xl">
        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-600">
          <p className="text-sm text-gray-500">Ocorrências (recentes)</p>
          <p className="text-3xl font-bold text-blue-700 mt-1">{stats.incidents}</p>
          <a href="/incidents" className="text-xs text-blue-600 hover:underline mt-2 block">Ver todas →</a>
        </div>
        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-green-600">
          <p className="text-sm text-gray-500">Trocas (recentes)</p>
          <p className="text-3xl font-bold text-green-700 mt-1">{stats.swaps}</p>
          <a href="/swaps" className="text-xs text-green-600 hover:underline mt-2 block">Ver todas →</a>
        </div>
      </div>
    </Layout>
  )
}
