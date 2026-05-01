import { Incident } from '../hooks/useIncidents'

interface Props {
  incidents: Incident[]
  onDelete?: (id: number) => void
  onEdit?: (incident: Incident) => void
}

export function IncidentTable({ incidents, onDelete, onEdit }: Props) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm border-collapse">
        <thead>
          <tr className="bg-gray-100 text-left">
            <th className="px-4 py-2 border">Prefixo</th>
            <th className="px-4 py-2 border">Tipo</th>
            <th className="px-4 py-2 border">Linha</th>
            <th className="px-4 py-2 border">Sentido</th>
            <th className="px-4 py-2 border">Descrição</th>
            <th className="px-4 py-2 border">Data</th>
            <th className="px-4 py-2 border">Ações</th>
          </tr>
        </thead>
        <tbody>
          {incidents.length === 0 && (
            <tr><td colSpan={7} className="text-center py-4 text-gray-500">Nenhuma ocorrência</td></tr>
          )}
          {incidents.map(i => (
            <tr key={i.id} className="hover:bg-gray-50">
              <td className="px-4 py-2 border font-mono">{i.prefix_code}</td>
              <td className="px-4 py-2 border">{i.incident_type}</td>
              <td className="px-4 py-2 border">{i.line || '—'}</td>
              <td className="px-4 py-2 border">{i.direction || '—'}</td>
              <td className="px-4 py-2 border truncate max-w-xs">{i.description || '—'}</td>
              <td className="px-4 py-2 border text-xs">{new Date(i.created_at).toLocaleString('pt-BR')}</td>
              <td className="px-4 py-2 border">
                <div className="flex gap-2">
                  {onEdit && <button onClick={() => onEdit(i)} className="text-blue-600 hover:underline text-xs">Editar</button>}
                  {onDelete && <button onClick={() => onDelete(i.id)} className="text-red-600 hover:underline text-xs">Deletar</button>}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
