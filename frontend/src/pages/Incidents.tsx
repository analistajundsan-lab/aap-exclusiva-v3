import { useState } from 'react'
import { Layout } from '../components/Layout'
import { IncidentTable } from '../components/IncidentTable'
import { IncidentForm } from '../components/IncidentForm'
import { useIncidents, Incident } from '../hooks/useIncidents'

export function Incidents() {
  const { incidents, loading, error, createIncident, updateIncident, deleteIncident } = useIncidents()
  const [modal, setModal] = useState<'create' | 'edit' | null>(null)
  const [editing, setEditing] = useState<Incident | null>(null)

  const handleCreate = async (data: Parameters<typeof createIncident>[0]) => {
    await createIncident(data)
    setModal(null)
  }

  const handleUpdate = async (data: Parameters<typeof createIncident>[0]) => {
    if (!editing) return
    await updateIncident(editing.id, data)
    setModal(null)
    setEditing(null)
  }

  const handleEdit = (incident: Incident) => {
    setEditing(incident)
    setModal('edit')
  }

  const handleDelete = async (id: number) => {
    if (confirm('Deletar esta ocorrência?')) await deleteIncident(id)
  }

  return (
    <Layout>
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-bold text-gray-800">Ocorrências</h1>
        <button onClick={() => setModal('create')}
          className="bg-blue-700 text-white px-4 py-2 rounded text-sm hover:bg-blue-800">
          + Nova Ocorrência
        </button>
      </div>

      {error && <p className="text-red-600 text-sm mb-3">{error}</p>}
      {loading ? <p className="text-gray-500">Carregando...</p> : (
        <div className="bg-white rounded-lg shadow">
          <IncidentTable incidents={incidents} onEdit={handleEdit} onDelete={handleDelete} />
        </div>
      )}

      {modal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-lg">
            <h2 className="text-lg font-semibold mb-4">
              {modal === 'create' ? 'Nova Ocorrência' : 'Editar Ocorrência'}
            </h2>
            <IncidentForm
              initial={editing || undefined}
              onSubmit={modal === 'create' ? handleCreate : handleUpdate}
              onCancel={() => { setModal(null); setEditing(null) }}
            />
          </div>
        </div>
      )}
    </Layout>
  )
}
