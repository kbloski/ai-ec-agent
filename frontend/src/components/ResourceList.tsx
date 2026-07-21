import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import type { Entity } from '@/types'

interface ResourceListProps {
  title: string
  items: Entity[] | undefined
  isLoading: boolean
  error?: unknown
  linkTo?: (item: Entity) => string
  itemLabel?: (item: Entity) => string
  onGenerate?: () => void
  isGenerating?: boolean
  generateLabel?: string
  onDelete?: (item: Entity) => void
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
  onDelete,
}: ResourceListProps) {
  const count = items?.length ?? 0

  return (
    <section className="overflow-hidden rounded-lg border">
      <div className="flex items-center justify-between gap-2 border-b bg-muted/40 px-4 py-2.5">
        <h2 className="text-sm font-semibold">
          {title}
          {count > 0 && (
            <span className="ml-1.5 font-normal text-muted-foreground">({count})</span>
          )}
        </h2>
        {onGenerate && (
          <Button size="sm" onClick={onGenerate} disabled={isGenerating}>
            {isGenerating ? 'Generowanie…' : generateLabel}
          </Button>
        )}
      </div>

      {isLoading && <p className="px-4 py-3 text-sm text-muted-foreground">Ładowanie…</p>}
      {Boolean(error) && (
        <p className="px-4 py-3 text-sm text-destructive">Nie udało się pobrać danych.</p>
      )}
      {!isLoading && !error && count === 0 && (
        <p className="px-4 py-3 text-sm text-muted-foreground">Brak elementów — wygeneruj pierwszy.</p>
      )}

      {count > 0 && (
        <ul className="divide-y">
          {items?.map((item) => (
            <li key={item.id} className="flex items-center gap-2 px-4 py-2.5 hover:bg-accent/50">
              {linkTo ? (
                <Link to={linkTo(item)} className="flex-1 truncate text-sm hover:underline">
                  {itemLabel(item)}
                </Link>
              ) : (
                <span className="flex-1 truncate text-sm">{itemLabel(item)}</span>
              )}
              {onDelete && (
                <Button
                  size="sm"
                  variant="black"
                  onClick={() => {
                    if (window.confirm('Czy na pewno usunąć ten element?')) {
                      onDelete(item)
                    }
                  }}
                >
                  Usuń
                </Button>
              )}
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
