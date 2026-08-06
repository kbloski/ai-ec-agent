import { Outlet } from 'react-router-dom'
import { AppSidebar } from '@/components/AppSidebar'
import { AppContextSidebar } from '@/components/AppContextSidebar'
import { Toaster } from '@/components/ui/sonner'

/** Root layout: primary sidebar, contextual sidebar, routed page content. */
export function AppShell() {
  return (
    <div className="flex min-h-svh">
      <AppSidebar />
      <AppContextSidebar />
      <main className="min-w-0 flex-1">
        <Outlet />
      </main>
      <Toaster position="bottom-right" richColors closeButton />
    </div>
  )
}
