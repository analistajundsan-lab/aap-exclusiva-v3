import { ReactNode } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

export function Layout({ children }: { children: ReactNode }) {
  const { logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-blue-800 text-white px-6 py-3 flex items-center justify-between shadow">
        <div className="flex items-center gap-6">
          <span className="font-bold text-lg">AAP Exclusiva</span>
          <Link to="/dashboard" className="hover:text-blue-200 text-sm">Dashboard</Link>
          <Link to="/incidents" className="hover:text-blue-200 text-sm">Ocorrências</Link>
          <Link to="/swaps" className="hover:text-blue-200 text-sm">Trocas</Link>
        </div>
        <button onClick={handleLogout} className="text-sm hover:text-blue-200">
          Sair
        </button>
      </nav>
      <main className="p-6">{children}</main>
    </div>
  )
}
