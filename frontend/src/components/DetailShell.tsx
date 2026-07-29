import { useState, type ReactNode } from 'react'
import { Link } from 'react-router-dom'
import { EntityFields } from '@/components/EntityFields'
import { EditableFields } from '@/components/EditableFields'
import { Button } from '@/components/ui/button'
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
  /** When provided, renders an "Edytuj" toggle that swaps the read-only fields panel for an inline edit form. */
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
  const [isEditing, setIsEditing] = useState(false)

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

        <div className="flex items-center justify-between gap-2">
          <h1 className="text-2xl font-semibold">{title}</h1>
          {editable && data && !isEditing && (
            <Button size="sm" variant="black" onClick={() => setIsEditing(true)}>
              Edytuj
            </Button>
          )}
        </div>

        {isLoading && <p className="text-sm text-muted-foreground">Ładowanie…</p>}
        {Boolean(error) && <p className="text-sm text-destructive">Nie udało się pobrać danych.</p>}

        {data && (
          <div className="rounded-lg border p-4">
            {editable && isEditing ? (
              <EditableFields
                data={data}
                collapsibleFields={collapsibleFields}
                itemActions={itemActions}
                itemLinks={itemLinks}
                isSaving={editable.isSaving}
                onCancel={() => setIsEditing(false)}
                onSave={async (fields) => {
                  await editable.onSave(fields)
                  setIsEditing(false)
                }}
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
