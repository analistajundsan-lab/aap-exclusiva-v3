import { useState } from 'react'
import { Layout } from '../components/Layout'
import { SwapTable } from '../components/SwapTable'
import { SwapForm } from '../components/SwapForm'
import { useSwaps, Swap } from '../hooks/useSwaps'

export function Swaps() {
  const { swaps, loading, error, createSwap, updateSwap, deleteSwap } = useSwaps()
  const [modal, setModal] = useState<'create' | 'edit' | null>(null)
  const [editing, setEditing] = useState<Swap | null>(null)

  const handleCreate = async (data: Parameters<typeof createSwap>[0]) => {
    await createSwap(data)
    setModal(null)
  }

  const handleUpdate = async (data: Parameters<typeof createSwap>[0]) => {
    if (!editing) return
    await updateSwap(editing.id, data)
    setModal(null)
    setEditing(null)
  }

  const handleEdit = (swap: Swap) => {
    setEditing(swap)
    setModal('edit')
  }

  const handleDelete = async (id: number) => {
    if (confirm('Deletar esta troca?')) await deleteSwap(id)
  }

  return (
    <Layout>
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-bold text-gray-800">Trocas de Veículos</h1>
        <button onClick={() => setModal('create')}
          className="bg-green-700 text-white px-4 py-2 rounded text-sm hover:bg-green-800">
          + Nova Troca
        </button>
      </div>

      {error && <p className="text-red-600 text-sm mb-3">{error}</p>}
      {loading ? <p className="text-gray-500">Carregando...</p> : (
        <div className="bg-white rounded-lg shadow">
          <SwapTable swaps={swaps} onEdit={handleEdit} onDelete={handleDelete} />
        </div>
      )}

      {modal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-md">
            <h2 className="text-lg font-semibold mb-4">
              {modal === 'create' ? 'Nova Troca' : 'Editar Troca'}
            </h2>
            <SwapForm
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
