import { Link, Outlet } from 'react-router-dom'
import { AppSidebar } from '@/components/AppSidebar'

/** Root layout: header, global resource sidebar on the left, routed page content on the right. */
export function AppShell() {
  return (
    <div className="flex min-h-svh flex-col">
      <nav className="border-b p-4">
        <Link to="/" className="text-sm font-medium">
          ai-ec-agent
        </Link>
      </nav>

      <div className="flex flex-1">
        <AppSidebar />
        <main className="min-w-0 flex-1">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
