import type { ReactNode } from 'react'
import { Link } from 'react-router-dom'
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
  itemActions?: Record<string, (item: Record<string, unknown>) => void>
  itemLinks?: Record<string, (item: Record<string, unknown>) => string>
  /** When provided, the fields panel becomes an editable form that saves via this handler; otherwise fields render disabled/read-only. */
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
  itemActions,
  itemLinks,
  editable,
}: DetailShellProps) {
  return (
    <div className="max-w-3xl space-y-6 p-6">
      {data && children && (
        <Collapsible>
          <CollapsibleTrigger className="group flex items-center gap-1.5 text-xs font-medium tracking-wide text-muted-foreground uppercase hover:text-foreground">
            <ChevronDown className="size-3.5 shrink-0 transition-transform group-data-[panel-open]:rotate-180" />
            Zasoby
          </CollapsibleTrigger>
          <CollapsibleContent className="pt-2">
            <div className="space-y-4">{children}</div>
          </CollapsibleContent>
        </Collapsible>
      )}

      <div className="space-y-6">
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
            <EditableFields
              data={data}
              exclude={exclude}
              itemActions={itemActions}
              itemLinks={itemLinks}
              isSaving={editable?.isSaving}
              onSave={editable ? (fields) => editable.onSave(fields) : undefined}
            />
          </div>
        )}
      </div>
    </div>
  )
}
