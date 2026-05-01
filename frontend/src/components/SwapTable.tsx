import { Swap } from '../hooks/useSwaps'

interface Props {
  swaps: Swap[]
  onDelete?: (id: number) => void
  onEdit?: (swap: Swap) => void
}

export function SwapTable({ swaps, onDelete, onEdit }: Props) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm border-collapse">
        <thead>
          <tr className="bg-gray-100 text-left">
            <th className="px-4 py-2 border">SAI</th>
            <th className="px-4 py-2 border">ENTRA</th>
            <th className="px-4 py-2 border">Linhas</th>
            <th className="px-4 py-2 border">Data</th>
            <th className="px-4 py-2 border">Ações</th>
          </tr>
        </thead>
        <tbody>
          {swaps.length === 0 && (
            <tr><td colSpan={5} className="text-center py-4 text-gray-500">Nenhuma troca registrada</td></tr>
          )}
          {swaps.map(s => (
            <tr key={s.id} className="hover:bg-gray-50">
              <td className="px-4 py-2 border font-mono">{s.vehicle_out}</td>
              <td className="px-4 py-2 border font-mono">{s.vehicle_in}</td>
              <td className="px-4 py-2 border">{s.lines_covered || '—'}</td>
              <td className="px-4 py-2 border text-xs">{new Date(s.created_at).toLocaleString('pt-BR')}</td>
              <td className="px-4 py-2 border">
                <div className="flex gap-2">
                  {onEdit && <button onClick={() => onEdit(s)} className="text-blue-600 hover:underline text-xs">Editar</button>}
                  {onDelete && <button onClick={() => onDelete(s.id)} className="text-red-600 hover:underline text-xs">Deletar</button>}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
