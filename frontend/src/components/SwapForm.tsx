import { useState } from 'react'
import { Swap } from '../hooks/useSwaps'

interface Props {
  initial?: Partial<Swap>
  onSubmit: (data: Omit<Swap, 'id' | 'created_by' | 'created_at'>) => Promise<void>
  onCancel: () => void
}

export function SwapForm({ initial, onSubmit, onCancel }: Props) {
  const [form, setForm] = useState({
    vehicle_out: initial?.vehicle_out || '',
    vehicle_in: initial?.vehicle_in || '',
    lines_covered: initial?.lines_covered || '',
  })

  const handle = (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm(f => ({ ...f, [e.target.name]: e.target.value }))

  return (
    <div className="space-y-3">
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-sm font-medium mb-1">Prefixo SAI *</label>
          <input name="vehicle_out" value={form.vehicle_out} onChange={handle}
            className="w-full border rounded px-3 py-2 text-sm" placeholder="Ex: 4521" />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Prefixo ENTRA *</label>
          <input name="vehicle_in" value={form.vehicle_in} onChange={handle}
            className="w-full border rounded px-3 py-2 text-sm" placeholder="Ex: 4522" />
        </div>
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">Linhas Cobertas</label>
        <input name="lines_covered" value={form.lines_covered} onChange={handle}
          className="w-full border rounded px-3 py-2 text-sm" placeholder="Ex: 803, 804" />
      </div>
      <div className="flex gap-2 justify-end">
        <button onClick={onCancel} className="px-4 py-2 text-sm border rounded hover:bg-gray-100">Cancelar</button>
        <button onClick={() => onSubmit(form)} className="px-4 py-2 text-sm bg-green-700 text-white rounded hover:bg-green-800">
          Salvar
        </button>
      </div>
    </div>
  )
}
