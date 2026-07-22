import { NavLink } from 'react-router-dom'
import { Package, Settings } from 'lucide-react'
import { cn } from '@/lib/utils'

interface SidebarSection {
  label: string
  to: string
  icon: typeof Package
}

/** Top-level resources the user has access to. Add new entries here as new root-level sections appear. */
const SECTIONS: SidebarSection[] = [{ label: 'Oferty', to: '/', icon: Package }]

const navLinkClassName = ({ isActive }: { isActive: boolean }) =>
  cn(
    'flex items-center gap-2 rounded-md px-2 py-2 text-sm',
    isActive
      ? 'bg-accent text-accent-foreground'
      : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground',
  )

/** Global left-hand resource navigation, persistent across the whole app. */
export function AppSidebar() {
  return (
    <aside className="hidden w-60 shrink-0 flex-col border-r p-4 md:flex">
      <h2 className="mb-2 px-2 text-xs font-medium tracking-wide text-muted-foreground uppercase">
        Zasoby
      </h2>
      <nav className="space-y-1">
        {SECTIONS.map(({ label, to, icon: Icon }) => (
          <NavLink key={to} to={to} end={to === '/'} className={navLinkClassName}>
            <Icon className="size-4" />
            {label}
          </NavLink>
        ))}
      </nav>

      <nav className="mt-auto space-y-1 border-t pt-2">
        <NavLink to="/settings" className={navLinkClassName}>
          <Settings className="size-4" />
          Ustawienia
        </NavLink>
      </nav>
    </aside>
  )
}
