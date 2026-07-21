import type { ReactNode } from 'react'
import { Link } from 'react-router-dom'
import { EntityFields } from '@/components/EntityFields'
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

        {isLoading && <p className="text-sm text-muted-foreground">Ładowanie…</p>}
        {Boolean(error) && <p className="text-sm text-destructive">Nie udało się pobrać danych.</p>}

        {data && (
          <div className="rounded-lg border p-4">
            <EntityFields data={data} exclude={exclude} collapsibleFields={collapsibleFields} />
          </div>
        )}
      </div>
    </div>
  )
}
