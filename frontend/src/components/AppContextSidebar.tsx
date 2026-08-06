import { ArrowLeft } from 'lucide-react'
import { NavLink, matchPath, useLocation, useNavigate } from 'react-router-dom'
import { cn } from '@/lib/utils'

const navLinkClassName = ({ isActive }: { isActive: boolean }) =>
  cn(
    'flex items-center gap-2 rounded-md px-3 py-2 text-sm',
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
    { pattern: '/offers/:id/*', process: [['knowledges', 'Knowledges']], resources: [['insights', 'Insights'], ['items', 'Elementy oferty']] },
    { pattern: '/knowledges/:id/*', process: [['brand-marketing', 'Brand marketing']], knowledge: [['analyses', 'Analizy']], resources: [['insights', 'Insights'], ['target-audiences', 'Grupy docelowe']] },
    { pattern: '/knowledges/:knowledgeId/analysis/:id/*', process: [['checklists', 'Checklisty']], resources: [['questions', 'Pytania']] },
    { pattern: '/knowledges/:knowledgeId/analysis/:analysisId/checklists/:id/*', process: [], resources: [['items', 'Zadania']] },
    { pattern: '/brand-marketing/:id/*', process: [['marketing-strategies', 'Marketing strategy']], resources: [] },
    { pattern: '/marketing-strategy/:id/*', process: [['offer-strategies', 'Offer strategy']], resources: [] },
    { pattern: '/offer-strategy/:id/*', process: [['message-strategies', 'Message strategy']], resources: [] },
    { pattern: '/message-strategy/:id/*', process: [['ad-strategies', 'Ad strategy'], ['ugc-creatives', 'UGC creatives'], ['page-strategies', 'Page strategy']], resources: [] },
    { pattern: '/ad-strategy/:id/*', process: [['creative-strategies', 'Creative strategy']], resources: [] },
    { pattern: '/creative-strategy/:id/*', process: [['ad-executions', 'Ad execution']], resources: [] },
    { pattern: '/ad-execution/:id/*', process: [['creative-executions', 'Creative execution']], resources: [] },
    { pattern: '/page-strategy/:id/*', process: [['page-blueprints', 'Page blueprint']], resources: [] },
    { pattern: '/page-blueprint/:id/*', process: [['content-plans', 'Content plan']], resources: [] },
    { pattern: '/page-content-plan/:id/*', process: [['page-copies', 'Page copy']], resources: [] },
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
        {section.config.process.length > 0 && (
          <section>
            <h2 className="mb-2 border-b border-foreground/30 px-2 pb-2 text-xs font-semibold tracking-wide text-foreground uppercase">
              Proces
            </h2>
            <nav className="ml-2 space-y-1 border-l pl-2">
              {section.config.process.map(([slug, label]) => (
                <NavLink key={slug} to={`${detailPath}/${slug}`} className={navLinkClassName}>{label}</NavLink>
              ))}
            </nav>
          </section>
        )}

        {'knowledge' in section.config && section.config.knowledge.length > 0 && (
          <section className={section.config.process.length > 0 ? 'mt-6' : undefined}>
            <h2 className="mb-2 border-b border-foreground/30 px-2 pb-2 text-xs font-semibold tracking-wide text-foreground uppercase">
              Wiedza
            </h2>
            <nav className="ml-2 space-y-1 border-l pl-2">
              {section.config.knowledge.map(([slug, label]) => (
                <NavLink key={slug} to={`${detailPath}/${slug}`} className={navLinkClassName}>{label}</NavLink>
              ))}
            </nav>
          </section>
        )}

        {section.config.resources.length > 0 && (
          <section className={section.config.process.length > 0 || 'knowledge' in section.config ? 'mt-6' : undefined}>
            <h2 className="mb-2 border-b border-foreground/30 px-2 pb-2 text-xs font-semibold tracking-wide text-foreground uppercase">
              Zasoby
            </h2>
            <nav className="ml-2 space-y-1 border-l pl-2">
              {section.config.resources.map(([slug, label]) => (
                <NavLink key={slug} to={`${detailPath}/${slug}`} className={navLinkClassName}>{label}</NavLink>
              ))}
            </nav>
          </section>
        )}
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
