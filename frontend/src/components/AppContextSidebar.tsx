import { NavLink, useMatch } from 'react-router-dom'
import { cn } from '@/lib/utils'

const navLinkClassName = ({ isActive }: { isActive: boolean }) =>
  cn(
    'flex items-center gap-2 rounded-md px-2 py-2 text-sm',
    isActive
      ? 'bg-accent text-accent-foreground'
      : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground',
  )

/** Secondary, contextual navigation shown next to the primary sidebar. Its content depends on which section of the app is active. */
export function AppContextSidebar() {
  const offerMatch = useMatch('/offers/:offerId/*')

  if (offerMatch) {
    const { offerId } = offerMatch.params

    return (
      <aside className="hidden w-56 shrink-0 flex-col border-r p-4 lg:flex">
        <h2 className="mb-2 px-2 text-xs font-medium tracking-wide text-muted-foreground uppercase">
          Zasoby
        </h2>
        <nav className="space-y-1">
          <NavLink to={`/offers/${offerId}/knowledges`} className={navLinkClassName}>
            Knowledges
          </NavLink>
        </nav>
      </aside>
    )
  }

  return (
    <aside className="hidden w-56 shrink-0 flex-col border-r p-4 lg:flex">
      <p className="text-sm text-muted-foreground">hello :D</p>
    </aside>
  )
}
