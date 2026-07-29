import type { ReactNode } from 'react'
import { Link } from 'react-router-dom'
import { EntityFields } from '@/components/EntityFields'
import { EditableFields } from '@/components/EditableFields'
import { ChevronDown } from 'lucide-react'
import { EntityViewer } from '@/components/EntityViewer'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import type { Entity } from '@/types'

interface DetailShellProps {
  title: string
  backTo?: string
  backLabel?: string
  data: Entity | undefined
  isLoading: boolean
  error?: unknown
  children?: ReactNode
  exclude?: string[]
  collapsibleFields?: string[]
  itemActions?: Record<string, (item: Record<string, unknown>) => void>
  itemLinks?: Record<string, (item: Record<string, unknown>) => string>
  /** When provided, renders an always-on inline edit form instead of the read-only fields panel. */
  editable?: {
    onSave: (fields: Record<string, unknown>) => Promise<void>
    isSaving?: boolean
  }
}

/** Shared layout for every "detail" page: title, entity fields, optional child sections. */
export function DetailShell({
  title,
  backTo,
  backLabel = '← Wstecz',
  data,
  isLoading,
  error,
  children,
  exclude,
  collapsibleFields,
  itemActions,
  itemLinks,
  editable,
}: DetailShellProps) {
  return (
    <div className="grid grid-cols-1 gap-6 p-6 md:grid-cols-[280px_1fr]">
      <aside className="order-2 space-y-4 md:order-1">
        <h2 className="text-xs font-medium tracking-wide text-muted-foreground uppercase">
          Zasoby
        </h2>
        {data &&
          (children ? (
            <div className="space-y-4">{children}</div>
          ) : (
            <p className="text-sm text-muted-foreground">Brak powiązanych zasobów.</p>
          ))}
      </aside>

      <div className="order-1 max-w-3xl space-y-6 md:order-2">
        {backTo && (
          <Link to={backTo} className="text-sm text-muted-foreground hover:underline">
            {backLabel}
          </Link>
        )}

        <h1 className="text-2xl font-semibold">{title}</h1>

        {data && (
          <Collapsible>
            <CollapsibleTrigger className="group flex items-center gap-1.5 text-xs font-medium tracking-wide text-muted-foreground uppercase hover:text-foreground">
              <ChevronDown className="size-3.5 shrink-0 transition-transform group-data-[panel-open]:rotate-180" />
              Pokaż surowy JSON
            </CollapsibleTrigger>
            <CollapsibleContent className="pt-2">
              <EntityViewer data={data} />
            </CollapsibleContent>
          </Collapsible>
        )}

        {isLoading && <p className="text-sm text-muted-foreground">Ładowanie…</p>}
        {Boolean(error) && <p className="text-sm text-destructive">Nie udało się pobrać danych.</p>}

        {data && (
          <div className="rounded-lg border p-4">
            {editable ? (
              <EditableFields
                data={data}
                itemActions={itemActions}
                itemLinks={itemLinks}
                isSaving={editable.isSaving}
                onSave={(fields) => editable.onSave(fields)}
              />
            ) : (
              <EntityFields
                data={data}
                exclude={exclude}
                collapsibleFields={collapsibleFields}
                itemActions={itemActions}
                itemLinks={itemLinks}
              />
            )}
          </div>
        )}
      </div>
    </div>
  )
}
