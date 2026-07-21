import { NavLink, Route, Routes } from 'react-router-dom'
import { cn } from '@/lib/utils'
import Home from '@/pages/Home'
import About from '@/pages/About'

function App() {
  return (
    <div className="min-h-svh">
      <nav className="flex gap-4 border-b p-4">
        <NavLink
          to="/"
          end
          className={({ isActive }) =>
            cn('text-sm font-medium', isActive && 'text-primary underline')
          }
        >
          Home
        </NavLink>
        <NavLink
          to="/about"
          className={({ isActive }) =>
            cn('text-sm font-medium', isActive && 'text-primary underline')
          }
        >
          About
        </NavLink>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </div>
  )
}

export default App
