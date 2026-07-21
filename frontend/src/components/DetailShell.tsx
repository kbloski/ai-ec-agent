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
}: DetailShellProps) {
  return (
    <div className="mx-auto max-w-3xl space-y-6 p-6">
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
          <EntityFields data={data} />
        </div>
      )}

      {data && <div className="space-y-4">{children}</div>}
    </div>
  )
}
