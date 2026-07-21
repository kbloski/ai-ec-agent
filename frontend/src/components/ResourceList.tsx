import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import type { Entity } from '@/types'

interface ResourceListProps {
  title: string
  items: Entity[] | undefined
  isLoading: boolean
  error?: unknown
  linkTo: (item: Entity) => string
  itemLabel?: (item: Entity) => string
  onGenerate?: () => void
  isGenerating?: boolean
  generateLabel?: string
}

/** Generic "list of children + generate new one" block reused by every pipeline stage page. */
export function ResourceList({
  title,
  items,
  isLoading,
  error,
  linkTo,
  itemLabel = (item) => (item.name as string) ?? `#${item.id}`,
  onGenerate,
  isGenerating,
  generateLabel = 'Generuj',
}: ResourceListProps) {
  return (
    <section className="space-y-3 rounded-lg border p-4">
      <div className="flex items-center justify-between gap-2">
        <h2 className="text-lg font-semibold">{title}</h2>
        {onGenerate && (
          <Button size="sm" onClick={onGenerate} disabled={isGenerating}>
            {isGenerating ? 'Generowanie…' : generateLabel}
          </Button>
        )}
      </div>

      {isLoading && <p className="text-sm text-muted-foreground">Ładowanie…</p>}
      {Boolean(error) && (
        <p className="text-sm text-destructive">Nie udało się pobrać danych.</p>
      )}
      {!isLoading && !error && (items?.length ?? 0) === 0 && (
        <p className="text-sm text-muted-foreground">Brak elementów — wygeneruj pierwszy.</p>
      )}

      <ul className="space-y-1">
        {items?.map((item) => (
          <li key={item.id}>
            <Link
              to={linkTo(item)}
              className="block rounded-md border px-3 py-2 text-sm hover:bg-accent"
            >
              {itemLabel(item)}
            </Link>
          </li>
        ))}
      </ul>
    </section>
  )
}
