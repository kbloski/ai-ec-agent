import { ArrowLeft } from 'lucide-react'
import { NavLink, matchPath, useLocation, useNavigate } from 'react-router-dom'
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
  const { pathname } = useLocation()
  const navigate = useNavigate()
  const showBackButton = pathname !== '/' && pathname !== '/offers'
  const sections = [
    { pattern: '/offers/:id/*', links: [['knowledges', 'Knowledges']] },
    { pattern: '/knowledges/:id/*', links: [['analyses', 'Analizy'], ['brand-marketing', 'Brand marketing']] },
    { pattern: '/knowledges/:knowledgeId/analysis/:id/*', links: [['checklists', 'Checklisty'], ['questions', 'Pytania']] },
    { pattern: '/knowledges/:knowledgeId/analysis/:analysisId/checklists/:id/*', links: [['items', 'Zadania']] },
    { pattern: '/brand-marketing/:id/*', links: [['marketing-strategies', 'Marketing strategy']] },
    { pattern: '/marketing-strategy/:id/*', links: [['offer-strategies', 'Offer strategy']] },
    { pattern: '/offer-strategy/:id/*', links: [['message-strategies', 'Message strategy']] },
    { pattern: '/message-strategy/:id/*', links: [['ad-strategies', 'Ad strategy'], ['ugc-creatives', 'UGC creatives'], ['page-strategies', 'Page strategy']] },
    { pattern: '/ad-strategy/:id/*', links: [['creative-strategies', 'Creative strategy']] },
    { pattern: '/creative-strategy/:id/*', links: [['ad-executions', 'Ad execution']] },
    { pattern: '/ad-execution/:id/*', links: [['creative-executions', 'Creative execution']] },
    { pattern: '/page-strategy/:id/*', links: [['page-blueprints', 'Page blueprint']] },
    { pattern: '/page-blueprint/:id/*', links: [['content-plans', 'Content plan']] },
    { pattern: '/page-content-plan/:id/*', links: [['page-copies', 'Page copy']] },
  ] as const
  // Prefer the most specific route, otherwise an analysis URL would match Knowledge first.
  const section = [...sections].sort((a, b) => b.pattern.length - a.pattern.length)
    .map((config) => ({ config, match: matchPath(config.pattern, pathname) }))
    .find(({ match }) => match)

  if (section) {
    const detailPath = section.match?.pathnameBase ?? pathname

    return (
      <aside className="hidden w-56 shrink-0 flex-col border-r p-4 lg:flex">
        {showBackButton && (
          <button
            type="button"
            onClick={() => navigate(-1)}
            className="mb-5 flex items-center gap-2 rounded-md px-2 py-2 text-sm text-muted-foreground hover:bg-accent hover:text-accent-foreground"
          >
            <ArrowLeft className="size-4" />
            Wstecz
          </button>
        )}
        <h2 className="mb-2 px-2 text-xs font-medium tracking-wide text-muted-foreground uppercase">
          Zasoby
        </h2>
        <nav className="space-y-1">
          {section.config.links.map(([slug, label]) => (
            <NavLink key={slug} to={`${detailPath}/${slug}`} className={navLinkClassName}>{label}</NavLink>
          ))}
        </nav>
      </aside>
    )
  }

  return <aside className="hidden w-56 shrink-0 flex-col border-r p-4 lg:flex">
    {showBackButton && (
      <button
        type="button"
        onClick={() => navigate(-1)}
        className="flex items-center gap-2 rounded-md px-2 py-2 text-sm text-muted-foreground hover:bg-accent hover:text-accent-foreground"
      >
        <ArrowLeft className="size-4" />
        Wstecz
      </button>
    )}
  </aside>
}
